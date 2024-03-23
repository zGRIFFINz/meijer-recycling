import requests

api_url_get = "https://www.boredapi.com/api/activity"
api_url_post = "https://httpbin.org/anything"


def api_get_request():
    try:
        response = requests.get(api_url_get)
    except:
        print("oopsies, it's been a rough day. -_-")
        exit(1)
    return response


def api_post_request():
    poster = {'insect':'bee','dog':'mozzarella'}
    try:
        response = requests.post(url=api_url_post, json = poster)
    except:
        print("oopsies, it's been a rough day. -_- p")
        exit(1)
    return response

def evaluate(response):
    try:
        bugs = response.json()
        for key, val in bugs.items():
            print(key+':', val)
    except:
        print('Bro this isnt even data')
# print(response.json())

def main():
    #response = api_get_request()
    response = api_post_request()
    #response = "butts"
    evaluate(response)



if __name__ == "__main__":
    main()


