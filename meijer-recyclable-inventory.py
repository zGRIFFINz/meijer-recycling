import os
import base64
import requests
from dotenv import load_dotenv

# .env file vars
load_dotenv()
food_type = os.getenv("test_var")
service_id = os.getenv("service_id")
service_key = os.getenv("service_key")
user = os.getenv("user")
password = os.getenv("password")

# Formation of the token
token_decoded = f"{service_id}:{service_key}".encode("UTF-8")
basic_token = base64.encodebytes(token_decoded).decode("UTF-8").strip()


# Login function
def login():
    request = dict()
    request["url"] = "https://login.meijer.com/as/token.oauth2"
    request["headers"] = {"Authorization": f"Basic {basic_token}"}
    request["params"] = {
        "grant_type": "password",
        "scope": "openid",
        "username": user,
        "password": password,
    }
    print(request)
    response = requests.get(**request)
    print(response)
    print(response.status_code)


login()
