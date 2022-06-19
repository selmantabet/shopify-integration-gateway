import hmac
import base64
import hashlib


def hmac_authenticate(hash_base64, name, payload):
    hash_decoded = base64.b64decode(hash_base64)
    from app import TenantTable
    api_secret = TenantTable.query.filter(
        TenantTable.company_name == name).first().merchant_api_secret
    api_secret_bytes = str.encode(api_secret)
    h = hmac.new(api_secret_bytes, payload, hashlib.sha256)

    # Comparing hashes, using compare_digest to avoid timing attacks.
    if hmac.compare_digest(hash_decoded, h.digest()):
        return True
    return False
