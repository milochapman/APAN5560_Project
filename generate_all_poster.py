import requests
import base64

API_URL = "http://127.0.0.1:8000/generate_poster"

movies = [
    {
        "slug": "avatar_fire_and_ash",
        "summary": "In the aftermath of a new interplanetary conflict, Jake Sully and the Na’vi face a mysterious force born from fire and ash that threatens Pandora’s balance.",
        "style_hint": "epic, bioluminescent, alien",
    },
    {
        "slug": "super_mario_galaxy_movie",
        "summary": "Mario travels across floating planets and cosmic landscapes to stop Bowser from taking control of a galaxy-shifting star.",
        "style_hint": "colorful, whimsical, cosmic",
    },
    {
        "slug": "avengers_5",
        "summary": "The Avengers reunite to confront a new multiversal threat that merges timelines and forces unlikely heroes to fight side by side.",
        "style_hint": "heroic, dramatic, high-energy",
    },
    {
        "slug": "toy_story_5",
        "summary": "Woody, Buzz, and their friends embark on a new adventure after discovering a hidden world of forgotten toys seeking a place to belong.",
        "style_hint": "warm, nostalgic, family-friendly",
    },
]


def generate_and_save(movie):
    payload = {
        "summary": movie["summary"],
        "style_hint": movie["style_hint"],
    }

    print(f"\nRequesting poster for: {movie['slug']} ...")
    resp = requests.post(API_URL, json=payload)
    resp.raise_for_status()

    data = resp.json()
    data_url = data["image_url"]

    # data_url 形如 "data:image/png;base64,AAAA...."
    header, b64 = data_url.split(",", 1)
    img_bytes = base64.b64decode(b64)

    out_path = f"poster_{movie['slug']}.png"
    with open(out_path, "wb") as f:
        f.write(img_bytes)

    print(f"Saved to {out_path}")


def main():
    for m in movies:
        generate_and_save(m)


if __name__ == "__main__":
    main()
