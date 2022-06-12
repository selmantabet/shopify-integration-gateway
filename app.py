"""
FalconFlex Integration Gateway - Main Script

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for FalconFlex - Snoonu Technologies.
"""
import hmac
import base64
import hashlib

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from constants_prod import SHOPIFY_API_VERSION

from parsers import *
from rest_functions import *
from constants import *
from webhook_functions import *
from callback_functions import *
from helper_functions import *
from status_mapper import *
import json

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_ADDRESS}/{POSTGRESQL_DB_NAME}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


class TenantTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String(255), unique=True)
    company_name = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    fleet_token = db.Column(db.String(255), unique=True)
    merchant_token = db.Column(db.String(255), unique=True)
    merchant_api_secret = db.Column(db.String(255), unique=True)
    merchant_webhook_id = db.Column(db.String(255), unique=True)

    def __init__(self, company_id, company_name, url, fleet_token, merchant_token, merchant_api_secret, merchant_webhook_id):
        self.company_id = company_id
        self.company_name = company_name
        self.url = url
        self.fleet_token = fleet_token
        self.merchant_token = merchant_token
        self.merchant_api_secret = merchant_api_secret
        self.merchant_webhook_id = merchant_webhook_id

    def __repr__(self):
        return f"Company ID: {self.company_id} // URL: {self.url}"


class TenantSchema(ma.Schema):
    class Meta:
        fields = ("company_id", "company_name", "url", "fleet_token",
                  "merchant_token", "merchant_api_secret", "merchant_webhook_id")


tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)


class Tenant(Resource):
    """
    The Tenant resource: Simply deals with webhooks subscriptions upon info submission by an admin.

    FalconFlex callbacks are still not tested, need the right credentials for that.
    """

    def get(self):  # Get all tenant callbacks
        return

    def post(self):  # Create new tenant
        args = tenant_post_args.parse_args()
        fulfillments_callback_created = subscribe_merchant(
            clean_host_url(args["merchant_url"]), INTEGRATION_GATEWAY_TEST, args["shop_token"], "fulfillments", "create")
        print("Fulfillment Callback JSON: ", fulfillments_callback_created)
        webhook_id = fulfillments_callback_created["webhook"]["id"]

        fleet_callback_created = subscribe_fleet(FLEET_MANAGEMENT_URI,
                                                 args["fleet_token"], INTEGRATION_GATEWAY_TEST)

        url_cleaned = clean_host_url(args["merchant_url"])
        new_tenant = TenantTable(args["company_id"], retrieve_merchant_name(url_cleaned), url_cleaned, args["fleet_token"],
                                 args["shop_token"], args["shop_api_secret"], webhook_id)
        db.session.add(new_tenant)
        db.session.commit()
        return {"fulfillments_callback_response": fulfillments_callback_created, "fleet_callback_response": fleet_callback_created}, 200

    def put(self):  # Update tenant
        return

    # Delete tenant - NOT TESTED - FALCONFLEX API RESOURCE REQUIRED.
    def delete(self):
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


class Task(Resource):
    """
    The Task resource: Creates tasks upon receiving fulfillment webhooks.
    """

    def get(self):  # Get all tasks
        return

    def post(self):  # Create a new task
        # Parsing headers...
        hmac_hash = request.headers.get("x-shopify-hmac-sha256")
        merchant_url_noscheme = request.headers.get("x-shopify-shop-domain")
        merchant_name = merchant_url_noscheme.split(
            ".")[0]  # https://{merchant_name}.myshopify.com
        print(merchant_name, merchant_url_noscheme)
        fulfillment_id_header = request.headers.get("x-shopify-fulfillment-id")
        shopify_api_version = request.headers.get("x-shopify-api-version")
        if (shopify_api_version != SHOPIFY_API_VERSION):
            print("WARNING: SHOPIFY API VERSION HAS CHANGED.")
        request_body = request.get_data()
        if not hmac_authenticate(hmac_hash, merchant_name, request_body):
            return "Failed Authentication. Invalid HMAC.", 403
        print("Continuing from auth...")
        company_record = TenantTable.query.filter(
            TenantTable.company_name == merchant_name).first()

        merchant_url = company_record.url
        fleet_token = company_record.fleet_token
        merchant_token = company_record.merchant_token

        fulfillment_payload = json.loads(request_body)
        # THIS MUST ALWAYS PASS. Since HMAC passed, request integrity should be fine.
        assert(fulfillment_payload["id"] == fulfillment_id_header,
               "Fatal error: Fulfillment ID Header not equal to body fulfillment ID.")

        # merchant_token = MERCHANT_TOKEN  # ONLY FOR TESTING
        task_payload = generate_task_payload(
            merchant_url, merchant_token, fulfillment_payload)
        print("Payload generated: ", task_payload)
        creation_response = create_task(
            FLEET_MANAGEMENT_URI, fleet_token, task_payload)
        return {"Creation Response JSON: ": creation_response}, 200


class Task_Update(Resource):
    def get(self):
        return

    def post(self):
        print("Connected...")
        task_update_payload_raw = request.get_json()
        print("JSON Retrieved: ", task_update_payload_raw)
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
                raise("Malformed Metadata: ", i)

        merchant_url_cleaned = clean_host_url(merchant_url)
        company_record = TenantTable.query.filter(
            TenantTable.url == merchant_url_cleaned).first()
        shop_token = company_record.merchant_token
        status = task_update_payload["TaskStatus"]
        mapped_status = mapping_dict[status]
        update_response = send_status_update(
            merchant_url_cleaned, shop_token, order_id, fulfillment_id, mapped_status)
        return update_response, 200


class TenantView(Resource):
    def get(self):  # Get all tenant callbacks
        args = tenant_get_args.parse_args()
        company_record = TenantTable.query.filter(
            TenantTable.company_id == args["company_id"]).first()
        return str(company_record), 200


"""------ root/host in testing is INTEGRATION_GATEWAY_TEST ------"""

api.add_resource(Task, "/tasks")

api.add_resource(Task_Update, "/taskscallback")

api.add_resource(Tenant, "/tenants")

api.add_resource(TenantView, "/tenant")


def hmac_authenticate(hash_base64, name, payload):
    hash_decoded = base64.b64decode(hash_base64)
    api_secret = TenantTable.query.filter(
        TenantTable.company_name == name).first().merchant_api_secret
    api_secret_bytes = str.encode(api_secret)
    h = hmac.new(api_secret_bytes, payload, hashlib.sha256)

    # Comparing hashes, using compare_digest to avoid timing attacks.
    if hmac.compare_digest(hash_decoded, h.digest()):
        return True
    return False


if __name__ == "__main__":
    # Needless to say, do not use deploy this using the run method, let alone debug mode.
    app.run(debug=True)
