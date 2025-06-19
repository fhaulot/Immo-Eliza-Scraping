#In this file, we will obtain all the urls of the sales property in the immovlan website. 

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

"""We import several modules 
Requests to get the proper url of the website
We use the selenium module to get trough the cookies once. 
We use time to let the website charge his popup page before clicking the  button
We use add an undetected chrome driver and also BeautifulSoup to parse the all html page"""

driver = uc.Chrome(version_main=122)
driver.get("https://immovlan.be/fr/immobilier?transactiontypes=a-vendre,en-vente-publique&noindex=1")
time.sleep(8)
cookie_button = driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]')
cookie_button.click()

"""This part define headers to get trough the first cookie page. We fake a chrome browser then we get the url page, 
we wait 8 seconds for the website to charge the cookie popup page. Then we define the cookie accept button  with his XPath 
and use click to click on it. 
"""

root_url = "https://immovlan.be/fr/immobilier?transactiontypes=a-vendre,en-vente-publique" 
sales_url = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.6099.129 Safari/537.36"
}
def scrape_page(page_number) :
    url = f"{root_url}&page={page_number}&noindex=1"
    req= requests.get(url, headers=headers)

    if req.status_code == 200 :
        soup = BeautifulSoup(req.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link["href"]
            if "/detail/" in href :
                full_url = "ttps://immovlan.be/fr/immobilier?transactiontypes=a-vendre,en-vente-publique&noindex=1" + href if href.startswith("/") else href
                if full_url not in sales_url :
                    sales_url.append(full_url)       
    else :
        print(f"Error while scrapping page{page_number}. Status code = {req.status_code}")

"""We define how to scrape a page. We us headers to get trough all the pages without being blocked by the website. 
We use a sales_url empty list to append. We noticed a reccurence in the url with the number of the page. We check that we are note
blocked with the status code then parse the content of the page. 
We loop trough it by looking for all the href with /detail/ in it and create the full url if the version found is a small version of it.
"""

for page in range(1, 51) :
    scrape_page(page)
print(len(sales_url))
for url in sales_url :
    print(url)
print(sales_url)

"""We create a final loop to use our scrape_page fonction trough the 50 pages of the website. It won't allow to get all the announces
but we manage to get 613 cleaned urls."""