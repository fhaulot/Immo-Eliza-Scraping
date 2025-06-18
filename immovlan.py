import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.6099.129 Safari/537.36"
}
driver = uc.Chrome(version_main=122)
driver.get("https://immovlan.be/fr/immobilier?transactiontypes=a-vendre,en-vente-publique&noindex=1")
time.sleep(8)
cookie_button = driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]')
cookie_button.click()


root_url = "https://immovlan.be/fr/immobilier?transactiontypes=a-vendre,en-vente-publique" 
sales_url = []

def scrape_page(page_number) :
    url = f"{root_url}&page={page_number}&noindex=1"
    req= requests.get(url, headers=headers)

    if req.status_code == 200 :
        soup = BeautifulSoup(req.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link["href"]
            if "/projectdetail/" or "/detail/" in href :
                full_url = "ttps://immovlan.be/fr/immobilier?transactiontypes=a-vendre,en-vente-publique&noindex=1" + href if href.startswith("/") else href
                if full_url not in sales_url :
                    sales_url.append(full_url)
        
    else :
        print(f"Error while scrapping page{page_number}. Status code = {req.status_code}")

for page in range(1, 51) :
    scrape_page(page)
print(len(sales_url))
for url in sales_url :
    print(url)
print(sales_url)