from constants import MERCHANT_HOST, MERCHANT_TOKEN
from helper_functions import generate_task_payload
from rest_functions import *
from constants import *
import json

# time_buffer = timedelta(minutes=1)
# today_dt = datetime.utcnow()
# today_dt_fixed = (today_dt + time_buffer).isoformat()

json_in = '{"id":4274928910589,"order_id":4782097891581,"status":"success","created_at":"2022-06-05T17:12:43+03:00","service":"manual","updated_at":"2022-06-05T17:12:43+03:00","tracking_company":null,"shipment_status":null,"location_id":69392335101,"origin_address":null,"email":"selman.t@snoonu.com","destination":{"first_name":"Selmane","address1":"Building 41, Street 312, Zone 69","phone":"974-3369-3992","city":"Doha","zip":null,"province":"Ad Dawhah","country":"Qatar","last_name":"Tabet","address2":"Apartment C-208, AlAsmakh Residency","company":null,"latitude":25.2676538,"longitude":51.5357698,"name":"Selmane Tabet","country_code":"QA","province_code":null},"line_items":[{"id":12205295993085,"variant_id":42957710098685,"title":"Test Product 2","quantity":1,"sku":"","variant_title":"Premium Latex \/ Oriental","vendor":"chaoscodes","fulfillment_service":"manual","product_id":7723383914749,"requires_shipping":true,"taxable":true,"gift_card":false,"name":"Test Product 2 - Premium Latex \/ Oriental","variant_inventory_management":"shopify","properties":[],"product_exists":true,"fulfillable_quantity":9,"grams":1000,"price":"200.00","total_discount":"0.00","fulfillment_status":"partial","price_set":{"shop_money":{"amount":"200.00","currency_code":"SAR"},"presentment_money":{"amount":"200.00","currency_code":"SAR"}},"total_discount_set":{"shop_money":{"amount":"0.00","currency_code":"SAR"},"presentment_money":{"amount":"0.00","currency_code":"SAR"}},"discount_allocations":[],"duties":[],"admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/12205295993085","tax_lines":[]}],"tracking_number":null,"tracking_numbers":[],"tracking_url":null,"tracking_urls":[],"receipt":{},"name":"#1005.1","admin_graphql_api_id":"gid:\/\/shopify\/Fulfillment\/4274928910589"}'
fulfillment_payload = {
    "id": 4223208325328,
    "order_id": 4756185153744,
    "status": "success",
    "created_at": "2022-06-02T03:43:37+03:00",
    "service": "manual",
    "updated_at": "2022-06-06T03:43:37+03:00",
    "tracking_company": None,
    "shipment_status": None,
    "location_id": 69392335101,
    "origin_address": None,
    "email": "selman.t@snoonu.com",
    "destination": {
        "first_name": "Selmane",
        "address1": "Building 41,Street 312, Zone 69",
        "phone": "974-3369-3992",
        "city": "Doha",
        "zip": None,
        "province": "Ad Dawhah",
        "country": "Qatar",
        "last_name": "Tabet",
        "address2": "Apartment C-208, AlAsmakh Residency",
        "company": None,
        "latitude": 25.2676538,
        "longitude": 51.5357698,
        "name": "Selmane Tabet",
        "country_code": "QA",
        "province_code": None},
    "line_items": [
        {
            "id": 12441661833424,
            "variant_id": 42737566580944,
            "title": "TestProduct2",
            "quantity": 1,
            "sku": "TEST2",
            "variant_title": None,
            "vendor": "falconflex-test",
            "fulfillment_service": "manual",
            "product_id": 7702296953040,
            "requires_shipping": True,
            "taxable": False,
            "gift_card": False,
            "name": "TestProduct2",
            "variant_inventory_management": "shopify",
            "properties": [],
            "product_exists":True,
            "fulfillable_quantity":6,
            "grams":6900,
            "price":"44.00",
            "total_discount":"0.00",
            "fulfillment_status":"partial",
            "price_set":{
                    "shop_money": {
                        "amount": "44.00",
                        "currency_code": "QAR"
                    },
                "presentment_money": {
                        "amount": "44.00",
                        "currency_code": "QAR"
                }
            },
            "total_discount_set": {
                "shop_money": {
                    "amount": "0.00",
                    "currency_code": "QAR"
                },
                "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "QAR"
                }
            },
            "discount_allocations": [],
            "duties":[],
            "admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/12441661833424",
            "tax_lines":[]}],
    "tracking_number": None,
    "tracking_numbers": [],
    "tracking_url": None,
    "tracking_urls": [],
    "receipt": {},
    "name": "#1009.2",
    "admin_graphql_api_id": "gid:\/\/shopify\/Fulfillment\/4223208325328"
}

fulfillment_payload = json.loads(json_in)

payload = generate_task_payload(
    MERCHANT_HOST, MERCHANT_TOKEN, fulfillment_payload)

print(json.dumps(create_task(FLEET_MANAGEMENT_URI,
                             FLEET_AUTH_TOKEN, payload), indent=4))
