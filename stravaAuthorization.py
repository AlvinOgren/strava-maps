import requests
import json
from flask import Flask, request, redirect
from fetch_credentials import fetch_credentials  # Import the function

# Fetch credentials from file or environment variables
CLIENT_ID, CLIENT_SECRET = fetch_credentials()
REDIRECT_URI = "http://127.0.0.1:5000/callback"  # Flask server running locally

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    # Step 1: Redirect user to Strava authorization page
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
    # Step 2: Strava redirects back to this route with a code
    code = request.args.get("code")
    if not code:
        return "Authorization failed. Please try again."

    # Step 3: Exchange authorization code for an access token
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

    # Save the access token for future use
    with open("strava_token.json", "w") as f:
        json.dump(token_data, f)
    return "Authorization successful! You can close this window."

if __name__ == "__main__":
    # Start the Flask web server
    print("Open your browser and navigate to http://127.0.0.1:5000 to log in.")
    app.run(port=5000)