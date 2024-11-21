import json
import requests
import time
from fetch_credentials import fetch_credentials

def refresh_token():
    """Refresh the Strava access token if expired."""
    with open("strava_token.json") as f:
        token_data = json.load(f)

    if token_data["expires_at"] < time.time():
        client_id, client_secret = fetch_credentials()
        response = requests.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": token_data["refresh_token"],
            },
        )
        new_token_data = response.json()
        with open("strava_token.json", "w") as f:
            json.dump(new_token_data, f)
        print("Token refreshed!")
        return new_token_data["access_token"]

    return token_data["access_token"]