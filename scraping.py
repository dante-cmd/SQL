# selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from pathlib import Path
import time
import re
import json
import requests
import pandas as pd
# downloading names
# from downloading_names import get_names

# Enable Performance Logging in Chrome
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

driver_path = "C:/Users/dante/Downloads/FINANCE/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)
options = Options()
driver = webdriver.Chrome(service=service, options=options)

URL = "https://www.metro.pe"
driver.get(URL)
driver.maximize_window()
nav_element = driver.find_element(by=By.XPATH, value="//nav")
nav_element.click()
time.sleep(0.5)
elements = driver.find_elements(
    by=By.XPATH,
    value='//nav/ul/li//div[contains(@class,"submenuContainer") and contains(@class,"relative")]//section[contains(@class,"menuItemsCategory")]//li//a'
        )

urls = [element.get_attribute("href") for element in elements]
data_category_array = []

for url_category in urls:
    category = True
    try:
        # url_category = element.get_attribute("href")
        driver.get(url_category)
        time.sleep(5)
    except:
        category = False
    
    if not category:
        continue
    
    try:
        counter = 0
        # Equivalent to 500px
        constant = 500 
        url_products = set()
        data_array = []

        while True:
            driver.execute_script(f"window.scrollTo(0, {constant})")
            constant += 500
            time.sleep(2)
            
            logs = driver.get_log("performance")
            
            additional = 0
            for log in logs:
                log_json = json.loads(log["message"])["message"]
                if log_json["method"] == "Network.requestWillBeSent":
                    url_product = log_json["params"]["request"]["url"]
                    search_product = re.search(
                        r'.+api[/]catalog_system[/]pub[/]products[/]search[?]fq[=]productId[:]\d+$',
                        url_product)
                    if search_product:
                        if (url_product not in url_products):
                            print(url_product)
                            try:
                                response = requests.get(url_product)
                                data = json.loads(response.text)
                                data_array.append(data)
                                url_products.add(url_product)
                                additional += 1
                                if (len(data_array) > 60):
                                    break
                            except:
                                pass
            if (additional == 0) or (len(data_array) > 60) or (counter>10):
                break

            counter+=1
        data_category_array.append(data_array)
    except NoSuchElementException as e:
        print(e.msg)
    time.sleep(2)

columns = ['productId', 'productName', 'brand', 'brandId', 'brandImageUrl',
           'linkText', 'productReference', 'productReferenceCode', 'categoryId',
           'productTitle', 'metaTagDescription', 'releaseDate',
           'clusterHighlights', 'productClusters', 'searchableClusters',
           'categories', 'categoriesIds', 'link', 'Descripción', 'ProductData']


# array_data_consol = []
# for items in data_category_array:
#     for item in items:
#         array_data_consol.append(item[0])
# 
# data_frame = pd.json_normalize(array_data_consol, max_level=0)
# data_frame_consol = data_frame[columns].copy()
# data_frame_consol = data_frame_consol.drop_duplicates('productId')
# 
# data_frame_consol.to_parquet('data/DimProduct.parquet', index=False)

with open('wsusu.json','w') as file_:
    
    file_.write(json.dumps(data_category_array))

time.sleep(1)
driver.close()
