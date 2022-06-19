from flask_restful import Resource
# from env.constants_prod import INTEGRATION_GATEWAY
from utils.parsers import tenant_post_args
from utils.helper_functions import clean_host_url, retrieve_merchant_name
from utils.webhook_functions import subscribe_merchant

INTEGRATION_GATEWAY = "https://integration-gateway.azurewebsites.net"


class Tenant(Resource):
    """
    The Tenant resource: Simply deals with webhooks subscriptions upon info submission by an admin.

    FalconFlex callbacks are still not tested, need the right credentials for that.
    """

    def get(self):  # Get all tenant callbacks
        return "This resource only supports POST requests.", 405

    def post(self):  # Create new tenant
        from requests import JSONDecodeError
        import os

        verbose = (os.getenv('VERBOSE', 'False') == 'True')
        args = tenant_post_args.parse_args()
        fulfillments_callback_created = subscribe_merchant(
            clean_host_url(args["merchant_url"]), INTEGRATION_GATEWAY, args["shop_token"], "fulfillments", "create")
        try:
            fulfillments_callback_created_json = fulfillments_callback_created.json()
            webhook_id = fulfillments_callback_created_json["webhook"]["id"]
        except JSONDecodeError:
            return {"errors": "JSON could not be decoded."}, 400
        except KeyError:
            return {"errors": "Failure on webhook creation."}, 400
        except:
            return {"errors": "Something went wrong. Try again later."}, 500

        url_cleaned = clean_host_url(args["merchant_url"])
        from app import TenantTable, db
        new_tenant = TenantTable(args["company_id"], retrieve_merchant_name(url_cleaned), url_cleaned,
                                 args["shop_token"], args["shop_api_secret"], webhook_id)
        db.session.add(new_tenant)
        db.session.commit()

        if verbose:
            print("Callback Response JSON: ",
                  fulfillments_callback_created_json)
            print("Tenant string: ", str(new_tenant))
        return fulfillments_callback_created_json, 200

    def put(self):  # Update tenant
        return "This resource only supports POST requests.", 405

    # Delete tenant - NOT TESTED - FALCONFLEX API RESOURCE REQUIRED.
    def delete(self):
        return "This resource does not yet support DELETE requests.", 405
        args = tenant_delete_args.parse_args()
        merchant_url = clean_host_url(args["merchant_url"])
        company_record = TenantTable.query.filter(
            TenantTable.url == merchant_url).first()
        shop_token = company_record.merchant_token
        webhook_id = company_record.merchant_webhook_id
        fulfillments_callback_deleted = unsubscribe_merchant(
            merchant_url, webhook_id, shop_token)
        company_id = company_record.company_id
        fleet_token = company_record.fleet_token
        callback_id = company_record.fleet_callback_id
        fleet_callback_deleted = unsubscribe_fleet(
            args["fleet_url"], company_id, callback_id, fleet_token)
        return {"fulfillments_callback_response": fulfillments_callback_deleted, "fleet_callback_response": fleet_callback_deleted}, 200
