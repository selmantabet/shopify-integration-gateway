"""
Integration Gateway Test file.

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
The earliest test file, used to re-familiarize myself with REST functions
"""


import http.client
import requests
import json

from constants import FLEET_AUTH_TOKEN, FLEET_MANAGEMENT_URI, MERCHANT_TOKEN, MERCHANT_URI


shop_auth_headers = {"X-Shopify-Access-Token": MERCHANT_TOKEN}

fleet_auth_header = {"Authorization": "Bearer " + FLEET_AUTH_TOKEN}


def get_products():
    endpoint = "products.json"
    r = requests.get(MERCHANT_URI + endpoint, headers=shop_auth_headers)
    return r.json()


def get_orders():
    endpoint = "orders.json?status=any"
    r = requests.get(MERCHANT_URI + endpoint, headers=shop_auth_headers)
    return r.json()


def create_orders_on_merchant():
    endpoint = "orders.json"
    payload = {
        "order": {
            "financial_status": "pending",
            "line_items": [{"variant_id": 42957710098685, "quantity": 10}, {"variant_id": 42957710065917, "quantity": 30}],
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
                "latitude": 25.3140683,
                "longitude": 51.491176,
                "country_code": "QA"
            }
        }
    }
    r = requests.post(MERCHANT_URI + endpoint,
                      headers=shop_auth_headers, json=payload)
    return r.json()


def update_order_on_merchant(order_id):
    endpoint = f"orders/{order_id}.json"
    payload = {
        "order": {
            "id": order_id,
            "financial_status": "paid"
        }
    }
    r = requests.put(MERCHANT_URI + endpoint,
                     headers=shop_auth_headers, json=payload)
    return r.json()


def create_tasks():
    endpoint = "tasks/create"
    payload = {
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
    r = requests.post(FLEET_MANAGEMENT_URI + endpoint,
                      headers=fleet_auth_header)
    return r


def create_task_from_callback(webhook_dict):
    """
    "transportTypeId" : could we determine this instead?
    "amountToBeCollected" : webhook_dict["total_outstanding"]
    "taskItems" : {
        "name" : webhook_dict["line_items"][i]["name"]
        "quantity" : webhook_dict["line_items"][i]["quantity"]
        "price" : webhook_dict["line_items"][i]["price"]
        "notes" : 
        "imageUrl" : 
    }
    "pickupByUtc" : 
    "deliverByUtc" : 
    "pickup" : {
        "Address" : 
        "Name" : 
        "PhoneNumber" : 
        "Latitude" : 
        "Longitude" : 
        }
    "delivery" : {
        "Address" : webhook_dict["shipping_address"]["address1"] + "\n" + webhook_dict["shipping_address"]["address2"]
        "Name" : webhook_dict["shipping_address"]["name"]
        "PhoneNumber" : webhook_dict["phone"]
        "Latitude" : 
        "Longitude" : 
        }
    "priority" : 5
    "canGroupTask" : true
    "pickupLocationTypeId" : 2
    "deliveryLocationTypeId" : 2
    "notes" : webhook_dict["notes"]
    "clientGeneratedId" : webhook_dict["id"]
    """
    endpoint = "tasks/create"
    payload = {
        "transportTypeId": 1,
        "amountToBeCollected": 0,
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
    r = requests.post(FLEET_MANAGEMENT_URI + endpoint,
                      headers=fleet_auth_header)
    return r
    return


def get_locations_from_FF():
    conn = http.client.HTTPSConnection(
        "integrationgateway-staging-lb.falconflex.ai")
    payload = ''

    conn.request("GET", "/api/v1/tasks/location-points",
                 payload, fleet_auth_header)
    res = conn.getresponse()
    data = res.read()
    json_out = json.loads(data.decode("utf-8"))
    # order_id = json_out["order"]["id"]
    # with open(f"order-confirmation-{order_id}.json", 'w', encoding='utf-8') as f:
    #     json.dump(json_out, f, ensure_ascii=False, indent=4)
    return json_out


def get_locations_from_FF_requests():
    endpoint = "tasks/location-points"
    r = requests.get(FLEET_MANAGEMENT_URI + endpoint,
                     headers=fleet_auth_header)
    return r.json()


# print(create_tasks())
# print(json.dumps(get_locations_from_FF(), indent=4, sort_keys=True))
# print(json.dumps(get_locations_from_FF_requests(), indent=4, sort_keys=True))
# print(json.dumps(get_products(), indent=4))
# print(get_orders())
print(json.dumps(create_orders_on_merchant(), indent=4))
# print(json.dumps(update_order_on_merchant(4756161954000), indent=4))
# print(get_orders())
