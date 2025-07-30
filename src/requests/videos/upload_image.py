from google.cloud import storage
import os

BUCKET_NAME = "sweet-treat-experimental-first-bucket"

def upload_to_gcs_from_filename(source_file_path):
    # Initialize GCS client (uses Application Default Credentials or service account)
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(BUCKET_NAME)

    # Create a blob object from the destination path
    blob = bucket.blob(f"images/{source_file_path}")

    # Upload the file
    blob.upload_from_filename(source_file_path)

    # Construct and return the GCS URI
    gcs_uri = f"gs://{BUCKET_NAME}/images/{source_file_path}"
    return gcs_uri

# if name == '__main__':
#     # Example usage:
#     local_file = "matcha.png"  # Local file path
#     uri = upload_to_gcs_from_filename(local_file)
#     print("Uploaded to:", uri)
