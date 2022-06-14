"""
Integration Gateway Constants

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
This file contains constants that may be altered to fit business needs and is
meant to be used in production.
"""

# Time (in minutes) between webhook generation to pickupTime
TIME_BUFFER_MINUTES = 5

SHOPIFY_API_VERSION = '2022-04'

INTEGRATION_GATEWAY_PROD = "https://integration-gateway.azurewebsites.net"
FLEET_AUTH_TOKEN_PROD = "15D7E1D1F22D3F415C346E0DB3D2D6A50912F90461C355221F455B5DA4E24A43"
FLEET_MANAGEMENT_URI_PROD = "https://integrationgateway-staging-lb.falconflex.ai"

POSTGRESQL_DB_NAME = "falconflex-integration"
POSTGRESQL_AZURE_DB_NAME = "postgres"
POSTGRESQL_PORT = 5432
POSTGRESQL_HOST_AZURE = "integration-gateway-postgres.postgres.database.azure.com"
POSTGRESQL_USER = "postgres"
POSTGRESQL_AZURE_PASSWORD = "Selman_123"
