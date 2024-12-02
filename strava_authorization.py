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

app = Flask(__name__)

def authorize_user():
    """Start the Flask app to authorize the user."""
    print("Authorizing with Strava...")
    try:
        process = subprocess.Popen(["python3", "strava_authorization.py"])
        print("Once authorized, return to this terminal. Waiting for authorization...\n")
        
        # Wait for the token file to be created
        while not os.path.exists("strava_token.json"):
            time.sleep(1)

        print("Authorization successful! Terminating Flask process...")
        process.terminate()
    except KeyboardInterrupt:
        print("Authorization canceled by user.")
        process.terminate()
        exit(1)

    if not os.path.exists("strava_token.json"):
        print("Authorization failed. Please try again.")
        exit(1)

@app.route("/")
def home():
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
    code = request.args.get("code")
    exit_flag = request.args.get("exit")

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

    with open("strava_token.json", "w") as f:
        json.dump(token_data, f)

    if exit_flag:
        def shutdown():
            os._exit(0)
        Thread(target=shutdown).start()

    return "Authorization successful! You can close this window."

if __name__ == "__main__":
    print("Open your browser and navigate to http://127.0.0.1:5000 to log in.")
    app.run(port=5000)


