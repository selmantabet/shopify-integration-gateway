"""
Integration Gateway Test file.

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Random tests with the Flask server has been conducted here.
"""
from constants import *
import requests

from Junk.webhook_functions_old import *
from callback_functions import *

BASE = "http://localhost:5000/"

new_tenant_data = {
    "merchant_host": MERCHANT_HOST,
    "shop_token": MERCHANT_TOKEN,
    "fleet_host": FLEET_MANAGEMENT_URI,
    "fleet_token": FLEET_AUTH_TOKEN,
    "company_id": COMPANY_ID_TEST
}


def test_webhook_creation():
    # Create Webhook for order cancelation on Shopify
    print(subscribe_order_created(MERCHANT_HOST, INTEGRATION_GATEWAY_TEST,
                                  MERCHANT_TOKEN, COMPANY_ID_TEST, FLEET_AUTH_TOKEN))


def test_callback_creation():
    # Create callback on FalconFlex
    print(subscribe_fleet_updates(FLEET_MANAGEMENT_URI,
                                  COMPANY_ID_TEST, FLEET_AUTH_TOKEN, MERCHANT_HOST, MERCHANT_TOKEN))


def test_tenant_creation():
    # Launch TenantCreation routine
    response = requests.post(BASE + "tenants", new_tenant_data)
    print("Response: ", response)
    print("Response JSON: ", response.json())


def remove_webhook(webhook_id):
    # Remove webhook from Shopify
    r = unsubscribe_order_paid(MERCHANT_HOST, webhook_id, MERCHANT_TOKEN)
    print(r)
    print(r.json())


def retrieve_callbacks():
    # Retrieve a list of all callbacks from FalconFlex
    endpoint = f"Company?id={COMPANY_ID_TEST}"
    print("Endpoint: ", endpoint)
    fleet_auth_header = {"Authorization": "Bearer " + FLEET_AUTH_TOKEN}
    print("URL: ", FLEET_MANAGEMENT_URI + endpoint)
    res = requests.get(FLEET_MANAGEMENT_URI + endpoint,
                       headers=fleet_auth_header)
    print(res.json())


new_order_data = {
    "order": {
        "line_items": [{"variant_id": 42737566580944, "quantity": 10}],
        "email": "selman.t@snoonu.com",
        "shipping_address": {
            "name": "Selmane Tabet",
            "first_name": "Selman",
            "last_name": "Tabet",
            "address1": "Building 41, Street 312, Zone 69",
            "address2": "Apartment C-208, AlAsmakh Residency",
            "phone": "974-3369-3992",
            "city": "Doha",
            "province": "Ad Dawhah",
            "country": "Qatar",
            "latitude": "25.3140683",
            "longitude": "51.491176",
            "country_code": "QA"
        }
    }
}

# This should trigger a callback from Shopify to the webhook


def create_orders_on_merchant():
    endpoint = "orders.json"
    shop_auth_headers = {"X-Shopify-Access-Token": MERCHANT_TOKEN}
    r = requests.post(MERCHANT_URI + endpoint,
                      headers=shop_auth_headers, json=new_order_data)

    print(r.json())


task_payload = {
    "transportTypeId": 1,
    "deliveryFee": 0,
    "pickupByUtc": "2021-11-22T11:53",
    "deliverByUtc": "2021-11-23T15:53",
    "notes": "Pls pickup",
    "priority": 1,
    "canGroupTask": True,
    "taskItems": [
        {
            "name": "TestItem",
            "quantity": 10,
            "price": 1,
            "notes": "hey there test notes"
        }
    ],
    "pickup": {
        "Address": "Al Nasr Tower A",
        "Name": "Zaryab",
        "PhoneNumber": "090078601",
        "Latitude": 25.01,
        "Longitude": 51.01
    },
    "delivery": {
        "Address": "Al Maha Towers",
        "Name": "Hassan Nadeem",
        "PhoneNumber": "0900786101",
        "Latitude": 24.01,
        "Longitude": 51.01
    },
    "paymentStatusId": 3,
    "clientGeneratedId": "TestingOrder6"
}

fulfillment_creation_payload = {
    "fulfillment": {
        "tracking_number": "FF0123",
        "tracking_urls": ["https://snoonu.com/"],
        "line_items": [
            {
                "id": 42737566580944,
                "quantity": 5
            }
        ]
    }
}
