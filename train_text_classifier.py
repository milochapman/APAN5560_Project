import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from typing import Dict

import numpy as np
import torch
from torch.utils.data import DataLoader

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import evaluate
from sklearn.metrics import classification_report


# parameters

MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = os.path.join("models", "genre_classifier_distilbert")

MAX_LENGTH = 128       
BATCH_SIZE = 32        
NUM_EPOCHS = 1         
LEARNING_RATE = 5e-5

MAX_TRAIN_SAMPLES = 60000 
MAX_EVAL_SAMPLES = 8000     
MAX_TEST_SAMPLES = 8000     


def prepare_label_mapping(dataset) -> Dict[str, int]:
    """Collect all genres from the dataset to build label2id / id2label."""
    genres = sorted(list(set(dataset["train"]["genre"])))
    label2id = {g: i for i, g in enumerate(genres)}
    id2label = {i: g for g, i in label2id.items()}
    return label2id, id2label


def main():
    
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f"Using device: {device}")

    print("Loading dataset jquigl/imdb-genres ...")
    raw_datasets = load_dataset("jquigl/imdb-genres")

    label2id, id2label = prepare_label_mapping(raw_datasets)
    num_labels = len(label2id)
    print(f"Num labels: {num_labels}")
    print("Labels:", id2label)

    #tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=num_labels,
        label2id=label2id,
        id2label=id2label,
    ).to(device)

    # description to token ids + label id
    def preprocess_function(examples):
        texts = examples["description"]
        labels = [label2id[g] for g in examples["genre"]]
        encodings = tokenizer(
            texts,
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
        )
        encodings["labels"] = labels
        return encodings

    print("Tokenizing datasets ...")
    tokenized_datasets = raw_datasets.map(
        preprocess_function,
        batched=True,
        remove_columns=[
            "movie title - year",
            "genre",
            "expanded-genres",
            "rating",
            "description",
        ],
    )

    full_train = tokenized_datasets["train"]
    full_eval = tokenized_datasets["validation"]
    full_test = tokenized_datasets["test"]

    train_dataset = full_train.shuffle(seed=42).select(
        range(min(MAX_TRAIN_SAMPLES, len(full_train)))
    )
    eval_dataset = full_eval.shuffle(seed=42).select(
        range(min(MAX_EVAL_SAMPLES, len(full_eval)))
    )
    test_dataset = full_test.shuffle(seed=42).select(
        range(min(MAX_TEST_SAMPLES, len(full_test)))
    )

    print(
        f"Using {len(train_dataset)} train samples, "
        f"{len(eval_dataset)} eval samples, {len(test_dataset)} test samples."
    )

    # torch
    train_dataset.set_format(type="torch")
    eval_dataset.set_format(type="torch")
    test_dataset.set_format(type="torch")

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    eval_loader = DataLoader(eval_dataset, batch_size=BATCH_SIZE)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

    # evaluate
    accuracy = evaluate.load("accuracy")
    f1 = evaluate.load("f1")

    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)

    # fine-tuning
    for epoch in range(NUM_EPOCHS):
        model.train()
        total_loss = 0.0
        num_batches = 0

        print(f"\nEpoch {epoch + 1}/{NUM_EPOCHS}")
        for batch in train_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            optimizer.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            num_batches += 1
            if num_batches % 200 == 0:
                print(f"  Batch {num_batches}, loss = {total_loss / num_batches:.4f}")

        avg_loss = total_loss / max(num_batches, 1)
        print(f"Epoch {epoch + 1} training loss: {avg_loss:.4f}")

        # epoch 
        model.eval()
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for batch in eval_loader:
                labels = batch["labels"].numpy()
                batch = {k: v.to(device) for k, v in batch.items()}
                outputs = model(**batch)
                logits = outputs.logits
                preds = torch.argmax(logits, dim=-1).cpu().numpy()

                all_preds.extend(list(preds))
                all_labels.extend(list(labels))

        acc = accuracy.compute(predictions=all_preds, references=all_labels)["accuracy"]
        f1_macro = f1.compute(
            predictions=all_preds,
            references=all_labels,
            average="macro",
        )["f1"]
        print(f"Validation accuracy: {acc:.4f}, macro-F1: {f1_macro:.4f}")

    # evaluate
    print("\nEvaluating on test set ...")
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in test_loader:
            labels = batch["labels"].numpy()
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=-1).cpu().numpy()

            all_preds.extend(list(preds))
            all_labels.extend(list(labels))

    acc = accuracy.compute(predictions=all_preds, references=all_labels)["accuracy"]
    f1_macro = f1.compute(
        predictions=all_preds,
        references=all_labels,
        average="macro",
    )["f1"]

    print("Test accuracy:", acc)
    print("Test macro-F1:", f1_macro)

    target_names = [id2label[i] for i in range(num_labels)]
    print("\nClassification report on test set:")
    print(
        classification_report(
            all_labels,
            all_preds,
            target_names=target_names,
            digits=4,
        )
    )

    # save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Saving model to {OUTPUT_DIR} ...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("Finished! You can now load the model from:", OUTPUT_DIR)


if __name__ == "__main__":
    main()