import requests
import time
from seleniumbase import Driver
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en"
apartments_sales = "https://www.immoweb.be/en/search/apartment/for-sale"


"""
Check if there is a Captcha. If yes, click manually.
"""
try:
    req_apartments = requests.get(apartments_sales)
    if req_apartments.status_code == 200:
        print("Apartments_sales link is okay")
    else:
        raise Exception(f"Status error: {req_apartments.status_code}")
except Exception as e:
    print(f"Request failed: {e}")
    driver = Driver(uc=True, headless=False)
    driver.uc_open_with_reconnect(apartments_sales, reconnect_time=6)
    driver.uc_gui_click_captcha()
    # driver.quit()

try:
    driver
except NameError:
    driver = Driver(uc=True, headless=False)
