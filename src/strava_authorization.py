from flask import Flask, request, redirect
from threading import Thread
import requests
import json
import os
import subprocess
import time
from fetch_credentials import fetch_credentials

CLIENT_ID, CLIENT_SECRET = fetch_credentials()
REDIRECT_URI = "http://127.0.0.1:5000/callback"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config/strava_token.json")
TOKEN_PATH = os.path.join(BASE_DIR, "config", "strava_token.json")

app = Flask(__name__)

def authorize_user():
    """Start the Flask app to authorize the user."""
    print("Authorizing with Strava...")
    try:
        process = subprocess.Popen(["python3", "src/strava_authorization.py"])
        print("Once authorized, return to this terminal. Waiting for authorization...\n")
        
        # Wait for the token file to be created
        while not os.path.exists(TOKEN_PATH):
            time.sleep(1)

        print("Authorization successful! Terminating Flask process...")
        process.terminate()
    except KeyboardInterrupt:
        print("Authorization canceled by user.")
        process.terminate()
        exit(1)

    if not os.path.exists(TOKEN_PATH):
        print("Authorization failed. Please try again.")
        exit(1)

@app.route("/")
def home():
    """Redirects the user to Strava's OAuth authorization page."""
    auth_url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=activity:read_all"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """Handle the OAuth callback and exchange the authorization code for an access token."""
    code = request.args.get("code")
    if not code:
        return "Authorization failed. Please try again."

    token_response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        },
    )
    token_data = token_response.json()
    if "access_token" not in token_data:
        return "Failed to retrieve access token. Please try again."

    # Write token data to the correct location
    with open(CONFIG_PATH, "w") as f:
        json.dump(token_data, f)

    return "Authorization successful! You can close this window."

if __name__ == "__main__":
    print("Open your browser and navigate to http://127.0.0.1:5000 to log in.")
    app.run(port=5000)