from pathlib import Path
import os

from constants import POSTGRESQL_ADDRESS, POSTGRESQL_DB_NAME, POSTGRESQL_PASSWORD, POSTGRESQL_USER

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print("Deployment BASE DIR: ", str(BASE_DIR))
DEBUG = True
VERBOSE = True
DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=POSTGRESQL_USER,
    dbpass=POSTGRESQL_PASSWORD,
    dbhost=POSTGRESQL_ADDRESS,
    dbname=POSTGRESQL_DB_NAME
)
print("Deployment DB URI: ", str(DATABASE_URI))
# TIME_ZONE = 'UTC'

# STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
# STATIC_URL = 'static/'
