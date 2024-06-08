import traceback
import selenium
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
options = selenium.webdriver.firefox.options.Options()
#options.add_argument('ignore-certificate-errors')
#options.add_argument("--ignore-ssl-errors=yes")
#options.add_argument("--headless")
url = "https://www.meijer.com/shopping/search.html?text=grocery"
url = "https://www.meijer.com/shopping/search.html?text=grocery&sort_order=item_name-ascending"
#url = "https://www.meijer.com"

# Initialize driver
try:
    driver = webdriver.Firefox(options=options)
except SessionNotCreatedException as e:
    print(f"{e}: Session could not be created. Check DNS settings/flush cache.")
    exit(1)
driver.get(url)


# Pulls information from page for specified element.
def collect_web_data():
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-tile--line-clamp-text')))
    except TimeoutException as e:
        print(f"{e}: Timed out waiting for page to load.")
        driver.quit()
        exit(1)


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
        collect_web_data()
        parse_web_data()
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        print(traceback.format_exc())
    finally:
        driver.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        driver.quit()
        print("\n~~ Aborting Query. Bye! ~~")