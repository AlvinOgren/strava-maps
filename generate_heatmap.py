import json
import folium
from polyline import decode

# Load saved activities from Strava
with open("strava_activities.json") as f:
    activities = json.load(f)

# Extract ride details: name, polyline, and Strava activity ID
ride_data = []
for activity in activities:
    # Only include activities with valid summary_polyline data
    if 'map' in activity and activity['map']['summary_polyline']:
        ride_data.append({
            "name": activity['name'],
            "polyline": activity['map']['summary_polyline'],
            "id": activity['id']  # Strava ride ID
        })

# Decode polylines to GPS coordinates
rides = []
for r in ride_data:
    try:
        coordinates = decode(r["polyline"])
        rides.append({
            "name": r["name"],
            "coordinates": coordinates,
            "id": r["id"]
        })
    except Exception as e:
        print(f"Error decoding polyline for ride '{r['name']}': {e}")

# Create a base map centered on Linköping, Sweden
m = folium.Map(location=[58.4108, 15.6214], zoom_start=12)

# Add each ride as a polyline and a marker at its starting point
for ride in rides:
    # Add polyline for the ride path
    if ride["coordinates"]:  # Ensure coordinates are not empty
        folium.PolyLine(
            ride["coordinates"],  # GPS coordinates for the ride
            color="blue",         # Line color
            weight=3,             # Line thickness
            opacity=0.7           # Line transparency
        ).add_to(m)
    
    # Add a marker at the starting point of the ride with a link to Strava
    if ride["coordinates"]:  # Ensure coordinates are not empty
        start_point = ride["coordinates"][0]  # First coordinate of the ride
        ride_url = f"https://www.strava.com/activities/{ride['id']}"  # Strava activity link
        popup_html = f"<a href='{ride_url}' target='_blank'>{ride['name']}</a>"  # HTML link
        
        folium.Marker(
            location=start_point,
            popup=popup_html,  # Popup with clickable link
            icon=folium.Icon(color="red", icon="info-sign")  # Optional: Customize marker style
        ).add_to(m)

# Save the map to an HTML file
m.save("rides_polyline_with_links_map.html")
print("Map with polylines and linked ride pins saved to 'rides_polyline_with_links_map.html'.")
