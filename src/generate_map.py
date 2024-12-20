import json
import folium
from polyline import decode
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "rides_map.html")

def fetch_activities(access_token):
    """Fetch all activities of the authenticated user from the Strava API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://www.strava.com/api/v3/athlete/activities"
    activities = []

    page = 1
    while True:
        print("Fetching page:", page)
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            raise Exception(f"Error fetching activities: {response.json()}")
        
        data = response.json()
        if not data:
            break
        activities.extend(data)
        page += 1

    return activities

def generate_map(access_token, map_type="polyline"):
    """Generate an interactive map of Strava activities based on the specified map type."""
    activities = fetch_activities(access_token)
    m = folium.Map(location=[58.4108, 15.6214], zoom_start=12)

    if map_type == "heatmap": # not fully finished
        from folium.plugins import HeatMap
        all_coords = [
            coord
            for act in activities if "summary_polyline" in act["map"] and act["map"]["summary_polyline"]
            for coord in decode(act["map"]["summary_polyline"])
        ]
        HeatMap(all_coords, radius=5, blur=2).add_to(m)

    elif map_type == "polyline":
        rides = [
            {
                "name": act["name"],
                "id": act["id"],  # Include activity ID
                "coordinates": decode(act["map"]["summary_polyline"]),
            }
            for act in activities if "summary_polyline" in act["map"] and act["map"]["summary_polyline"]
        ]
        for ride in rides:
            # Construct Strava activity link
            activity_url = f"https://www.strava.com/activities/{ride['id']}"
            popup_html = f"<a href='{activity_url}' target='_blank'>{ride['name']}</a>"

            # Add the PolyLine with a popup
            folium.PolyLine(
                ride["coordinates"], 
                color="blue", 
                weight=3, 
                opacity=0.7, 
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(m)

            # Optionally add a marker at the start
            folium.Marker(
                location=ride["coordinates"][0],
                popup=folium.Popup(popup_html, max_width=300),
            ).add_to(m)

    m.save(OUTPUT_PATH)
    return OUTPUT_PATH