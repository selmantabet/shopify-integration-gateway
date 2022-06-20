import requests


def get_coordinates(map_service_url, map_service_secret, address):
    endpoint = "/api/GetGeolocation"
    payload = {
        "address": address
    }
    map_service_auth_header = {"secret": map_service_secret}
    r = requests.post(map_service_url + endpoint,
                      headers=map_service_auth_header, json=payload)

    r_json = r.json()
    if (r_json["error"] is None):
        coordinates = r_json["data"]["coordinates"]
        lat = coordinates["lat"]
        long = coordinates["long"]
        return (lat, long)
    raise requests.RequestException from r_json["error"]


def get_address(map_service_url, map_service_secret, latitude, longitude):
    endpoint = "/api/GetAddress"
    payload = {
        "latitude": latitude,
        "longitude": longitude
    }
    map_service_auth_header = {"secret": map_service_secret}
    r = requests.post(map_service_url + endpoint,
                      headers=map_service_auth_header, json=payload)

    r_json = r.json()
    if (r_json["error"] is None):
        address = r_json["data"]["address"]
        return address["fullAddress"]
    raise requests.RequestException from r_json["error"]


# MAP_SERVICE_URI = "http://map-service-staging-alb-501217691.ap-southeast-1.elb.amazonaws.com"
# MAP_SERVICE_SECRET = "snvsjkvnskdnvkjdsv"
# b = get_coordinates(MAP_SERVICE_URI, MAP_SERVICE_SECRET,
#                     "Building 105 Street 855 Zone 67\nHazm AlMarkhiya")
# print(b)
