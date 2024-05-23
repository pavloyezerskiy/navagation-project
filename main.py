import requests
import json
import time

def countdown(seconds):
    for i in range(int(seconds), 0, -1):
        print(f"Time remaining: {i} seconds")
        time.sleep(1)
    print("Make an action!")



# Coordinates of the starting and ending points
start_latitude = 49.813681750504834
start_longitude = 24.03426690116848
end_latitude = 49.85030652792358
end_longitude = 23.98223837000308

# OSRM API URL
osrm_url = f"http://router.project-osrm.org/route/v1/driving/"
request_url = f"{osrm_url}{start_longitude},{start_latitude};{end_longitude},{end_latitude}?steps=true&annotations=true"

# Make the request
response = requests.get(request_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    if len(data["routes"][0]["legs"]) > 0:
        total_meters_driven = 0
        total_seconds_driven = 0
        total_seconds = 0
        total_meters = 0


        legs = data["routes"][0]["legs"]
        for leg in legs:
            steps = leg['steps']
            for i in range(len(steps)):
                step = steps[i]
                distance = round(step['distance'],0)
                duration = round(step['duration'],0)
                total_seconds += duration
                total_meters += distance

        for leg in legs:

            steps = leg['steps']
            for i in range(len(steps)):
                step = steps[i]
                print("    ")


                # Action
                action = step['maneuver']['type']
                if action == "new name":
                    action = "go"
                action_type = step['maneuver']['modifier']

                if action != "end of road":
                    print(f"Action: {action} {action_type}")
                else:
                    print(f"Action: at the {action} go {action_type}")


                # Street
                street = step['name']
                print(f"To the street: {street}")

                # Extract distance and duration
                distance = round(step['distance'],0)
                duration = round(step['duration'],0)
                print(f"Drive for: {distance} meters")
                print(f"Time to next maneuver: {duration} seconds")

                #Next action
                if i+1 < len(steps):
                    action = steps[i+1]['maneuver']['type']
                    if action == "new name":
                        action = "go"
                    action_type = steps[i+1]['maneuver']['modifier']

                    if action != "end of road":
                        print(f"Next maneuver: {action} {action_type}")
                    else:
                        print(f"Next maneuver: at the {action} go {action_type}")
                    street = steps[i+1]['name']
                    print(f"To the street: {street}")

                print(f"{total_seconds - total_seconds_driven} seconds left till the end of the drive")
                print(f"{total_meters - total_meters_driven} meters left till the end of the drive")


                # Total left
                total_meters_driven += distance
                total_seconds_driven += duration


                print("______________")


                countdown(duration)

    else:
        print("No legs found in the data.")
        print("No route found.")
else:
    print("Failed to fetch route.")

