from dotenv import load_dotenv
import os

cwd = os.getcwd()
env_path = os.path.join(cwd, "env", "vars.env")
print("cfg env path: ", env_path)
if (os.path.exists(env_path)):
    load_dotenv(dotenv_path=env_path)
    print("env vars initialized from config")


VERBOSE = (os.getenv('VERBOSE', 'False') == 'True')

if not 'WEBSITE_HOSTNAME' in os.environ:
    # local development
    print("Loading development parameters...")
    DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ["POSTGRESQL_USER"],
        dbpass=os.environ["POSTGRESQL_PASSWORD"],
        dbhost=os.environ["POSTGRESQL_ADDRESS"],
        dbname=os.environ["POSTGRESQL_DB_NAME"]
    )
    if VERBOSE:
        print(DATABASE_URI)

else:
    # production
    print("Loading production parameters...")
    print("Website Hostname: ", os.environ["WEBSITE_HOSTNAME"])
    DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ['DBUSER'],
        dbpass=os.environ['DBPASS'],
        dbhost=os.environ['DBHOST'] + ".postgres.database.azure.com",
        dbname=os.environ['DBNAME']
    )
    # INTEGRATION_GATEWAY_URI =
    if VERBOSE:
        print(DATABASE_URI)
