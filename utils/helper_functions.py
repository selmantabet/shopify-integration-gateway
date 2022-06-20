"""
Integration Gateway Helper functions

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
These functions serve as the logic behind the main Flask server script.
"""

import requests
from datetime import datetime, timedelta
# import json


def clean_host_url(url):
    url_cleaned = url.strip("./").replace(" ", "")
    return url_cleaned


def retrieve_merchant_name(url):
    url_cleaned = clean_host_url(url)
    url_cleaned = url_cleaned.replace("https://", "")
    merchant_name = url_cleaned.split(".")[0]
    return merchant_name


def payload_error_checker(payload):
    if "errors" in payload:
        return True
    if "error" in payload:
        return True


def generate_task_payload(merchant_host, shop_token, fulfillment_payload):
    """
    This function takes in the merchants domain and its corresponding token along with the merchant webhook's body
    and uses them to generate the JSON body that would be used in the HTTP request to be sent to FalconFlex.

    As such, it would be used in the create_task() routine defined in rest_functions.py, which is called in the Task resource.
    """
    if payload_error_checker(fulfillment_payload):
        return {"errors": "Bad Request from merchant."}

    # ONLY USE THIS PART IF SHOPIFY EVER ADDS THIS TO THEIR WEBHOOK.
    # FOR NOW, ALL ORDERS WILL BE ASSUMED TO BE INTERNATIONAL.

    # if fulfillment_payload["destination"]["country_code"] == "QA":
    #     delivery_address = {
    #         "Address": fulfillment_payload["destination"]["address1"] + "\n" + fulfillment_payload["destination"]["address2"],
    #         "Name": fulfillment_payload["shipping_address"]["name"],
    #         "PhoneNumber": fulfillment_payload["phone"],
    #         "ZoneNumber": fulfillment_payload["zone_number"],
    #         "StreetNumber": fulfillment_payload["street_number"],
    #         "BuildingNumber": fulfillment_payload["building_number"]
    #     }

    #     delivery_type = 3

    task_items = []
    # Iterate through every line item and append it as a task item
    for i in range(len(fulfillment_payload["line_items"])):
        item = {
            "name": fulfillment_payload["line_items"][i]["name"],
            "quantity": fulfillment_payload["line_items"][i]["quantity"],
            "price": fulfillment_payload["line_items"][i]["price"],
        }  # Webhooks do not include product images, but we can fetch them ourselves if need be.
        task_items.append(item)

    datesUtc = determine_dates()

    # Convert the provided location_id to the pickup address
    location_data_response = retrieve_fulfillment_location(
        merchant_host, shop_token, fulfillment_payload["location_id"])
    location_data = location_data_response["location"]  # Cleaned

    origin_phone = location_data["phone"].replace(" ", "")
    destination_phone = fulfillment_payload["destination"]["phone"].replace(
        " ", "")

    if origin_phone == "":
        origin_phone = "000000000"
    if destination_phone == "":
        destination_phone = "000000000"

    import os
    map_service_url = os.environ["MAP_SERVICE_URI"]
    map_service_secret = os.environ["MAP_SERVICE_SECRET"]
    from utils.map_service import get_coordinates
    pickup_address = str(
        location_data["address1"]) + " \n " + str(location_data["address2"])
    try:
        pickup_coordinates = get_coordinates(
            map_service_url, map_service_secret, pickup_address)
    except requests.RequestException as exc:
        print("Pickup coordinates parse failed.")
        print("Errors: ", exc)
        return {"Failed to parse coordinates from provided pickup address.", 500}
    destination_address = str(fulfillment_payload["destination"]["address1"]) + " \n " + str(
        fulfillment_payload["destination"]["address2"])
    destination_lat = fulfillment_payload["destination"]["latitude"]
    destination_long = fulfillment_payload["destination"]["longitude"]
    try:
        destination_latitude = float(destination_lat)
        destination_longitude = float(destination_long)
        destination_coordinates = (destination_latitude, destination_longitude)
    except ValueError:
        try:
            destination_coordinates = get_coordinates(
                map_service_url, map_service_secret, destination_address)
        except requests.RequestException as exc:
            print("Destination coordinates parse failed.")
            print("Errors: ", exc)
            return {"Failed to parse coordinates from provided destination address.", 500}

    task_payload = {
        "transportTypeId": 1,  # could we determine this instead?
        "amountToBeCollected": 0.0,  # Webhook does not include this.
        "taskItems": task_items,
        # We need to look more into the time values, but can't test until I manage to directly work with it in staging.
        "pickupByUtc": datesUtc[0],
        "deliverByUtc": datesUtc[1],
        "pickup": {
            # Enforce str type via typecast as sometimes Address2 is NoneType
            "Address": pickup_address,
            "Name": location_data["name"],
            "PhoneNumber": origin_phone,
            # Lat-Longs are not normally provided, you need to use the Google Maps API for this.
            "Latitude": pickup_coordinates[0],
            "Longitude": pickup_coordinates[1],
        },
        "delivery": {
            "Address": destination_address,
            "Name": fulfillment_payload["destination"]["name"],
            "PhoneNumber": destination_phone,
            # Lat-Longs are not provided, you need to use the Google Maps API for this.
            "Latitude": destination_coordinates[0],
            "Longitude": destination_coordinates[1]},
        # Someone should check the default values for the following two
        "priority": 5,
        "canGroupTask": True,
        "pickupLocationTypeId": 2,
        "deliveryLocationTypeId": 2,
        "userMetaDataDtos": generate_metadata(merchant_host, fulfillment_payload),
        "clientGeneratedId": fulfillment_payload["order_id"]
    }
    # print(task_payload["pickup"]["Address"], "\n\n",
    #       task_payload["delivery"]["Address"])
    return task_payload


def retrieve_fulfillment_location(merchant_host, shop_token, location_id):
    """
    The pickup location will always be the order's fulfillment center.
    The fulfillment center's location can only be retrieved via Shopify's 
    Locations API resource as the location data is not sent over the webhook.
    Only the location ID is sent in each webhook. We could, however, store 
    fulfillment location details (including lat-longs) on FalconFlex. Doing so would 
    require the task payload generator function to have its pickupLocationTypeId
    and deliverLocationTypeId fields re-evaluated to make use of this.
    """
    endpoint = f"/admin/api/2022-04/locations/{location_id}.json"
    shop_auth_header = {"X-Shopify-Access-Token": shop_token}
    r = requests.get(merchant_host + endpoint,
                     headers=shop_auth_header)
    if payload_error_checker(r.json()):
        print("Error condition...", r.json())
        return {"errors": "Bad Request from merchant."}
    return r.json()


def determine_dates():
    pickupByUtc_dt = datetime.utcnow()
    import os
    time_buffer = timedelta(minutes=int(os.getenv("TIME_BUFFER_MINUTES", 3)))
    verbose = (os.getenv('VERBOSE', 'False') == 'True')
    if verbose:
        print("Time Buffer Selected: ", time_buffer)
    pickupByUtc_dt = pickupByUtc_dt + time_buffer
    delivery_duration = timedelta(hours=1)
    deliverByUtc_dt = pickupByUtc_dt + delivery_duration
    pickupByUtc = pickupByUtc_dt.isoformat()
    deliverByUtc = deliverByUtc_dt.isoformat()
    return (pickupByUtc, deliverByUtc)


def generate_metadata(merchant_host, payload):
    output = [
        {"key": "order_id",
         "value": payload["order_id"]},
        {"key": "fulfillment_id",
         "value": payload["id"]},
        {"key": "merchant_url",
         "value": merchant_host}
    ]
    return output


# print(json.dumps(retrieve_fulfillment_location(
#     MERCHANT_HOST, MERCHANT_TOKEN, 69392335101), indent=4))
