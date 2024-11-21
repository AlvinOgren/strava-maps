import os
import json

def fetch_credentials():
    """Fetch Client ID and Secret from a JSON file or environment variables."""
    credentials_path = "strava_credentials.json"

    if os.path.exists(credentials_path):
        with open(credentials_path, "r") as f:
            credentials = json.load(f)
            if "client_id" in credentials and "client_secret" in credentials:
                return credentials["client_id"], credentials["client_secret"]
            else:
                raise ValueError(
                    "Invalid credentials format in 'strava_credentials.json'."
                )

    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")

    if client_id and client_secret:
        return client_id, client_secret
    else:
        raise EnvironmentError(
            "Client ID and Secret not found! Set them in 'strava_credentials.json' "
            "or as environment variables."
        )