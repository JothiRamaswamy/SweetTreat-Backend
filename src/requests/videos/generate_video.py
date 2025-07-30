from typing import Optional
import requests
from src.utils.access_token import get_access_token
from src.constants import LOCATION, PROJECT_ID, MODEL_ID

url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:predictLongRunning"

def generate_video(image_gcs_uri, video_gcs_uri) -> Optional[str]:

    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    payload = {
        "instances": [
            {
                "prompt": "You are a 23 year old white collar worker who is solo exploring a city and wants to post fun, casual videos of what she is doing on her anonymous instagram/tiktok account. You need to create faceless content with NONE of your body visible in the frame. No faces or hands. You need videos that look like they were taken by the average person with the back camera of an iphone. Your task: Create a 5-second video from this exact image. The video should look like this image was a still pulled from a real moment. Use only subtle, natural motion: slight camera sway, maybe a blink of motion in the blurred background. No lighting changes, no added elements (NO additional hands in the frame. NO gestures and pointing whatsoever and that is a demand.). Keep everything exactly as-is. The result should feel like raw, unstaged UGC captured on a phone, matching Gen Z TikTok content in realism and casualness. Honestly, if you just make it look like a swaying video in the worst case scenario, that is good enough. better than any flesh of a hand that was not orgiinally in the picture. The video should be slightly low quality, and 'grainy' looking",
                "image": {
                    # Only one of the following should be provided
                    # "bytesBase64Encoded": "base64-encoded-image-data",
                    "gcsUri": image_gcs_uri,
                    "mimeType": "image/png"
                },
            }
        ],
        "parameters": {
            "aspectRatio": "9:16",
            "durationSeconds": 5,
            "enhancePrompt": False,
            "generateAudio": False,
            "negativePrompt": "",
            "personGeneration": "none",
            "sampleCount": 1,
            "seed": 42,
            "storageUri": video_gcs_uri
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        assert 'name' in data
        return data['name'].split('/')[-1]
        
    else:
        print("Failed to generate video")
        return None
    
# if __name__ == '__main__':
#     generate_video("gs://sweet-treat-experimental-first-bucket/images/matcha.png", "gs://sweet-treat-experimental-first-bucket/videos")
