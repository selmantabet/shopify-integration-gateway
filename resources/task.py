from flask_restful import Resource
from env.constants_prod import SHOPIFY_API_VERSION, FLEET_MANAGEMENT_URI_PROD, FLEET_AUTH_TOKEN_PROD
from utils.hmac_auth import hmac_authenticate
from utils.helper_functions import generate_task_payload
from utils.rest_functions import create_task
import json


class Task(Resource):
    """
    The Task resource: Creates tasks upon receiving fulfillment webhooks.
    """

    def get(self):  # Get all tasks
        return "This resource only supports POST requests.", 405

    def post(self):  # Create a new task
        import os
        verbose = (os.getenv('VERBOSE', 'False') == 'True')
        # Parsing headers...
        from flask import request
        hmac_hash = request.headers.get("x-shopify-hmac-sha256")
        merchant_url_noscheme = request.headers.get("x-shopify-shop-domain")
        merchant_name = merchant_url_noscheme.split(
            ".")[0]  # https://{merchant_name}.myshopify.com
        fulfillment_id_header = request.headers.get("x-shopify-fulfillment-id")
        shopify_api_version = request.headers.get("x-shopify-api-version")

        if verbose:
            print("Headers parsed:")
            print("x-shopify-hmac-sha256 : ", hmac_hash)
            print("x-shopify-shop-domain : ", merchant_url_noscheme)
            print("Merchant name parsed : ", merchant_name)
            print("x-shopify-fulfillment-id : ", fulfillment_id_header)
            print("x-shopify-api-version : ", shopify_api_version)

        if (shopify_api_version != SHOPIFY_API_VERSION):
            print(
                "WARNING: SHOPIFY API VERSION HAS CHANGED. PLEASE UPDATE GATEWAY ACCORDINGLY.")
        request_body = request.get_data()
        if not hmac_authenticate(hmac_hash, merchant_name, request_body):
            return "Failed Authentication. Invalid HMAC.", 403
        if verbose:
            print("HMAC Authentication Successful.")
        from app import TenantTable
        company_record = TenantTable.query.filter(
            TenantTable.company_name == merchant_name).first()

        merchant_url = company_record.url
        merchant_token = company_record.merchant_token

        fulfillment_payload = json.loads(request_body)
        # THIS MUST ALWAYS PASS. Since HMAC passed, request integrity should be fine.
        assert(fulfillment_payload["id"] == fulfillment_id_header,
               "Fatal error: Fulfillment ID Header not equal to body fulfillment ID.")

        # merchant_token = MERCHANT_TOKEN  # ONLY FOR TESTING
        task_payload = generate_task_payload(
            merchant_url, merchant_token, fulfillment_payload)
        if verbose:
            print("Task Payload generated: ", task_payload)
        creation_response = create_task(
            FLEET_MANAGEMENT_URI_PROD, FLEET_AUTH_TOKEN_PROD, task_payload)
        from requests import JSONDecodeError
        try:
            creation_response_json = creation_response.json()
        except JSONDecodeError:
            return {"errors": "Task Creation JSON could not be decoded."}, 500
        except:
            return {"errors": "Something went wrong with task creation. Try again later."}, 500
        if verbose:
            print("Creation Response JSON: ", creation_response_json)
        return creation_response_json, 200

    def put(self):
        return "This resource only supports POST requests.", 405

    def delete(self):
        return "This resource only supports POST requests.", 405
