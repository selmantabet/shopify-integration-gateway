"""
Bad tenant creation requests.

1 - Bad form structure
2 - Bad raw data
3 - Incorrect data in form.

"""


import json
import requests
from dotenv import load_dotenv
import os

cwd = os.getcwd()
env_path = os.path.join(cwd, "env", "vars.env")
print("cfg env path: ", env_path)
if (os.path.exists(env_path)):
    load_dotenv(dotenv_path=env_path)
    print("env vars initialized from unit test")


def setup_environment(integration_gateway):
    print("Setting up environment...")
    endpoint = "/tenants"
    payload = {
        "merchant_url": os.environ["MERCHANT_HOST"],
        "shop_token": os.environ["MERCHANT_TOKEN"],
        "shop_api_secret": os.environ["MERCHANT_SECRET"],
        "company_id": os.environ["COMPANY_ID_TEST"]
    }
    r = requests.post(integration_gateway + endpoint, data=payload)
    return r.json()


def reset_environment(integration_gateway):
    print("Resetting environment...")
    payload = {
        "merchant_url": "https://chaoscodes.myshopify.com"
    }
    r = requests.delete(integration_gateway + "/tenants", data=payload)
    return r.status_code


def bad_form_structure(integration_gateway):
    print("Testing bad tenant form structure...")
    endpoint = "/tenants"
    payload = {
        "merchant_url": os.environ["MERCHANT_HOST"],
        "shop_token": os.environ["MERCHANT_TOKEN"],
        "shop_api_secret": os.environ["MERCHANT_SECRET"]
    }
    r = requests.post(integration_gateway + endpoint, data=payload)
    return r.json()


def bad_shop_token(integration_gateway):
    print("Testing bad tenant token...")
    endpoint = "/tenants"
    payload = {
        "merchant_url": os.environ["MERCHANT_HOST"],
        "shop_token": "shpat_b59b4bc17c2bed5a53xsdf2",
        "shop_api_secret": os.environ["MERCHANT_SECRET"],
        "company_id": os.environ["COMPANY_ID_TEST"]
    }
    r = requests.post(integration_gateway + endpoint, data=payload)
    return r.json()


def url_no_schema(integration_gateway):
    print("Testing bad tenant url...")
    endpoint = "/tenants"
    payload = {
        "merchant_url": "chaoscodes.myshopify.com/",
        "shop_token": os.environ["MERCHANT_TOKEN"],
        "shop_api_secret": os.environ["MERCHANT_SECRET"],
        "company_id": os.environ["COMPANY_ID_TEST"]
    }
    r = requests.post(integration_gateway + endpoint, data=payload)
    return r.status_code


def corrupt_raw_data(integration_gateway):
    print("Testing bad request body...")
    endpoint = "/tenants"
    payload = "corrupted part"
    r = requests.post(integration_gateway + endpoint, data=payload)
    return r.json()


def bad_form_data(integration_gateway):
    print("Testing bad form entries...")
    endpoint = "/tenants"
    payload = {
        "merchant_url": "https://wRGWWGWRWGWRG",
        "shop_token": "DFDFDSFF334RR",
        "shop_api_secret": "ADCFSFDFSFFSDF",
        "company_id": "CDSVSFVG"
    }
    r = requests.post(integration_gateway + endpoint, data=payload)
    return r.status_code


def another_bad_form_data(integration_gateway):
    print("Testing even worse form entries...")
    endpoint = "/tenants"
    payload = {
        "merchant_url": "wRGWWGWRWGWRG",
        "shop_token": "DFDFDSFF334RR",
        "shop_api_secret": "ADCFSFDFSFFSDF",
        "company_id": "CDSVSFVG"
    }
    r = requests.post(integration_gateway + endpoint, data=payload)
    return r.status_code


"""
Bad task creation requests

1 - HMAC authentication failure.
2 - Incomplete LatLong entry.

"""


def bad_hmac(integration_gateway):
    print("Testing bad HMAC...")
    endpoint = "/tasks"
    body = '{"id":4291620110589,"order_id":4782097891581,"status":"success","created_at":"2022-06-12T12:52:51+03:00","service":"manual","updated_at":"2022-06-12T12:52:51+03:00","tracking_company":null,"shipment_status":null,"location_id":69392335101,"origin_address":null,"email":"selman.t@fms.com","destination":{"first_name":"Selmane","address1":"Building 41, Street 312, Zone 69","phone":"974-3369-3992","city":"Doha","zip":null,"province":"Ad Dawhah","country":"Qatar","last_name":"Tabet","address2":"Apartment C-208, AlAsmakh Residency","company":null,"latitude":25.2676538,"longitude":51.5357698,"name":"Selmane Tabet","country_code":"QA","province_code":null},"line_items":[{"id":12205295993085,"variant_id":42957710098685,"title":"Test Product 2","quantity":3,"sku":"","variant_title":"Premium Latex \/ Oriental","vendor":"chaoscodes","fulfillment_service":"manual","product_id":7723383914749,"requires_shipping":true,"taxable":true,"gift_card":false,"name":"Test Product 2 - Premium Latex \/ Oriental","variant_inventory_management":"shopify","properties":[],"product_exists":true,"fulfillable_quantity":5,"grams":1000,"price":"200.00","total_discount":"0.00","fulfillment_status":"partial","price_set":{"shop_money":{"amount":"200.00","currency_code":"SAR"},"presentment_money":{"amount":"200.00","currency_code":"SAR"}},"total_discount_set":{"shop_money":{"amount":"0.00","currency_code":"SAR"},"presentment_money":{"amount":"0.00","currency_code":"SAR"}},"discount_allocations":[],"duties":[],"admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/12205295993085","tax_lines":[]},{"id":12205296025853,"variant_id":42957710065917,"title":"Test Product 2","quantity":10,"sku":"","variant_title":"Premium Latex \/ Custom","vendor":"chaoscodes","fulfillment_service":"manual","product_id":7723383914749,"requires_shipping":true,"taxable":true,"gift_card":false,"name":"Test Product 2 - Premium Latex \/ Custom","variant_inventory_management":"shopify","properties":[],"product_exists":true,"fulfillable_quantity":17,"grams":1000,"price":"200.00","total_discount":"0.00","fulfillment_status":"partial","price_set":{"shop_money":{"amount":"200.00","currency_code":"SAR"},"presentment_money":{"amount":"200.00","currency_code":"SAR"}},"total_discount_set":{"shop_money":{"amount":"0.00","currency_code":"SAR"},"presentment_money":{"amount":"0.00","currency_code":"SAR"}},"discount_allocations":[],"duties":[],"admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/12205296025853","tax_lines":[]}],"tracking_number":null,"tracking_numbers":[],"tracking_url":null,"tracking_urls":[],"receipt":{},"name":"#1005.3","admin_graphql_api_id":"gid:\/\/shopify\/Fulfillment\/4291620110589"}'
    payload = json.loads(body)
    headers = {
        'connection': 'close',
        'x-shopify-webhook-id': 'd3a487dd-193e-4a09-9714-35e0d047ca91',
        'x-shopify-topic': 'fulfillments/create',
        'x-shopify-shop-domain': 'chaoscodes.myshopify.com',
        'x-shopify-hmac-sha256': 'DJrzJYGfxDvZAsi8oKesPJjcTBxKzh4naQL1GbBBT1M=',
        'x-shopify-fulfillment-id': '4291620110589',
        'x-shopify-api-version': '2022-04',
        'content-type': 'application/json',
        'accept-encoding': 'gzip;q=1.0,deflate;q=0.6,identity;q=0.3',
        'accept': '*/*',
        'content-length': '2668',
        'user-agent': 'Shopify-Captain-Hook',
        'host': 'webhook.site'
    }
    r = requests.post(integration_gateway + endpoint,
                      headers=headers, data=payload)
    return r.json()


def bad_fulfillment_id(integration_gateway):
    print("Testing mismatched fulfillment ID...")
    endpoint = "/tasks"
    body = '{"id":4291620110589,"order_id":4782097891581,"status":"success","created_at":"2022-06-12T12:52:51+03:00","service":"manual","updated_at":"2022-06-12T12:52:51+03:00","tracking_company":null,"shipment_status":null,"location_id":69392335101,"origin_address":null,"email":"selman.t@fms.com","destination":{"first_name":"Selmane","address1":"Building 41, Street 312, Zone 69","phone":"974-3369-3992","city":"Doha","zip":null,"province":"Ad Dawhah","country":"Qatar","last_name":"Tabet","address2":"Apartment C-208, AlAsmakh Residency","company":null,"latitude":25.2676538,"longitude":51.5357698,"name":"Selmane Tabet","country_code":"QA","province_code":null},"line_items":[{"id":12205295993085,"variant_id":42957710098685,"title":"Test Product 2","quantity":3,"sku":"","variant_title":"Premium Latex \/ Oriental","vendor":"chaoscodes","fulfillment_service":"manual","product_id":7723383914749,"requires_shipping":true,"taxable":true,"gift_card":false,"name":"Test Product 2 - Premium Latex \/ Oriental","variant_inventory_management":"shopify","properties":[],"product_exists":true,"fulfillable_quantity":5,"grams":1000,"price":"200.00","total_discount":"0.00","fulfillment_status":"partial","price_set":{"shop_money":{"amount":"200.00","currency_code":"SAR"},"presentment_money":{"amount":"200.00","currency_code":"SAR"}},"total_discount_set":{"shop_money":{"amount":"0.00","currency_code":"SAR"},"presentment_money":{"amount":"0.00","currency_code":"SAR"}},"discount_allocations":[],"duties":[],"admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/12205295993085","tax_lines":[]},{"id":12205296025853,"variant_id":42957710065917,"title":"Test Product 2","quantity":10,"sku":"","variant_title":"Premium Latex \/ Custom","vendor":"chaoscodes","fulfillment_service":"manual","product_id":7723383914749,"requires_shipping":true,"taxable":true,"gift_card":false,"name":"Test Product 2 - Premium Latex \/ Custom","variant_inventory_management":"shopify","properties":[],"product_exists":true,"fulfillable_quantity":17,"grams":1000,"price":"200.00","total_discount":"0.00","fulfillment_status":"partial","price_set":{"shop_money":{"amount":"200.00","currency_code":"SAR"},"presentment_money":{"amount":"200.00","currency_code":"SAR"}},"total_discount_set":{"shop_money":{"amount":"0.00","currency_code":"SAR"},"presentment_money":{"amount":"0.00","currency_code":"SAR"}},"discount_allocations":[],"duties":[],"admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/12205296025853","tax_lines":[]}],"tracking_number":null,"tracking_numbers":[],"tracking_url":null,"tracking_urls":[],"receipt":{},"name":"#1005.3","admin_graphql_api_id":"gid:\/\/shopify\/Fulfillment\/4291620110589"}'
    payload = json.loads(body)
    headers = {
        'connection': 'close',
        'x-shopify-webhook-id': 'd3a487dd-193e-4a09-9714-35e0d047ca91',
        'x-shopify-topic': 'fulfillments/create',
        'x-shopify-shop-domain': 'chaoscodes.myshopify.com',
        'x-shopify-hmac-sha256': 'DJrzJYGfxDvZAsi8oKesPJjcTBxKzh4naQL1GbBBT1M=',
        'x-shopify-fulfillment-id': '4291620110589234',
        'x-shopify-api-version': '2022-04',
        'content-type': 'application/json',
        'accept-encoding': 'gzip;q=1.0,deflate;q=0.6,identity;q=0.3',
        'accept': '*/*',
        'content-length': '2668',
        'user-agent': 'Shopify-Captain-Hook',
        'host': 'webhook.site'
    }
    r = requests.post(integration_gateway + endpoint,
                      headers=headers, data=payload)
    return r.json()


def no_latlongs(integration_gateway):
    print("Testing no lat-long payload...")
    endpoint = "/tasks"
    body = '{"id":4291620110589,"order_id":4782097891581,"status":"success","created_at":"2022-06-12T12:52:51+03:00","service":"manual","updated_at":"2022-06-12T12:52:51+03:00","tracking_company":null,"shipment_status":null,"location_id":69392335101,"origin_address":null,"email":"selman.t@fms.com","destination":{"first_name":"Selmane","address1":"Building 41, Street 312, Zone 69","phone":"974-3369-3992","city":"Doha","zip":null,"province":"Ad Dawhah","country":"Qatar","last_name":"Tabet","address2":"Apartment C-208, AlAsmakh Residency","company":null,"latitude":null,"longitude":null,"name":"Selmane Tabet","country_code":"QA","province_code":null},"line_items":[{"id":12205295993085,"variant_id":42957710098685,"title":"Test Product 2","quantity":3,"sku":"","variant_title":"Premium Latex \/ Oriental","vendor":"chaoscodes","fulfillment_service":"manual","product_id":7723383914749,"requires_shipping":true,"taxable":true,"gift_card":false,"name":"Test Product 2 - Premium Latex \/ Oriental","variant_inventory_management":"shopify","properties":[],"product_exists":true,"fulfillable_quantity":5,"grams":1000,"price":"200.00","total_discount":"0.00","fulfillment_status":"partial","price_set":{"shop_money":{"amount":"200.00","currency_code":"SAR"},"presentment_money":{"amount":"200.00","currency_code":"SAR"}},"total_discount_set":{"shop_money":{"amount":"0.00","currency_code":"SAR"},"presentment_money":{"amount":"0.00","currency_code":"SAR"}},"discount_allocations":[],"duties":[],"admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/12205295993085","tax_lines":[]},{"id":12205296025853,"variant_id":42957710065917,"title":"Test Product 2","quantity":10,"sku":"","variant_title":"Premium Latex \/ Custom","vendor":"chaoscodes","fulfillment_service":"manual","product_id":7723383914749,"requires_shipping":true,"taxable":true,"gift_card":false,"name":"Test Product 2 - Premium Latex \/ Custom","variant_inventory_management":"shopify","properties":[],"product_exists":true,"fulfillable_quantity":17,"grams":1000,"price":"200.00","total_discount":"0.00","fulfillment_status":"partial","price_set":{"shop_money":{"amount":"200.00","currency_code":"SAR"},"presentment_money":{"amount":"200.00","currency_code":"SAR"}},"total_discount_set":{"shop_money":{"amount":"0.00","currency_code":"SAR"},"presentment_money":{"amount":"0.00","currency_code":"SAR"}},"discount_allocations":[],"duties":[],"admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/12205296025853","tax_lines":[]}],"tracking_number":null,"tracking_numbers":[],"tracking_url":null,"tracking_urls":[],"receipt":{},"name":"#1005.3","admin_graphql_api_id":"gid:\/\/shopify\/Fulfillment\/4291620110589"}'
    payload = json.loads(body)
    headers = {
        'connection': 'close',
        'x-shopify-webhook-id': 'd3a487dd-193e-4a09-9714-35e0d047ca91',
        'x-shopify-topic': 'fulfillments/create',
        'x-shopify-shop-domain': 'chaoscodes.myshopify.com',
        'x-shopify-hmac-sha256': '6955f2ab1a939dd4689e0633fa934a0a',
        'x-shopify-fulfillment-id': '4291620110589',
        'x-shopify-api-version': '2022-04',
        'content-type': 'application/json',
        'accept-encoding': 'gzip;q=1.0,deflate;q=0.6,identity;q=0.3',
        'accept': '*/*',
        'content-length': '2668',
        'user-agent': 'Shopify-Captain-Hook',
        'host': 'webhook.site'
    }
    r = requests.post(integration_gateway + endpoint,
                      headers=headers, data=payload)
    return r.json()


"""
Bad status update payloads.

1 - Bad status update payload structures

"""


def bad_status_payload(integration_gateway):
    print("Testing bad update payload...")
    endpoint = "/taskscallback"
    body = '{"CallBackType":"taskcreated","Data":{"Id":"62a5c631df47f38d5c0c9d75","ShortId":"7XhnyTGf","ClientGeneratedId":"4782097891581","DeliveryFee":0.0,"CreatedAtUtc":"2022-06-12T10:55:45.5832974Z","UpdatedAtUtc":"2022-06-12T10:55:45.5832974Z","CreatedBy":"admin@fms.com","UpdatedBy":"admin@fms.com","PickupByUtc":"2022-06-12T11:00:46.766517","DeliverByUtc":"2022-06-12T12:00:46.766517","EstimatedPickupByUtc":null,"EstimatedDeliveryByUtc":null,"EstimatedDistanceRemainingToPickupKm":0.0,"EstimatedDistanceRemainingToDeliverKm":0.0,"EtaToCompletionMinFromUtcNow":0,"OwningCompanyName":"","OwningCompanyId":"620ac4fe812b6a4a8977e007","ExecutingCompanyId":"620ac4fe812b6a4a8977e007","PaymentStatus":"Paid","TaskStatus":"Unplanned","Pickup":{"Address":"12282 King Abdulaziz Road, Al Mouroj\n","Name":"12282 King Abdulaziz Road, Al Mouroj","Notes":null,"PhoneNumber":"+97433693992","Latitude":25.3138126,"Longitude":51.4408446},"Delivery":{"Address":"Building 41, Street 312, Zone 69\nApartment C-208, AlAsmakh Residency","Name":"Selmane Tabet","Notes":null,"PhoneNumber":"974-3369-3992","Latitude":25.2676538,"Longitude":51.5357698},"CollectionAmount":0.0,"TaskItems":[],"AgentTripDto":null,"AutoAssignmentDto":{"AutoAssignAllowed":false,"MaxRetryCount":10,"CurrentRetryCount":0,"InternalRetryCount":0,"RetryIntervalSec":10,"DidAutoAssign":false},"MetaDataFields":[{"Key":"order_id","Value":"4782097891581","ColorHex":"#5F94E4","MetaDataTypeId":2,"ClientViewAllowed":true,"MetaDataType":{"Name":"UserMetaDataType","Value":2}},{"Key":"fulfillment_id","Value":"4291636363517","ColorHex":"#5F94E4","MetaDataTypeId":2,"ClientViewAllowed":true,"MetaDataType":{"Name":"UserMetaDataType","Value":2}},{"Key":"merchant_url","Value":"https://chaoscodes.myshopify.com","ColorHex":"#5F94E4","MetaDataTypeId":2,"ClientViewAllowed":true,"MetaDataType":{"Name":"UserMetaDataType","Value":2}}],"TransportTypeId":1}}'
    payload = json.loads(body)

    r = requests.post(integration_gateway + endpoint, data=payload)
    return r.json()


if __name__ == "__main__":
    integration_gateway_test = "http://localhost:5000"
    reset_environment(integration_gateway_test)
    try:
        print("Commencing Tenant request tests...")

        print(bad_form_structure(integration_gateway_test))
        reset_environment(integration_gateway_test)
        print(bad_shop_token(integration_gateway_test))
        reset_environment(integration_gateway_test)
        print(url_no_schema(integration_gateway_test))
        reset_environment(integration_gateway_test)
        print(corrupt_raw_data(integration_gateway_test))
        reset_environment(integration_gateway_test)
        print(bad_form_data(integration_gateway_test))
        reset_environment(integration_gateway_test)
        print(another_bad_form_data(integration_gateway_test))
        reset_environment(integration_gateway_test)

        print("Commencing Task request tests...")
        setup_environment(integration_gateway_test)
        print(bad_hmac(integration_gateway_test))
        reset_environment(integration_gateway_test)
        setup_environment(integration_gateway_test)
        print(bad_fulfillment_id(integration_gateway_test))
        reset_environment(integration_gateway_test)
        setup_environment(integration_gateway_test)
        print(no_latlongs(integration_gateway_test))
        reset_environment(integration_gateway_test)

        print("Commencing Update request test...")
        setup_environment(integration_gateway_test)
        print(bad_status_payload(integration_gateway_test))
        reset_environment(integration_gateway_test)
    finally:
        reset_environment(integration_gateway_test)
