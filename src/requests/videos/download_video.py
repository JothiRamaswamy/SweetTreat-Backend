from typing import Optional
from google.cloud import storage
import os

def download_video_from_gcs(gcs_uri: str, local_path: Optional[str] = None):
    print(local_path)
    """
    Downloads a video from a GCS URI to a local file.

    Args:
        gcs_uri (str): GCS URI in the format gs://bucket-name/path/to/video.mp4
        local_path (str): Local file path where the video should be saved
    """
    if local_path is None:
        local_path = gcs_uri.split('/')[-1]
    if not gcs_uri.startswith("gs://"):
        raise ValueError("Invalid GCS URI. Must start with 'gs://'")

    # Parse bucket and blob
    parts = gcs_uri[5:].split('/', 1)
    if len(parts) != 2:
        raise ValueError("Invalid GCS URI format. Expected gs://bucket/path")

    bucket_name, blob_path = parts

    # Initialize GCS client
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    # Download the blob to the local path
    blob.download_to_filename(local_path)
    print(f"Downloaded: {gcs_uri} → {local_path}")

# if __name__ == '__main__':
#     download_video_from_gcs("gs://sweet-treat-experimental-first-bucket/videos/10234769133952762370/sample_0.mp4", "matcha.mp4")
