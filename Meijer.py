import base64
import os
import requests
from dotenv import load_dotenv

load_dotenv()
User = os.getenv('Mperks_UN')
PassKey = os.getenv('Mperks_PS')
account_services_client_id = os.getenv('client_id')
account_services_secret = os.getenv('secret')

# From Meijer_v5.20.1_apkpure.com/res/values/strings.xml
# Token string, decoded
token_decoded = f"{account_services_client_id}:{account_services_secret}".encode("UTF-8")
# Token string, encoded
basic_token = base64.encodebytes(token_decoded).decode("UTF-8").strip()


def login():
    request = dict()
    request["url"] = "https://login.meijer.com/as/token.oauth2"
    request["headers"] = {"Authorization": f"Basic {basic_token}"}
    request["params"] = {
        "grant_type": "password",
        "scope": "openid",
        "username": User,
        "password": PassKey,
    }
    return request

request = login()
print(request)

# access_token=<JWT Token>
# refresh_token=<Refresh Token>
# token_type=Bearer
# expires_in=604799 (7 days)
r = requests.post(**request)
#for key, value in r.items():
  #  setattr(requests, key, value)
print(r)

# Break apart the JWT to get the MeijerID data
# scope=['openid']
# client_id=mma
# iss=https://login.meijer.com/
# sub=<INT>
# eguest_id=<INT>
# has_digital=<INT>
# digital_id=<INT>
# has_mperks=<INT>
# mperks_shopper_id=<INT>
# mperks_ext_shopper_id=<UUID>
# exp=<>
"""
_, meijer_id64, _ = requests.access_token.split(".")
ids = json.loads(base64.decodebytes(f"{meijer_id64}=".encode()))
for key, value in ids.items():
    setattr(requests, key, value)
requests.bearer_token = f"{requests.token_type} {requests.access_token}"
#
requests.session.headers.update({"Authorization": requests.bearer_token})

"""
