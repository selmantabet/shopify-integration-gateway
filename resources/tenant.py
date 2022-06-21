from flask_restful import Resource
from utils.parsers import tenant_post_args, tenant_delete_args
from utils.helper_functions import clean_host_url, retrieve_merchant_name
from utils.webhook_functions import subscribe_merchant


class Tenant(Resource):
    """
    The Tenant resource: Simply deals with webhooks subscriptions upon info submission by an admin.

    FalconFlex callbacks are still not tested, need the right credentials for that.
    """

    def get(self):  # Get all tenant callbacks
        return "This resource only supports POST and DELETE requests.", 405

    def post(self):  # Create new tenant
        from requests import JSONDecodeError
        import os
        if "WEBSITE_HOSTNAME" in os.environ:
            gateway_host = os.environ["WEBSITE_HOSTNAME"]
        else:
            gateway_host = "integration-gateway.azurewebsites.net"
        gateway_url = "https://" + gateway_host
        verbose = (os.getenv('VERBOSE', 'False') == 'True')
        from app import TenantTable, db
        args = tenant_post_args.parse_args()
        merchant_url = clean_host_url(args["merchant_url"])
        company_record = TenantTable.query.filter(
            TenantTable.url == merchant_url).first()
        if company_record:
            return "Merchant Already Exists", 409
        fulfillments_callback_created = subscribe_merchant(
            merchant_url, gateway_url, args["shop_token"], "fulfillments", "create")
        try:
            fulfillments_callback_created_json = fulfillments_callback_created.json()
            webhook_id = fulfillments_callback_created_json["webhook"]["id"]
        except JSONDecodeError:
            return {"errors": "JSON could not be decoded."}, 400
        except KeyError:
            return {"errors": "Failure on webhook creation.", "dump": fulfillments_callback_created_json}, 400
        except:
            return {"errors": "Something went wrong. Try again later."}, 500

        url_cleaned = clean_host_url(args["merchant_url"])

        new_tenant = TenantTable(args["company_id"], retrieve_merchant_name(url_cleaned), url_cleaned,
                                 args["shop_token"], args["shop_api_secret"], webhook_id)
        db.session.add(new_tenant)
        db.session.commit()

        if verbose:
            print("Callback Creation Response JSON: ",
                  fulfillments_callback_created_json)
            print("Tenant string: ", str(new_tenant))
        return fulfillments_callback_created_json, 200

    def put(self):  # Update tenant
        return "This resource only supports POST and DELETE requests.", 405

    # Delete tenant
    def delete(self):
        from app import TenantTable
        from utils.webhook_functions import unsubscribe_merchant
        import os
        from sqlalchemy import delete, create_engine
        verbose = (os.getenv('VERBOSE', 'False') == 'True')
        args = tenant_delete_args.parse_args()
        merchant_url = clean_host_url(args["merchant_url"])
        company_record = TenantTable.query.filter(
            TenantTable.url == merchant_url).first()
        if not company_record:
            return "Merchant Not Found", 404
        shop_token = company_record.merchant_token
        webhook_id = company_record.merchant_webhook_id
        fulfillments_callback_deleted = unsubscribe_merchant(
            merchant_url, webhook_id, shop_token)
        status = fulfillments_callback_deleted.status_code
        if verbose:
            print("Callback Deletion Response Code: ",
                  status)
            print("Deleting Tenant from database -> ", str(company_record))
        deletion = delete(TenantTable).where(
            TenantTable.url == merchant_url)
        from config.cfg import DATABASE_URI
        engine = create_engine(DATABASE_URI)
        engine.execute(deletion)
        return 200
