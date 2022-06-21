import os
from dotenv import load_dotenv

from callback_functions import subscribe_fleet

cwd = os.getcwd()
env_path = os.path.join(cwd, "env", "vars.env")
print("cfg env path: ", env_path)
if (os.path.exists(env_path)):
    load_dotenv(dotenv_path=env_path)
    print("env vars initialized from setup script")

fleet_callback_created = subscribe_fleet(os.environ["FLEET_MANAGEMENT_URI"],
                                         os.environ["FLEET_AUTH_TOKEN"], os.environ["INTEGRATION_GATEWAY"])

print(fleet_callback_created)
