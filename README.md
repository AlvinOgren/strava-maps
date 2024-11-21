# strava-maps
Try: run python setup.py
If it fails, try: python3 -m pip install flask requests folium polyline

Before running the program, add your Client ID and Client Secret to the designated spots in the strava_credentials.json file. Both Client ID and Client Secret can be found under Strava -> Settings -> My API Application.

If you however haven't set up and application in Strava's Developer Portal yet, here's how:

Go to the Strava Developer Portal (https://developers.strava.com/) and log in with your Strava account.

Click on "Create & Manage My API Application".

Fill out the application form with the following details:

Application Name: Choose a name for your app (e.g., "My Strava Map Tool").
Category: Select a category (e.g., "Personal" or "Development").
Website: Provide any URL, such as a personal website or placeholder (e.g., https://example.com).
Authorization Callback Domain: Enter http://127.0.0.1:5000 (or the domain your app will run on). This is required for the OAuth flow.
Save the application by clicking Save or Create. After saving, you’ll be redirected to a page displaying your app's Client ID and Client Secret.

To run the program: python3 main.py. Follow the provided link and authorize