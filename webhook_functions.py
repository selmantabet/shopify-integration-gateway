"""
Integration Gateway Merchant Webhook functions

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
This is where webhook calls for the merchant are made.
For now, FalconFlex webhook (or as we call it, callback) code are in the callback_functions.py file.
"""

import requests
from constants import *
import json


def subscribe_merchant(merchant_host, integration_endpoint, shop_token, category, trigger):
    endpoint = "/admin/api/2022-04/webhooks.json"
    integration_endpoint = integration_endpoint.strip("/")
    shop_auth_header = {"X-Shopify-Access-Token": shop_token}
    payload = {
        "webhook": {
            "topic": f"{category}/{trigger}",
            "address": integration_endpoint + "/tasks",
            "format": "json",
        }
    }
    r = requests.post(merchant_host + endpoint,
                      headers=shop_auth_header, json=payload)

    return r


def unsubscribe_merchant(merchant_host, webhook_id, shop_token):
    endpoint = f"/admin/api/2022-04/webhooks/{webhook_id}.json"
    shop_auth_header = {"X-Shopify-Access-Token": shop_token}

    r = requests.delete(merchant_host + endpoint,
                        headers=shop_auth_header)

    return r  # Should always be Response 200 OK


def retrieve_webhooks_merchant(merchant_host, shop_token):
    # Retrieve a list of webhooks from Shopify
    response = requests.get(merchant_host + "/admin/api/2022-04/webhooks.json",
                            headers={"X-Shopify-Access-Token": shop_token})
    return response.json()


def retrieve_events(merchant_host, shop_token, order_id, fulfillment_id):
    endpoint = f"/admin/api/2022-04/orders/{order_id}/fulfillments/{fulfillment_id}/events.json"
    response = requests.get(merchant_host + endpoint,
                            headers={"X-Shopify-Access-Token": shop_token})
    return response.json()


# print(json.dumps(retrieve_events(MERCHANT_HOST,
#       MERCHANT_TOKEN, 4782097891581, 4291636363517), indent=4))
# print(json.dumps(subscribe_merchant(MERCHANT_HOST, INTEGRATION_GATEWAY_TEST,
#       MERCHANT_TOKEN, "fulfillments", "create"), indent=4))
# print(unsubscribe_merchant(MERCHANT_HOST, 1144080564477, MERCHANT_TOKEN))
# print(retrieve_webhooks_merchant(MERCHANT_HOST, MERCHANT_TOKEN))
