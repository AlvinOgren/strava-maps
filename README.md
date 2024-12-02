# Strava Maps

A Python application for visualizing users Strava activities on an interactive map. The project allows the user to authenticate with the Strava API, fetch their activities data and generate a map based on that data.

## Install Dependencies
To install the required libraries:
`pip install -r requirements.txt`

## Configure Strava API Access
1. Create an application in the [Strava Developer Portal](https://developers.strava.com/).

2. Save your Client ID and Client Secret provided by Strava.

3. Replace the placeholders for Client ID and Client Secret in `strava_credentials.json`. Alternatively, you can set these as environment variables as `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`.

## Usage
To run the program:
`python3 main.py`

- Follow the link provided in the terminal to authorize the application.
- Once authorized, `strava_token.json` will store your access token for future use.
- The program will then give you feedback on the retrieving of your activites. This might take a while depending on the amount of activities.
- Finally, the program should generate the map, in the form of an html file, and open it in your default browser.

## Configuration
- `strava_credentials.json`: Stores your Strava API credentials. You need to configure this.
- `strava_token.json`: Stores the access and refresh tokens. This file will automatically be created after you have run the program.

## Requirements
This project requires Flask, folium, polyline and requests.

These, with their correct versions, can be installed using:
`pip install -r requirements.txt`

Of course, you also need to [create a Strava app](#configure-strava-api-access).