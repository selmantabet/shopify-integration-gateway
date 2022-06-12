from constants import FLEET_MANAGEMENT_URI


callback_url = FLEET_MANAGEMENT_URI

callback_host = callback_url.replace("https://", "")
callback_host = callback_host.strip("/")
callback_host = callback_host + "/taskscallback"
print(callback_host)
