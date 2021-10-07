# salesforce marketing cloud API (sfmc)

# Libraries
import json
from datetime import datetime
import requests
import sys
from math import floor
from time import time
import itertools
import sfmc_api_auth


# Retrieve login parameters from config file
with open('/Users/quentinbracq/Desktop/pycharmprojects/sfmc-api-python/config.json') as credentials:
    credentials = json.load(credentials)

client_id = credentials["client_id"]
client_secret = credentials["client_secret"]
data_extension = credentials["data_extension"]
# Create DE in sfmc - External Key useful to send data via API call
# https://help.salesforce.com/s/articleView?id=sf.mc_es_create_data_extension_classic.htm&type=5

# The Salesforce Marketing Cloud REST API has a hard limit of 5MB per request,
# which means we’ll need to ensure our payloads don’t exceed this limit.
# We’ll use the sys.getsizeof() method to approximate the total size of the data we want to import
# and then batch that into chunks of less than 5MBs.


# Prepare data
data = [
    {'email_address': 'omsg813@live.fr',
     'contact_name': 'Bob',
     'contact_surname': 'Jean',
     'phone_number': ''
     }
]


# Functions: Import Data
def datetime_converter(value: datetime) -> str:
    if isinstance(value, datetime):
        return value.__str__()


def get_batch_size(record: dict) -> int:
    batch = json.dumps({'items': record}, default=datetime_converter)
    return floor(4000 / (sys.getsizeof(batch) / 1024))


def import_data(client_id, client_secret, data_extension, data):
    access_token, expires_in = sfmc_api_auth.generate_access_token(client_id, client_secret)
    subdomain = 'mc42bdlx7mz5h4np2xxvhsb4scvq'
    rest_url = f'https://{subdomain}.rest.marketingcloudapis.com'
    headers = {'authorization': f'Bearer {access_token}'}

    batch_size = get_batch_size(data[0])
    for batch in range(0, len(data), batch_size):
        if expires_in < time() + 60:
            access_token, expires_in = sfmc_api_auth.generate_access_token(client_id, client_secret)
        batch_data = data[batch:batch + batch_size]
        insert_request = requests.post(
            url=f'{rest_url}/data/v1/async/dataextensions/key:{data_extension}/rows',
            data=json.dumps({'items': batch_data}, default=datetime_converter),
            headers=headers
        )

        if insert_request.status_code not in (200, 202):
            raise Exception(f'Insertion failed with message: {insert_request.json()}')
    insert_request.close()


if __name__ == '__main__':
    import_data(client_id, client_secret, data_extension, data)
