"""
Integration Gateway FalconFlex callback functions

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
This is where webhook calls for FalconFlex are made.

NONE OF THESE CALLBACKS HAVE BEEN TESTED. Awaiting API update so that I can test these.

So far, the calls here have resulted in 404 responses.
"""

import requests
from constants import *


def subscribe_fleet(fleet_management_url, fleet_token, callback_url):
    callback_host = callback_url.replace("https://", "")
    callback_host = callback_host.strip("/")
    endpoint = f"/api/v1/company/callbacks/create"
    print("Endpoint: ", endpoint)
    fleet_auth_header = {"Authorization": "Bearer " + fleet_token}
    print(fleet_auth_header)
    payloads = [
        {
            "url": callback_host + "/taskscallback",
            "callbackTriggerId": 2,
            "scheme": "https"
        },
        {
            "url": callback_host + "/taskscallback",
            "callbackTriggerId": 3,
            "scheme": "https"
        },
        {
            "url": callback_host + "/taskscallback",
            "callbackTriggerId": 4,
            "scheme": "https"
        },
        {
            "url": callback_host + "/taskscallback",
            "callbackTriggerId": 5,
            "scheme": "https"
        }
    ]
    responses = []
    # print(payload)
    # # print("Request body composed...")
    # print("Request URL: ", fleet_management_url + endpoint)
    for i in range(len(payloads)):
        r = requests.post(fleet_management_url + endpoint,
                          headers=fleet_auth_header, json=payloads[i])
        responses.append(r.status_code)

    return responses


def unsubscribe_fleet(fleet_management_url, company_id, callback_id, fleet_token):

    endpoint = f"/api/v1/company/callbacks/remove?companyId={company_id}&callbackId={callback_id}"
    print("Endpoint: ", endpoint)
    fleet_auth_header = {"Authorization": "Bearer " + fleet_token}
    print(fleet_auth_header)
    r = requests.delete(fleet_management_url + endpoint,
                        headers=fleet_auth_header)
    return r


# print(subscribe_fleet(FLEET_MANAGEMENT_URI, COMPANY_ID_TEST,
#       FLEET_AUTH_TOKEN, INTEGRATION_GATEWAY_TEST_NOSCHEME, MERCHANT_TOKEN))
