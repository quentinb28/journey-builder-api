# salesforce marketing cloud API (sfmc)

# Libraries
import requests
import json
from time import time
import datetime
from math import *
import sys
import sfmc_api_auth


# Retrieve login parameters from config file
with open("config.json") as credentials:
    credentials = json.load(credentials)

client_id = credentials["client_id"]
client_secret = credentials["client_secret"]

# journey name
journey_name = "New Journey - 6. oktober 2021 17.41"


if __name__ == "__main__":

    access_token, expires_in = sfmc_api_auth.generate_access_token(client_id, client_secret)
    subdomain = 'mc42bdlx7mz5h4np2xxvhsb4scvq'
    rest_url = f'https://{subdomain}.rest.marketingcloudapis.com'

    headers = {
        'authorization': f'Bearer {access_token}',
    }

    # GET JOURNEY DATA (check how to get a specific journey)

    r = requests.get(
        url='https://mc42bdlx7mz5h4np2xxvhsb4scvq.rest.marketingcloudapis.com/interaction/v1/interactions/',
        headers=headers
    )

    journey_data = json.loads(r.content)

    journey_id = [d["id"] for d in journey_data["items"] if d["name"] == journey_name][0]
    journey_key = [d["key"] for d in journey_data["items"] if d["name"] == journey_name][0]
    journey_modifiedDate = [d["modifiedDate"] for d in journey_data["items"] if d["name"] == journey_name][0]
    journey_version = [d["version"] for d in journey_data["items"] if d["name"] == journey_name][0]
    journey_workflowApiVersion = [d["workflowApiVersion"] for d in journey_data["items"] if d["name"] == journey_name][0]

    # GET ACTIVITIES DATA

    r = requests.get(
        url=f'{rest_url}/interaction/v1/interactions/{journey_id}',
        headers=headers
    )

    # Print response GET
    activities_data = json.loads(r.content)  # json.dumps(r, sort_keys=True, indent=4)
    # PathA actual value: r_clean["activities"][0]["outcomes"][0]["arguments"]["percentage"]
    # PathA string label: r_clean["activities"][0]["outcomes"][0]["metaData"]["label"]
    # PathB actual value: r_clean["activities"][0]["outcomes"][1]["arguments"]["percentage"]
    # PathB string label: r_clean["activities"][0]["outcomes"][1]["metaData"]["label"]

    # Set PathA to 70%
    activities_data["activities"][0]["outcomes"][0]["arguments"]["percentage"] = 70
    activities_data["activities"][0]["outcomes"][0]["metaData"]["label"] = "70%"

    # Set PathB to 30%
    activities_data["activities"][0]["outcomes"][1]["arguments"]["percentage"] = 30
    activities_data["activities"][0]["outcomes"][1]["metaData"]["label"] = "30%"

    # print(json.dumps(activities_data["activities"], sort_keys=True, indent=4))

    # ADD ACTIVITIES DATA TO JOURNEY DATA

    """updated_data = {
        "key": journey_key,
        "modifiedDate": journey_modifiedDate,
        "name": journey_name,
        "version": journey_version,
        "workflowApiVersion": journey_workflowApiVersion,
        "activities": activities_data["activities"]
    }"""
    updated_data = journey_data['items'][0]
    updated_data["activities"] = activities_data
    # print(updated_data)
    # print(json.dumps(updated_data, sort_keys=True, indent=4))

    # UPDATE JOURNEY DATA

    headers = {
        "authorization": f"Bearer {access_token}",
        # "content-type": "application/json"  # - 400 Bad Request
    }

    update_request = requests.put(
        url=f'{rest_url}/interaction/v1/interactions/',
        data=updated_data,
        headers=headers
    )  # Cannot update journey with status == 'Published' / sol: Pause then Update then Resume

    # "JSON Deserialization Exception: Location Unknown", "errorcode":10004

    # Print response PUT
    print(update_request.status_code, update_request. content)
