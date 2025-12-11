import os
import base64
import requests

# FastAPI 服务地址
API_URL = "http://127.0.0.1:8000"


def save_data_url(data_url: str, out_path: str) -> None:
    """
    把 data:image/png;base64,... 这种格式的字符串解码并保存为 PNG 文件
    """
    header, b64 = data_url.split(",", 1)
    img_bytes = base64.b64decode(b64)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(img_bytes)

    print(f" Saved: {out_path}")


def generate_and_save(endpoint: str, payload: dict, prefix: str = "poster") -> None:
    """
    通用保存函数：
    - endpoint: "generate_poster" 或 "generate_campaign"
    - payload: 传给 API 的 JSON
    - prefix: 输出目录 / 文件名前缀
    """
    url = f"{API_URL}/{endpoint.lstrip('/')}"
    print(f" Calling API: {url}")
    print(f" Payload: {payload}")

    resp = requests.post(url, json=payload)
    print(f" Status code: {resp.status_code}")
    resp.raise_for_status()
    data = resp.json()

    # Case 1: generate_campaign → 有多个 variants
    if "variants" in data:
        print("Detected: campaign (multiple images) response")
        variants = data["variants"]
        out_dir = os.path.join("outputs", prefix)
        os.makedirs(out_dir, exist_ok=True)

        if not variants:
            print(" variants is empty, nothing to save.")
            return

        for v in variants:
            data_url = v.get("image_url")
            variant_name = (v.get("variant") or f"variant_{v.get('id','x')}").replace(" ", "_")
            vid = v.get("id", 0)

            if not data_url:
                print(f" Variant {vid} has no image_url, skipping.")
                continue

            filename = f"{vid}_{variant_name}.png"
            out_path = os.path.join(out_dir, filename)
            save_data_url(data_url, out_path)

    # Case 2: generate_poster → 单张图片
    elif "image_url" in data:
        print(" Detected: single poster response")
        data_url = data["image_url"]
        out_dir = "outputs"
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{prefix}.png")
        save_data_url(data_url, out_path)

    else:
        print("Unknown response format, keys:", list(data.keys()))
        raise ValueError("Unknown response format")

    print("Done.")


if __name__ == "__main__":
    # ① Campaign Posters
    campaign_payload = {
        "summary": "A legendary Jedi rises to confront a new Sith empire threatening the galaxy.",
        "style_hint": "Star Wars style, IMAX, SDXL, cinematic lighting, blue and purple neon, high detail"
    }

    generate_and_save(
        endpoint="generate_campaign",
        payload=campaign_payload,
        prefix="starwars_campaign"
    )

    # ② Single Poster
    single_poster_payload = {
        "summary": "A lone hero walks through a neon city at night.",
        "style_hint": "cyberpunk, SDXL, neon lights, dramatic, IMAX poster"
    }

    generate_and_save(
        endpoint="generate_poster",
        payload=single_poster_payload,
        prefix="cyberpunk_poster"
    )