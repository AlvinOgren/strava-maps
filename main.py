import os
import webbrowser
import subprocess
import time
from refresh_strava_token import refresh_token  # Refresh token functionality
from generate_map import generate_map  # Map generation functionality

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


def generate_and_open_map():
    """Generate the map and open it in the browser."""
    print("Generating the map...")
    try:
        # Refresh token and ensure it's valid
        access_token = refresh_token()

        # Generate the map
        map_path = generate_map(access_token, map_type="polyline")  # or "heatmap"
        print(f"Map generated successfully: {map_path}")

        # Open the map in the browser
        print("Opening the map in your default browser...")
        webbrowser.open(f"file://{os.path.abspath(map_path)}")
    except Exception as e:
        print(f"Failed to generate the map: {e}")
        exit(1)

if __name__ == "__main__":
    print("Welcome to the Strava Map Generator!")
    authorize_user()
    generate_and_open_map()
    print("\nProgram finished")