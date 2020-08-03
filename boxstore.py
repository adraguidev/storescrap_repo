from scrappingscript import Scrapper
import pandas as pd

baseurl = "https://thebox.com.pe"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36 '
}

web_scrapping = Scrapper(baseurl, headers)
categories = web_scrapping.get_links("https://thebox.com.pe", "collections", comp='/collections', sw='/')

product_tags = ["grid-view-item grid-view-item--sold-out product-card", "grid-view-item product-card"]

pages_per_cat = web_scrapping.link_pages(categories, product_tags)

products_list = web_scrapping.get_products(pages_per_cat, 'products')

data = web_scrapping.product_data(products_list)

#df = pd.DataFrame(data)

#df['name'] = df['name'].str.replace("\n", '-')
#df['description'] = df['description'].str.replace("\n", '-')
#df['color'] = df['color'].str.replace("\n", '-')
#df['size'] = df['size'].str.replace("\n", '-')

#df.to_csv('theboxstore.csv', encoding="utf-8-sig")
