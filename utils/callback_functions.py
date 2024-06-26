"""
Integration Gateway FMS callback functions

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
This is where webhook calls for FMS are made.
"""

import requests


def subscribe_fleet(fleet_management_url, fleet_token, callback_url):
    callback_host = callback_url.replace("https://", "")
    callback_host = callback_host.strip("/")
    endpoint = "/api/v1/company/callbacks/create"

    fleet_auth_header = {"Authorization": "Bearer " + fleet_token}

    payloads = []
    for i in [2, 3, 4, 5, 9]:
        payload = {
            "url": callback_host + "/taskscallback",
            "callbackTriggerId": i,
            "scheme": "https"
        }
        payloads.append(payload)

    responses = []

    for i in range(len(payloads)):
        r = requests.post(fleet_management_url + endpoint,
                          headers=fleet_auth_header, json=payloads[i])
        responses.append(r.status_code)

    return responses


def unsubscribe_fleet(fleet_management_url, company_id, callback_id, fleet_token):

    endpoint = f"/api/v1/company/callbacks/remove?companyId={company_id}&callbackId={callback_id}"

    fleet_auth_header = {"Authorization": "Bearer " + fleet_token}

    r = requests.delete(fleet_management_url + endpoint,
                        headers=fleet_auth_header)
    return r
