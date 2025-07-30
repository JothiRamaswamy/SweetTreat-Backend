from typing import Optional
from src.requests.videos.upload_image import upload_to_gcs_from_filename
from src.requests.videos.generate_video import generate_video
from src.requests.videos.get_video import get_video

def create_video_from_image(image_path: str, download_name: Optional[str] = None) -> None:
    image_gcs_uri = upload_to_gcs_from_filename(image_path)
    video_gcs_uri = "gs://sweet-treat-experimental-first-bucket/videos/"
    operation_id = generate_video(image_gcs_uri, video_gcs_uri)
    print(operation_id)
    finished = False
    while(not finished):
        try:
            print(download_name)
            video = get_video(operation_id, download_name)
            finished = True
        except Exception as e:
            finished = False
            
if __name__ == '__main__':
    create_video_from_image("photo_3.png", "photo_3.mp4")
        
    