import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
"""driver = webdriver(uc=True, headless=False)
driver.uc_open_with_reconnect(apartments_sales, reconnect_time=6)
driver.uc_gui_click_captcha()
    # driver.quit()"""

# Specify the correct ChromeDriver version for your Chrome browser (122)
driver = uc.Chrome(version_main=122)
driver.get("https://immo.notaire.be/fr/biens-a-vendre")
time.sleep(8)
cookie_button = driver.find_element(By .XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
cookie_button.click()


"""url = requests.get("https://immo.notaire.be/fr/biens-a-vendre")
soup = BeautifulSoup(url.text, 'html.parser')
links = soup.find_all("a", href=True)
sales_url = []
for link in links :
    href = link['href']
    if "/a-vendre/" in href:
            # Ajouter l'URL relative au site de base
            full_url = "https://immo.notaire.be" + href if href.startswith("/") else href
            sales_url.append(full_url)

for url in sales_url:
    print(url)"""

root_url = "https://immo.notaire.be/fr/biens-a-vendre" 
sales_url = []

def scrape_page(page_number) :
    url = f"{root_url}?page={page_number}"
    req= requests.get(url)

    if req.status_code == 200 :
        soup = BeautifulSoup(req.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link["href"]
            if "/a-vendre/" in href :
                full_url = "https://immo.notaire.be" + href if href.startswith("/") else href
                if full_url not in sales_url :
                    sales_url.append(full_url)
        
    else :
        print(f"Error while scrapping page{page_number}. Status code = {req.status_code}")

for page in range(1, 21) :
    scrape_page(page)
print(len(sales_url))
for url in sales_url :
    print(url)
   