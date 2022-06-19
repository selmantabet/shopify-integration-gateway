"""
FalconFlex Integration Gateway - Main Script

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for FalconFlex - Snoonu Technologies.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from config import cfg
from resources.config_check import ConfigCheck
from resources.task_update import Task_Update
from resources.tenant_view import TenantView
from resources.tenant import Tenant
from resources.task import Task
from dotenv import load_dotenv
import os

cwd = os.getcwd()
env_path = os.path.join(cwd, "env", "vars.env")
print("cfg env path: ", env_path)
if (os.path.exists(env_path)):
    load_dotenv(dotenv_path=env_path)
    print("env vars initialized from main app")

verbose = (os.getenv('VERBOSE', 'False') == 'True')

app = Flask(__name__)
api = Api(app)


app.config.from_object(cfg)
app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)

ma = Marshmallow(app)


class TenantTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String(255), unique=True)
    company_name = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    merchant_token = db.Column(db.String(255), unique=True)
    merchant_api_secret = db.Column(db.String(255), unique=True)
    merchant_webhook_id = db.Column(db.String(255), unique=True)

    def __init__(self, company_id, company_name, url, merchant_token, merchant_api_secret, merchant_webhook_id):
        self.company_id = company_id
        self.company_name = company_name
        self.url = url
        self.merchant_token = merchant_token
        self.merchant_api_secret = merchant_api_secret
        self.merchant_webhook_id = merchant_webhook_id

    def __repr__(self):
        return f"Company ID: {self.company_id} // URL: {self.url}"


class TenantSchema(ma.Schema):
    class Meta:
        fields = ("company_id", "company_name", "url",
                  "merchant_token", "merchant_api_secret", "merchant_webhook_id")


tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)


"""------ root/host in testing is INTEGRATION_GATEWAY_TEST ------"""

api.add_resource(Task, "/tasks")

api.add_resource(Task_Update, "/taskscallback")

api.add_resource(Tenant, "/tenants")

api.add_resource(TenantView, "/tenant")

api.add_resource(ConfigCheck, "/config")


if __name__ == "__main__":
    # Needless to say, do not use deploy this using the run method, let alone debug mode.
    app.run(debug=True)
