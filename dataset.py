import pandas as pd
import json
from bs4 import BeautifulSoup
from typing import List, Optional
from collections import namedtuple
from pydantic import BaseModel
import numpy as np


class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    image_url: Optional[str] = None
    stock_quantity:int
    is_available:bool


with open('dataset/scraping_data.json', 'r') as scraping:
    scraping_data = json.loads(scraping.read())

type(scraping_data)
# print(scraping_data[0][0][0].keys())
# scraping_data[0][0][0]['description']
# scraping_data[0][0][0]['Información adicional']

array = []
for category in scraping_data:
    for idx, item in enumerate(category):
        try:
            item_categories = item[0]['categories']
        except Exception as e:
            print(e)
            continue
        if len(item_categories) > 0:
            if len(item_categories[-1].split('/')) == 3:
                item_category = item_categories[-1].replace('/', '')
            else:
                item_category = item_categories[-1].split('/')[1]
        else:
            item_category = ''

        item_description = item[0]['description']

        if item_description:
            item_description_01 = BeautifulSoup(item_description).get_text()
        else:
            item_description_01 = ''

        try:
            price = float(item[0]['items'][0]['sellers'][0]['commertialOffer']['Price'])
        except Exception as e:
            print(e)
            price = float(np.random.randint(5,500))

        item_product = Product(
            name=item[0]['productName'],
            description=item_description_01,
            price=price,
            category=item_category,
            image_url=item[0]['link'],
            stock_quantity=np.random.randint(1, 50),
            is_available=True)
        array.append(item_product.dict())

products = pd.DataFrame(array)
products.description = products.description.astype('string')
products_01 = products[~(products.description.str.len() <= 0)].copy()
# products.description.str.contains('nan').sum()
# ll = products[products.description.str.contains(':')]
# products[products.name.str.contains('na')]

products_01.to_csv(r'products.csv', encoding='utf-8', index=False)


customer = pd.read_excel(r"C:\Users\dante\python\SQL\scripts\app\data\Dim_Customer.xlsx")

customer_01 = customer[['CustomerName', 'Email']].copy()
customer_02 = customer_01.rename(
    columns={'CustomerName':'username',
             'Email':'email'})
customer_02['email'] = customer_02['email'].astype('string')
customer_02['password'] = customer_02['email'].str.split('@').str.get(0)

customer_02.to_csv(r'customers.csv', encoding='utf-8', index=False)


df = pd.read_csv(r"C:\Users\dante\Ecommerce\ecommerce_app\usa.txt", sep='|')
df['First Name'] = df['First Name'].astype('string')
df['First Name'] = df['First Name'].str.replace(' ', '')

df['Last Name'] = df['Last Name'].astype('string')
df['Last Name'] = df['Last Name'].str.replace(' ', '')
user_names = df[['First Name', 'Last Name']].apply(lambda x:' '.join(x), axis=1)


def convert_username(x:str) -> str:
    return x.replace("'", '').lower().replace(' ', '.')



