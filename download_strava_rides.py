import requests
import json

# Your Strava credentials
client_id = "52650"
client_secret = "a0cdf2f362cdf59d86baf2e13d75cb07ae25c0ea"
redirect_uri = "http://localhost"
auth_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=activity:read_all"

print(f"Authorize your app by visiting this URL:\n{auth_url}")

# Use the returned code from Strava
authorization_code = input("Enter the code from Strava: ")

# Exchange the code for an access token
response = requests.post("https://www.strava.com/oauth/token", data={
    'client_id': client_id,
    'client_secret': client_secret,
    'code': authorization_code,
    'grant_type': 'authorization_code'
})
access_token = response.json()['access_token']

# Fetch activities with pagination
activities = []
page = 1  # Start with the first page
per_page = 100  # Maximum allowed per request
while True:
    print(f"Fetching page {page}...")
    activities_url = f"https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page": page, "per_page": per_page}
    response = requests.get(activities_url, headers=headers, params=params)
    data = response.json()
    
    # Break the loop if no more activities are returned
    if not data:
        break
    
    activities.extend(data)  # Add the fetched activities to the list
    page += 1  # Move to the next page

# Save all activities
with open("strava_activities.json", "w") as f:
    json.dump(activities, f)

print(f"Fetched {len(activities)} activities. Saved to 'strava_activities.json'.")
