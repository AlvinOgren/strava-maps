import json
import folium
from polyline import decode
import requests

def fetch_activities(access_token):
    """Fetch Strava activities using the access token."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://www.strava.com/api/v3/athlete/activities"
    activities = []

    page = 1
    while True:
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            raise Exception(f"Error fetching activities: {response.json()}")
        
        data = response.json()
        if not data:
            break  # No more activities
        
        activities.extend(data)
        page += 1

    return activities

def generate_map(access_token):
    """Generate a map using Strava activities and save it to an HTML file."""
    activities = fetch_activities(access_token)

    # Decode polylines from activities
    rides = [
        {"name": act["name"], "coordinates": decode(act["map"]["summary_polyline"])}
        for act in activities if act["map"]["summary_polyline"]
    ]

    # Create a base map (centered arbitrarily; adjust as needed)
    m = folium.Map(location=[58.4108, 15.6214], zoom_start=12)

    # Add polylines and markers
    for ride in rides:
        folium.PolyLine(ride["coordinates"], color="blue", weight=3, opacity=0.7).add_to(m)
        folium.Marker(location=ride["coordinates"][0], popup=ride["name"]).add_to(m)

    # Save map to an HTML file
    map_path = "rides_map.html"
    m.save(map_path)
    return map_path