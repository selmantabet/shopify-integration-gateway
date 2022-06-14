"""
Integration Gateway Test Constants

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
These values are used only for testing purposes.

THIS IS NOT INTENDED FOR PRODUCTION USE.

It contains all the keys and strings used to test out different parts of the project.
"""

POSTGRESQL_DB_NAME = "falconflex-integration"
POSTGRESQL_AZURE_DB_NAME = "postgres"
POSTGRESQL_PORT = 5432
POSTGRESQL_ADDRESS = "localhost"
POSTGRESQL_HOST_AZURE = "integration-gateway-postgres.postgres.database.azure.com"
POSTGRESQL_USER = "postgres"
POSTGRESQL_PASSWORD = "Selman@123"
POSTGRESQL_AZURE_PASSWORD = "Selman_123"

API_KEY = "0d1520ca4fb7f27f1782fe0b7c0451bc"
API_SECRET = "6955f2ab1a939dd4689e0633fa934a0a"
API_VERSION = '2022-04'
MERCHANT_HOST = "https://chaoscodes.myshopify.com/"
MERCHANT_URI = "https://chaoscodes.myshopify.com/admin/api/2022-04/"
MERCHANT_HOST_OLD = "https://falconflex-test.myshopify.com/"
MERCHANT_URI_OLD = "https://falconflex-test.myshopify.com/admin/api/2022-04/"
MERCHANT_TOKEN = "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"
MERCHANT_TOKEN_OLD = "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"


FLEET_MANAGEMENT_HOST = "integrationgateway-staging-lb.falconflex.ai"
FLEET_MANAGEMENT_URI = "https://integrationgateway-staging-lb.falconflex.ai"
FLEET_MANAGEMENT_URI_TEST = "https://webhook.site/3cc94e74-27fb-4bfa-b9e8-350bc6d5a206"
FLEET_AUTH_TOKEN = "15D7E1D1F22D3F415C346E0DB3D2D6A50912F90461C355221F455B5DA4E24A43"

INTEGRATION_GATEWAY = "https://localhost:5000/"
INTEGRATION_GATEWAY_HOST = "webhook.site"
INTEGRATION_GATEWAY_TEST_NOSCHEME = "webhook.site/d18990f9-038f-4c9f-b20b-6ead5f45bb3f"
INTEGRATION_GATEWAY_TEST = "https://webhook.site/44a25e69-f3ce-4b30-81bd-f3210e4b230e"
INTEGRATION_GATEWAY_DUMMY = "https://webhook.site/testhook"
INTEGRATION_GATEWAY_TASK_CREATE = "https://webhook.site/d18990f9-038f-4c9f-b20b-6ead5f45bb3f/tasks"
INTEGRATION_GATEWAY_TASK_UPDATES = "https://webhook.site/d18990f9-038f-4c9f-b20b-6ead5f45bb3f/taskscallback"

INTEGRATION_GATEWAY_FROM_SHOP = "https://webhook.site/d18990f9-038f-4c9f-b20b-6ead5f45bb3f?company_id=620ac4fe812b6a4a8977e007&fleet_token=15D7E1D1F22D3F415C346E0DB3D2D6A50912F90461C355221F455B5DA4E24A43"
INTEGRATION_GATEWAY_FROM_FLEET = "https://webhook.site/d18990f9-038f-4c9f-b20b-6ead5f45bb3f?merchant=falconflex-test&token=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"

COMPANY_ID_TEST = "620ac4fe812b6a4a8977e007"

LONGITUDE_TEST = 51.4408446
LATITUDE_TEST = 25.3138126
