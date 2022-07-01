import pprint
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import pandas as pd

df = pd.read_csv("product-urls.csv")
urls = [list(row) for row in df.values]
urls.insert(0, df.columns.to_list())

i = 1

while i < len(urls):
    url = "".join(urls[i])
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    scraped_product_name = soup.find("h1").string
    product_name = scraped_product_name.strip("\r\n")

    selling_price = soup.select_one(".sellingPrice").string
    remove_selling_usd = selling_price[4:]

    list_price = soup.select_one(".listPrice").string
    remove_list_usd = list_price[4:]

    with open("scraped-prices.csv", "a") as csv_file:
        writer = csv.writer(csv_file, lineterminator="\n")
        date_today = date.today()
        price_row = [date_today, product_name,
                     remove_selling_usd, remove_list_usd, url]
        writer.writerow(price_row)

    i = i + 1
    print(i & " URLs scanned")

df = pd.read_csv("scraped-prices.csv")
prices = [list(row) for row in df.values]
prices.insert(0, df.columns.to_list())
print(prices)