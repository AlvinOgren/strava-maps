import os
import json
import time
import requests
from fetch_credentials import fetch_credentials

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(BASE_DIR, "config", "strava_token.json")

def refresh_token():
    """Refresh the Strava API access token if it has expired."""
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError("Token file not found. Please authorize first.")

    with open(TOKEN_PATH) as f:
        try:
            token_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid token file format.")

    if "expires_at" not in token_data or "refresh_token" not in token_data:
        raise ValueError("Incomplete token data. Please reauthorize.")

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
        with open(TOKEN_PATH, "w") as f:
            json.dump(new_token_data, f)
        print("Token refreshed")
        return new_token_data["access_token"]

    return token_data["access_token"]