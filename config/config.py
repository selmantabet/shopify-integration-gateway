import os
from constants import *

VERBOSE = True

if not 'WEBSITE_HOSTNAME' in os.environ:
    # local development
    print("Loading development parameters...")
    DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=POSTGRESQL_USER,
        dbpass=POSTGRESQL_PASSWORD,
        dbhost=POSTGRESQL_ADDRESS,
        dbname=POSTGRESQL_DB_NAME
    )
    if VERBOSE:
        print(DATABASE_URI)

else:
    # production
    print("Loading production parameters...")
    DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ['DBUSER'],
        dbpass=os.environ['DBPASS'],
        dbhost=os.environ['DBHOST'] + ".postgres.database.azure.com",
        dbname=os.environ['DBNAME']
    )
    if VERBOSE:
        print(DATABASE_URI)
