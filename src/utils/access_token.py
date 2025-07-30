from google.auth import default
from google.auth.transport.requests import Request


def get_access_token():
    # Get default credentials
    credentials, project = default()

    # Refresh credentials to get access token
    credentials.refresh(Request())

    # Get the access token
    access_token = credentials.token
    return access_token