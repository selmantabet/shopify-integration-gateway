import os

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'flask-insecure-7ppocbnx@w71dcuinn*t^_mzal(t@o01v3fee27g%rg18fc5d@'

DEBUG = False
VERBOSE = False
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']
                 ] if 'WEBSITE_HOSTNAME' in os.environ else []


# Configure Postgres database; the full username for PostgreSQL flexible server is
# username (not @sever-name).
DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'] + ".postgres.database.azure.com",
    dbname=os.environ['DBNAME']
)
print("Production DB URI: ", str(DATABASE_URI))
