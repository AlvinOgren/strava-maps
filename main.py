import os
import webbrowser
import subprocess
from refresh_strava_token import refresh_token  # Script to refresh tokens
from generate_map import generate_map  # Script to generate map

def authorize_user():
    """Start the Flask app to authorize the user."""
    print("Step 1: Authorizing with Strava...")
    try:
        # Run the Flask app (strava_authorization.py) in a subprocess
        process = subprocess.Popen(["python3", "strava_authorization.py"])
        
        print("\nOnce authorized, return to this terminal. Waiting for authorization...\n")
        process.wait()  # Wait for the Flask app to finish
    except KeyboardInterrupt:
        print("Authorization canceled by user.")
        process.terminate()
        exit(1)

    if os.path.exists("strava_token.json"):
        print("Authorization successful!")
    else:
        print("Authorization failed. Please try again.")
        exit(1)

def generate_and_open_map():
    """Generate the map and open it in the browser."""
    print("\nStep 2: Generating the map...")
    
    try:
        # Refresh the token to ensure it's valid
        access_token = refresh_token()
        
        # Generate the map
        map_path = generate_map(access_token)
        print(f"Map generated successfully: {map_path}")
        
        # Open the map in the default browser
        print("Step 3: Opening the map in your default browser...")
        webbrowser.open(f"file://{os.path.abspath(map_path)}")
    except Exception as e:
        print(f"Failed to generate the map: {e}")
        exit(1)

if __name__ == "__main__":
    print("Welcome to the Strava Map Generator!")
    authorize_user()
    generate_and_open_map()
    print("\nAll done! Enjoy exploring your rides on the map.")