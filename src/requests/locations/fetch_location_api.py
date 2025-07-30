import requests
import openai
from io import BytesIO
from PIL import Image
import dotenv
import os

from src.scripts.create_video_from_image import create_video_from_image
dotenv.load_dotenv()

# 🔑 API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_place_id(restaurant_name, location="New York, NY"):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": f"{restaurant_name}, {location}", "key": GOOGLE_API_KEY}
    res = requests.get(url, params=params).json()
    return res["results"][0]["place_id"]

def get_place_photos(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "fields": "photos", "key": GOOGLE_API_KEY}
    res = requests.get(url, params=params).json()
    return res["result"].get("photos", [])

def get_photo_image(photo_reference) -> Image.Image:
    url = "https://maps.googleapis.com/maps/api/place/photo"
    params = {"photoreference": photo_reference, "maxwidth": 800, "key": GOOGLE_API_KEY}
    res = requests.get(url, params=params)
    return Image.open(BytesIO(res.content))

import base64

def describe_image_with_gpt4o(image: Image.Image) -> str:
    # Convert PIL image to base64-encoded string
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    base64_bytes = base64.b64encode(buffered.getvalue())
    base64_string = base64_bytes.decode("utf-8")
    data_url = f"data:image/png;base64,{base64_string}"

    # Call GPT-4o with image as base64-encoded URL
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image for a restaurant website."},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def main():
    restaurant = input("Enter restaurant name: ")
    place_id = get_place_id(restaurant)
    photos = get_place_photos(place_id)

    for i, photo in enumerate(photos[:5]):
        print(f"\n🔍 Describing photo {i + 1}...")
        image = get_photo_image(photo["photo_reference"])
        image.save(f"{restaurant}_{i}.png")
        description = describe_image_with_gpt4o(image)
        print(f"📸 Description: {description}")
        create_video_from_image(f"{restaurant}_{i}.png", f"{restaurant}_{i}.mp4")

if __name__ == "__main__":
    main()
