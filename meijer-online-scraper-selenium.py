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

# Selenium options for operation
#firefox_options = Options()
#firefox_options.add_argument("--ignore-ssl-errors=yes")

#firefox_profile = webdriver.FirefoxProfile()
#firefox_profile.accept_untrusted_certs = True

options = selenium.webdriver.firefox.options.Options()
#options.accept_insecure_certs = True
#profile = webdriver.FirefoxProfile()
#profile.accept_untrusted_certs = True
options.add_argument('--ignore-certificate-errors=yes')
options.add_argument("--ignore-ssl-errors=yes")
# options.add_argument("--headless")

# Meijer website components
url_home = "https://www.meijer.com"
url_groceries = "https://www.meijer.com/shopping/search.html?text=grocery"
# url = "https://www.meijer.com/shopping/search.html?text=grocery&sort_order=item_name-ascending"
# meijer_searchbar = "form-control new-search-bar__search-box"
meijer_searchbar = "input.form-control.new-search-bar__search-box"
enter_button = ".new-search-bar__search-icon"
# meijer_searchbar = "/html/body/div[1]/div/div[2]/div/div/div[1]/div/header/nav/div[1]/div[2]/div/div/div/div/div/div/div/input"
product_names = "product-tile--line-clamp-text"
search_for = "grocery"

options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Initialize driver
try:
    # Initialize the WebDriver with the options
    driver = webdriver.Firefox(options=options)
    print(driver)
    print(options)
except SessionNotCreatedException as e:
    print(f"{e}: Session could not be created. Check DNS settings/flush cache.")
    exit(1)
driver.get(url_home)
driver.implicitly_wait(10)


# Imitate searching for "grocery" in search bar.
def grocery_search():
    #driver.implicitly_wait(10)
    time.sleep(3)
    try:
        searchbar = driver.find_element(By.CSS_SELECTOR, meijer_searchbar)
        print("Found it!")
        print(options)
        print(searchbar)
    except Exception as e:
        print("I didn't find it :(")
        print(e)
    searchbar.send_keys(search_for)
    time.sleep(2)
    start_search = driver.find_element(By.CSS_SELECTOR, enter_button)
    time.sleep(3)
    start_search.click()


# Pulls information from page for specified element.
def collect_web_data():
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


# Obligatory main
def main():
    try:
        grocery_search()
        #collect_web_data()
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
