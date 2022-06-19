from flask_restful import Resource

from utils.helper_functions import clean_host_url
from utils.status_mapper import mapping_dict
from utils.rest_functions import send_status_update


class Task_Update(Resource):
    def get(self):
        return "This resource only supports POST requests.", 405

    def post(self):
        from flask import request
        import os
        verbose = (os.getenv('VERBOSE', 'False') == 'True')
        try:
            task_update_payload_raw = request.get_json()
        except JSONDecodeError:
            return {"errors": "Task Update Payload JSON could not be decoded."}, 400
        except:
            return {"errors": "Something went wrong with parsing incoming data."}, 400
        task_update_payload = task_update_payload_raw["Data"]  # Cleaned
        task_update_metafields = task_update_payload["MetaDataFields"]
        order_id = task_update_payload["ClientGeneratedId"]

        # Check this once metadata structure is finalized.
        for i in task_update_metafields:
            if i["Key"] == "order_id":
                order_id = i["Value"]
            elif i["Key"] == "fulfillment_id":
                fulfillment_id = i["Value"]
            elif i["Key"] == "merchant_url":
                merchant_url = i["Value"]
            else:
                return {"errors": "Malformed metadata."}, 400
        from app import TenantTable
        merchant_url_cleaned = clean_host_url(merchant_url)
        company_record = TenantTable.query.filter(
            TenantTable.url == merchant_url_cleaned).first()
        shop_token = company_record.merchant_token
        status = task_update_payload["TaskStatus"]
        mapped_status = mapping_dict[status]
        update_response = send_status_update(
            merchant_url_cleaned, shop_token, order_id, fulfillment_id, mapped_status)
        from requests import JSONDecodeError
        try:
            update_response_json = update_response.json()
        except JSONDecodeError:
            return {"errors": "Update Response JSON could not be decoded."}, 400
        except:
            return {"errors": "Something went wrong with sending status update. Try again later."}, 400
        if verbose:
            print("Update Response JSON: ", update_response_json)
        return update_response_json, 200

    def put(self):
        return "This resource only supports POST requests.", 405

    def delete(self):
        return "This resource only supports POST requests.", 405
