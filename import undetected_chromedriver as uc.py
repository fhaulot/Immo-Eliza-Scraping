import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import random
import os
from urllib.robotparser import RobotFileParser

# Vérifie si le scraping est autorisé
def is_allowed(url, user_agent="*"):
    rp = RobotFileParser()
    rp.set_url("https://www.immovlan.be/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)

# Lis les URLs à scraper
file_path = "C:\\Users\\fhaul\\Documents\\GitHub\\Immo-Eliza-Scraping\\cleaned_urls.txt"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        sales_url = [line.strip() for line in f if line.strip()]
else:
    print("Fichier 'cleaned_urls.txt' non trouvé.")
    sales_url = []

# Configuration undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = uc.Chrome(options=options)

sales_data = []

for url in sales_url:
    try:
        if not is_allowed(url):
            print(f"⚠️ Accès interdit par robots.txt : {url}")
            continue

        print(f"Scraping : {url}")
        driver.get(url)
        time.sleep(random.uniform(3, 6))  # laisser le JS charger

        soup = BeautifulSoup(driver.page_source, "html.parser")
        data_bloc = soup.find("div", class_="general-info w-100")

        if not data_bloc:
            raise Exception("Bloc de données non trouvé.")

        infos = {'url': url}
        elements = data_bloc.find_all(["h3", "p"])

        for i in range(0, len(elements), 2):
            if elements[i].name == "h3" and elements[i+1].name == "p":
                key = elements[i].get_text(strip=True)
                value = elements[i+1].get_text(strip=True)
                infos[key] = value

        sales_data.append(infos)

    except Exception as e:
        print(f"❌ Erreur avec {url} : {e}")

driver.quit()

# Optionnel : exporter les données en CSV
import pandas as pd
df = pd.DataFrame(sales_data)
df.to_csv("immovlan_scraped_data.csv", index=False, encoding='utf-8')
print("✅ Données sauvegardées dans 'immovlan_scraped_data.csv'")