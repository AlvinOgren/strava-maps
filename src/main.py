import os
import webbrowser
import subprocess
import time
from refresh_strava_token import refresh_token
from generate_map import generate_map
from strava_authorization import authorize_user


def generate_and_open_map():
    """Generate the map and open it in the browser."""
    print("Generating the map...")
    try:
        # Refresh token and ensure it's valid
        access_token = refresh_token()

        # Generate the map
        map_path = generate_map(access_token, map_type="polyline")  # or "heatmap" (might not work perfectly, but is not necessary for the project)
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