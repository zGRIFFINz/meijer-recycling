# This is an example api program I wrote with Sam.
import json

import requests

api_url_get = "https://www.boredapi.com/api/activity"
api_url_post = "https://httpbin.org/anything"


def api_get_request():
    try:
        response = requests.get(api_url_get)
    except:
        print("fucking oops")
        exit(1)
    print(response.status_code)
    return response


def api_post_request():
    try:
        data_payload = {"dog": "motzi", "cat": "abby"}
        #joke_json = joke_type.jsonlo
        response = requests.post(api_url_post, json=data_payload)
    except:
        print("Post request wrong format.")
        exit(1)
    return response


def evaluate(response):
    try:
        original_dict = response.json()
        for key, val in original_dict.items():
            print(key + ":", val)
    except:
        print(response)


def main():
    #response = api_get_request()
    response = api_post_request()
    evaluate(response)


if __name__ == "__main__":
    main()
