import requests
import time
from src.requests.videos.download_video import download_video_from_gcs
from src.utils.access_token import get_access_token
from typing import Optional, List

def get_video(operation_id, download_name: Optional[str] = None) -> Optional[List[str]]:
    print(download_name)
    request_data = {
        "operationName": "projects/sweettreat-464701/locations/us-central1/publishers/google/models/veo-2.0-generate-001/operations/" + operation_id
    }
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/sweettreat-464701/locations/us-central1/publishers/google/models/veo-2.0-generate-001:fetchPredictOperation"

    headers = {
        "Authorization": f"Bearer {get_access_token()}",  # Your OAuth2 token
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=request_data)
    print("Response status code:", response.status_code)
    print("Response text:", response.text)
    
    if response.text:
        result = response.json()
        if 'done' in result:
            if 'response' in result:
                video_list = [r['gcsUri'] for r in result['response']['videos']]
                for video in video_list:
                    download_video_from_gcs(video, download_name)
                return video_list
            elif 'error' in result:
                return Exception(result['error'])['message']
        else:
            time.sleep(5)
            return get_video(operation_id, download_name)

# if __name__ == "__main__":
#     print(get_video("780beb6c-c816-4505-91d8-63bdc2abd936", "temp_matcha.mp4"))