from constants import *
from callback_functions import *
from webhook_functions import *
from helper_functions import *

fulfillments_callback_created = subscribe_merchant(
    clean_host_url(MERCHANT_HOST), INTEGRATION_GATEWAY_TEST, MERCHANT_TOKEN, "fulfillments", "create")
print("Fulfillment Callback JSON: ", fulfillments_callback_created)
if (payload_error_checker(fulfillments_callback_created)):
    print("Error detected...")
    webhook_id = 0
else:
    webhook_id = fulfillments_callback_created["webhook"]["id"]
print("Webhook ID: ", webhook_id, "    type: ", type(webhook_id))
fleet_callback_created = subscribe_fleet(FLEET_MANAGEMENT_URI,
                                         FLEET_AUTH_TOKEN, INTEGRATION_GATEWAY_DUMMY)
print("Fleet Callback Status Code: ", str(
    fleet_callback_created.status_code))
print(fleet_callback_created.json())
