import requests
from bs4 import BeautifulSoup

# Buycott web options
url_base = "https://www.buycott.com/upc/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


# Provide upc code
def upc_input():
    # upc_code = input("Enter UPC code: ")
    upc_code = "642860300267"
    return upc_code


# Grab product name from url results
def parse_web_data(upc_code):
    url_full = url_base + upc_code
    response = requests.get(url_full, headers=headers)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            product_names = soup.find_all("h2")
            if product_names:
                for product in product_names:
                    product_name = product.get_text()
                    print(product_name)
            else:
                print("Item not found.")
        except Exception as e:
            print(f"Cannot reach URL: {e}.")
    else:
        print(f"{response.status_code} Error")


# Obligatory main
def main():
    try:
        upc_code = upc_input()
        print(upc_code)
        parse_web_data(upc_code)
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        exit(1)
    finally:
        exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n~~ Aborting Query. Bye! ~~")
