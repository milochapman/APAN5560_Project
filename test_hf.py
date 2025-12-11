from huggingface_hub import InferenceClient
from PIL import Image

client = InferenceClient()

try:
    img = client.text_to_image(
        "a fantasy landscape",
        model="stabilityai/stable-diffusion-xl-base-1.0"
    )
    print("Success:", img)
except Exception as e:
    print("Error:", e)