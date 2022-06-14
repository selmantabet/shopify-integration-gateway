"""
Integration Gateway REST functions

Developed by Selman Tabet @ https://selman.io/
"""

import requests
from constants import *


def create_task(fleet_management_url, fleet_token, task_payload):
    endpoint = "/api/v1/tasks/create"
    fleet_auth_header = {"Authorization": "Bearer " + fleet_token}
    r = requests.post(fleet_management_url + endpoint,
                      headers=fleet_auth_header, json=task_payload)
    return r.json()


def send_status_update(merchant_host, shop_token, order_id, fulfillment_id, status):
    endpoint = f"/admin/api/2022-04/orders/{order_id}/fulfillments/{fulfillment_id}/events.json"
    shop_auth_header = {"X-Shopify-Access-Token": shop_token}
    update_payload = {
        "event": {
            "status": status
        }
    }
    r = requests.post(merchant_host + endpoint,
                      headers=shop_auth_header, json=update_payload)

    return r.json()


def get_fulfillment_events(merchant_host, shop_token, order_id, fulfillment_id):
    endpoint = f"/admin/api/2022-04/orders/{order_id}/fulfillments/{fulfillment_id}/events.json"
    shop_auth_header = {"X-Shopify-Access-Token": shop_token}
    r = requests.get(merchant_host + endpoint,
                     headers=shop_auth_header)

    return r.json()


# print(get_fulfillment_events(MERCHANT_HOST,
#       MERCHANT_TOKEN, 4756158578896, 4223330189520))
