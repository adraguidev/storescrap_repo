import requests
from bs4 import BeautifulSoup
import csv
import urllib3
import re

class Scrapper:
    """
    Clase Scrapper
    """
    def __init__(self, baseurl, headers):
        self.baseurl = baseurl
        self.headers = headers

    # url = url from store
    # comp = ubication of categories, ex = '/collections'
    # sw = starts with can be https default, "/" for subdirectories or left it empty

    def get_links(self, url, contains, comp='', sw='https'):
        """
        :param url:
        :param contains:
        :param comp:
        :param sw:
        :return:
        """
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')
        category_links = []
        links = [
            e.get('href')
            for e in soup.find_all('a')
            if e.get('href') and f'{contains}' in e.get('href')
        ]
        for link in links:
            if sw == 'https':
                category_links.append(link)
            elif sw == '/':
                category_links.append(self.baseurl + link)
                # print(re.match(r"(ftp|http|https)://.*\.(pe|com|net)", self.url))
                # category_links.append(a+_)
                # print(category_links)
            else:
                category_links.append(url + link)

        def fix_links(links_list):
            """

            :param links_list:
            :return:
            """
            fixed = []
            for x in links_list:
                if x.startswith(f'{self.baseurl}{comp}'):
                    fixed.append(x)
                else:
                    continue
            return fixed

        return fix_links(category_links)

    def link_pages(self, categories, products_tags):
        """

        :param categories:
        :param products_tags:
        :return:
        """
        pages_links = []
        for category in categories:
            for x in range(1, 200):
                r = requests.get(f"{category}?page={x}", headers=self.headers)
                soup = BeautifulSoup(r.content, 'lxml')
                if soup.find_all('div', {"class": products_tags}):
                    pages_links.append(f"{category}?page={x}")
                else:
                    break
        return pages_links

    def get_products(self, links, contains):
        """

        :param links:
        :param contains:
        :return:
        """
        category_links = []
        product_links = []
        for x in links:
            print(x)
            r = requests.get(f"{x}", headers=self.headers)
            soup = BeautifulSoup(r.content, 'lxml')
            links = [
                e.get('href') for e in soup.find_all('a')
                if e.get('href') and contains in e.get('href')
            ]
            category_links += links
        for x in category_links:
            if x.startswith('https'):
                product_links.append(x)
            else:
                product_links.append(self.baseurl + x)
        return product_links

    def product_data(self, product_list):
        """

        :param product_list:
        :return:
        """

        file = open('./boxscrap.csv', 'w',newline='')
        writer = csv.writer(file)
        writer.writerow(['name', 'price', 'description' ,'options', 'link'])

        #products_info = []
        count = 0
        for product in product_list:
            r = requests.get(product, headers=self.headers)
            soup = BeautifulSoup(r.content, 'lxml')
            print(f'Extrayendo data de : {product}')
            name = soup.find('h1',
                             class_='product-single__title').string.strip()
            print(f'Nombre de Producto: {name}')
            price = soup.find(
                'span', class_="price-item price-item--sale").text.strip()
            description = soup.find(
                'div', class_="product-single__description rte").text.strip()
            options = soup.find(
                'select',
                class_=
                "single-option-selector single-option-selector-product-template product-form__input"
            ).text.strip()
            writer.writerow([name.encode('utf-8'), price.encode('utf-8'), description.encode('utf-8'), options.encode('utf-8'), product.encode('utf-8')])

            #product = {
            #    'name': name,
            #    'price': price,
            #    'description': description,
            #    'options': options,
            #    'size': size,
            #    'link': product
            #}
            
            count += 1
            print(count)
            #products_info.append(product)
        return f'Total Products {count}'