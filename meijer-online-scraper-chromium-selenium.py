import traceback
import selenium
import time
import random
from selenium import webdriver
from selenium.common import TimeoutException, SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Download Chromium driver from https://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/

# Selenium options for operation
#firefox_options = Options()
#firefox_options.add_argument("--ignore-ssl-errors=yes")

#firefox_profile = webdriver.FirefoxProfile()
#firefox_profile.accept_untrusted_certs = True


#options.accept_insecure_certs = True
#profile = webdriver.FirefoxProfile()
#profile.accept_untrusted_certs = True
#options.add_argument('--ignore-certificate-errors=yes')
#options.add_argument("--ignore-ssl-errors=yes")
# options.add_argument("--headless")

# Meijer website components
url_home = "https://www.meijer.com"
url_groceries = "https://www.meijer.com/shopping/search.html?text=grocery"
meijer_searchbar = "input.form-control.new-search-bar__search-box"
enter_button = ".new-search-bar__search-icon"
load_more_button = "button.btn.btn-secondary"
product_names = "product-tile--line-clamp-text"
search_for = "grocery"

# Chromium web driver options
chrome_options = selenium.webdriver.chromium.options.ChromiumOptions()
#chrome_options.add_argument('--disable-http2')
chrome_options.add_argument('--incognito')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# Randomized wait options
def wait_1():
    wait = random.randint(3,6)
    return wait


def wait_2():
    wait = random.randint(10,15)
    return wait


# Initialize driver
try:
    # Initialize the WebDriver with the options
    driver = webdriver.Chrome(options=chrome_options)
    print(driver)
except SessionNotCreatedException as e:
    print(f"{e}: Session could not be created. Check DNS settings/flush cache.")
    exit(1)
driver.get(url_home)


# Imitate searching for "grocery" in search bar.
def grocery_search():
    time.sleep(wait_2())
    try:
        searchbar = driver.find_element(By.CSS_SELECTOR, meijer_searchbar)
        print("Found it!")
        #print(options)
        print(searchbar)
    except Exception as e:
        print("I didn't find it :(")
        print(e)
    time.sleep(wait_1())
    searchbar.send_keys(search_for)
    time.sleep(wait_1())
    start_search = driver.find_element(By.CSS_SELECTOR, enter_button)
    time.sleep(wait_1())
    start_search.click()


# Pulls information from page for specified element.
def driver_wait():
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, f"{product_names}")))
    except TimeoutException as e:
        print(f"{e}: Timed out waiting for page to load.")
        driver.quit()
        #exit(1)


# Parses html information from page source for desired html element.
def parse_web_data():
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    grocery_elements = soup.find_all("h2", class_="product-tile--line-clamp-text")

    if grocery_elements:
        for grocery in grocery_elements:
            print(grocery.get_text())
    else:
        print("Grocery not found")


# Click the "Load More" button at the bottom
def load_more():
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, load_more_button)))
        time.sleep(wait_2())
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(wait_1())
        load_more = driver.find_element(By.CSS_SELECTOR, load_more_button)
        print("I found the load more button")
        load_more.click()
        time.sleep(300)
    except Exception as e:
        print(f"{e}: Could not find load more button.")


# Obligatory main
def main():
    try:
        grocery_search()
        driver_wait()
        load_more()
        #parse_web_data()
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
