# salesforce marketing cloud API (sfmc)

# Create New Package API
# https://medium.com/swlh/how-to-import-data-to-salesforce-marketing-cloud-exacttarget-using-python-rest-api-1302a26f89c0

# Libraries
import json
import requests
from time import time


# Function: Fetch Access Token
def generate_access_token(client_id: str, client_secret: str) -> str:
    subdomain = 'mc42bdlx7mz5h4np2xxvhsb4scvq'
    auth_base_url = f'https://{subdomain}.auth.marketingcloudapis.com/v2/token'
    headers = {'content-type': 'application/json'}
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    authentication_response = requests.post(
        url=auth_base_url, data=json.dumps(payload), headers=headers
    ).json()

    if 'access_token' not in authentication_response:
        raise Exception(
            f'Unable to validate (ClientID/ClientSecret): {repr(authentication_response)}'
        )
    access_token = authentication_response['access_token']
    expires_in = time() + authentication_response['expires_in']

    return access_token, expires_in
