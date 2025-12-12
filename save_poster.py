import os
import json
import base64
import argparse
from datetime import datetime


def save_data_url_png(data_url: str, out_path: str) -> None:
    """
    Decode a data URL like: data:image/png;base64,xxxx... and save it as a PNG.
    """
    if not isinstance(data_url, str) or "," not in data_url:
        raise ValueError("image_url is not a valid data URL string")

    header, b64 = data_url.split(",", 1)

    # Basic validation
    if "base64" not in header.lower():
        raise ValueError(f"Unsupported data URL header: {header}")

    img_bytes = base64.b64decode(b64)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(img_bytes)

    print(f"Saved: {out_path}")


def sanitize_name(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return "variant"
    # Keep it filesystem-friendly
    bad = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for ch in bad:
        s = s.replace(ch, "_")
    s = s.replace(" ", "_")
    return s[:80]


def save_from_response_json(data: dict, out_dir: str, prefix: str) -> None:
    """
    Supports two response formats:
    1) Campaign: {"variants": [{"id":0,"variant":"theatrical poster","image_url":"data:image/png;base64,..."} , ...]}
    2) Single:  {"image_url":"data:image/png;base64,..."}
    """
    os.makedirs(out_dir, exist_ok=True)

    # Campaign response
    if isinstance(data, dict) and "variants" in data and isinstance(data["variants"], list):
        variants = data["variants"]
        if not variants:
            raise ValueError("Response contains 'variants' but it's empty.")

        for i, v in enumerate(variants):
            if not isinstance(v, dict):
                continue

            data_url = v.get("image_url")
            if not data_url:
                print(f"Skip variant index {i}: no image_url")
                continue

            vid = v.get("id", i)
            vname = sanitize_name(v.get("variant") or f"variant_{vid}")
            filename = f"{prefix}_{vid}_{vname}.png"
            out_path = os.path.join(out_dir, filename)
            save_data_url_png(data_url, out_path)

        return

    # Single poster response
    if isinstance(data, dict) and "image_url" in data and isinstance(data["image_url"], str):
        filename = f"{prefix}.png"
        out_path = os.path.join(out_dir, filename)
        save_data_url_png(data["image_url"], out_path)
        return

    raise ValueError(f"Unknown response format. Top-level keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")


def main():
    parser = argparse.ArgumentParser(
        description="Save images from Swagger response JSON (no API calls)."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the JSON file that contains the Swagger response (copy/paste response into a .json file)."
    )
    parser.add_argument(
        "--outdir",
        default="outputs",
        help="Output directory to save images (default: outputs)."
    )
    parser.add_argument(
        "--prefix",
        default=None,
        help="Filename prefix (default: timestamp)."
    )
    args = parser.parse_args()

    prefix = args.prefix or datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = args.outdir

    # Read JSON
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # If user accidentally saved {"response": {...}} or similar wrapper, allow simple unwrap
    if isinstance(data, dict) and "response" in data and isinstance(data["response"], dict):
        data = data["response"]

    save_from_response_json(data, out_dir=out_dir, prefix=prefix)
    print("Done.")


if __name__ == "__main__":
    main()
