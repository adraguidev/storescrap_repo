from scrappingscript import Scrapper
import pandas as pd
import random

def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]
    return random.choice(uastrings)   

baseurl = "https://www.strata.com.pe"
headers = {'User-Agent': GET_UA()}
webpage_to_extract = "https://www.strata.com.pe"
categories_name = "collections"
subdirectory ="/collections"
#Can be "http" or "/"
starts_with = '/'
#if it is more than one, it has to be a list
products_tags = ["ProductItem__Wrapper"]
#--------------------------------------------#
name_tag = "h1"
name_class = "ProductMeta__Title Heading u-h2"
price_tag = 'span'
price_class = ["ProductMeta__Price Price Price--highlight Text--subdued u-h4", "ProductMeta__Price Price Text--subdued u-h4"]
description_tag = 'div'
description_class = "ProductMeta__Description"


web_scrapping = Scrapper(baseurl, headers)
categories = web_scrapping.get_links(webpage_to_extract, categories_name, comp=subdirectory, sw=starts_with)
pages_per_cat = web_scrapping.link_pages(categories, products_tags)

products_list = web_scrapping.get_products(pages_per_cat, 'products')

data = web_scrapping.product_data(products_list,name_tag ,name_class ,price_tag ,price_class ,description_tag ,description_class)