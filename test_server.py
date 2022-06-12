from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

import hmac
import hashlib

from parsers import *
from rest_functions import *
from constants import *
from webhook_functions import *
from callback_functions import *
from helper_functions import *
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
        return f"Company ID: {self.company_id} // URL: {self.url} // Name: {self.company_name}"


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

    def get(self, company_id):  # Get all tenant callbacks
        company_record = TenantTable.query.filter(
            TenantTable.company_id == company_id).first()
        print(company_record)

        return tenant_schema.jsonify(company_record), 200

    def post(self):  # Create new tenant
        args = tenant_post_args.parse_args()
        fulfillments_callback_created = subscribe_merchant(
            clean_host_url(args["merchant_url"]), INTEGRATION_GATEWAY_TEST, args["shop_token"], "fulfillments", "create")
        print("Fulfillment Callback JSON: ", fulfillments_callback_created)
        webhook_id = str(fulfillments_callback_created["webhook"]["id"])
        # fleet_callback_created = subscribe_fleet(FLEET_MANAGEMENT_URI,
        #                                          args["fleet_token"], INTEGRATION_GATEWAY_TEST)
        # print("Fleet Callback Status Code: ", str(
        #     fleet_callback_created.status_code))
        url_cleaned = clean_host_url(args["merchant_url"])
        new_tenant = TenantTable(args["company_id"], retrieve_merchant_name(url_cleaned), url_cleaned, args["fleet_token"],
                                 args["shop_token"], args["shop_api_secret"], webhook_id)
        db.session.add(new_tenant)
        db.session.commit()
        return {"fulfillments_callback_response": fulfillments_callback_created, "fleet_callback_response": 200}, 200


class TenantView(Resource):
    def get(self):  # Get all tenant callbacks
        args = tenant_get_args.parse_args()
        company_record = TenantTable.query.filter(
            TenantTable.company_id == args["company_id"]).first()
        print(company_record)
        print(company_record.fleet_token, type(company_record.fleet_token))
        print(company_record.merchant_api_secret, type(
            company_record.merchant_api_secret))

        return str(company_record), 200


api.add_resource(Tenant, "/tenants")

api.add_resource(TenantView, "/tenant")


if __name__ == "__main__":
    # Needless to say, do not use deploy this using the run method, let alone debug mode.
    app.run(debug=True)
