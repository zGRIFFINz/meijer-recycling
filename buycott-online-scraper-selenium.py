import traceback
import selenium
import time
from selenium import webdriver
from selenium.common import TimeoutException, SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Download Firefox Gecko driver from https://github.com/mozilla/geckodriver/releases, geckodriver-v0.34.0-linux32.tar.gz

# Configure driver options.
options = selenium.webdriver.firefox.options.Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
#options.add_argument("--ignore-ssl-errors=yes")
#options.add_argument("--ignore-certificate-errors")
#options.accept_insecure_certs = True
#profile = webdriver.FirefoxProfile()
#profile.accept_untrusted_certs = True
# options.add_argument("--headless")

# Buycott website components
buycott_searchbar = "input.form-control#nav_search"
buycott_enter_button = "#nav_search_button"
buycott_meijer = "https://www.buycott.com/"
product_name = "<div>Meijer Naturals Oats, Old Fashioned</div>"
product_upc = "/html/body/div/div[2]/table[1]/tbody/tr[1]/td[3]/div[1]/a"
next_button = ""

# Initialize driver
try:
    # Initialize the WebDriver with the options
    driver = webdriver.Firefox(options=options)
    print(driver)
    print(options)
except SessionNotCreatedException as e:
    print(f"{e}: Session could not be created. Check DNS settings/flush cache.")
    exit(1)
driver.get(buycott_meijer)
driver.implicitly_wait(10)


# Waits for upc input.
def upc_input():
    #upc_code = input("Enter UPC code: ")
    upc_code = "642860300267"
    return upc_code


# Search Buycott online database for upc code.
def buycott_search(upc_code):
    try:
        searchbar = driver.find_element(By.CSS_SELECTOR, buycott_searchbar)
    except Exception as e:
        print(f"Could not find searchbar: {e}.")
    driver.implicitly_wait(3)
    try:
        searchbar = driver.find_element(By.CSS_SELECTOR, buycott_searchbar)
    except Exception as e:
        print(f"Could not find searchbar: {e}.")
    driver.implicitly_wait(3)
    try:
        searchbar.send_keys(upc_code)
    except Exception as e:
        print(f"Could not enter upc: {e}.")
    driver.implicitly_wait(3)
    try:
        start_search = driver.find_element(By.CSS_SELECTOR, buycott_enter_button)
        start_search.click()
    except Exception as e:
        print(f"Could not find enter button: {e}.")



# Pulls information from page for specified element.
def wait_page_load():
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, f"{product_upc}")))
    except TimeoutException as e:
        print(f"{e}: Timed out waiting for page to load.")
        driver.quit()
        #exit(1)


# Parses html information from page source for desired html element.
def parse_product_data():
    page_source = driver.page_source
    upc_codes = []
    product_names = []

    soup = BeautifulSoup(page_source, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        if a_tag["href"].startswith("/upc/"):
            upc_code = a_tag["href"].split("/")[-1]
            upc_codes.append(upc_code)
    print(upc_codes)

    #grocery_elements = soup.find_all("a", href=True)

    #if grocery_elements:
    #    for grocery in grocery_elements:
    #        print(grocery.get_text())
    #else:
    #    print("Grocery not found")


# Imitate searching for "grocery" in search bar.
def next_page():
    exit(0)
#searchbar.send_keys(search_for)
#time.sleep(2)
#start_search = driver.find_element(By.CSS_SELECTOR, enter_button)
#time.sleep(3)
#start_search.click()


# Obligatory main
def main():
    upc_code = ""
    try:
        upc_input()
        buycott_search(upc_code)
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        print(traceback.format_exc())
    #finally:
    #    driver.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        driver.quit()
        print("\n~~ Aborting Query. Bye! ~~")
