from constants_prod import *
from callback_functions import *
fleet_callback_created = subscribe_fleet(FLEET_MANAGEMENT_URI_PROD,
                                         FLEET_AUTH_TOKEN_PROD, INTEGRATION_GATEWAY)

print(fleet_callback_created)
