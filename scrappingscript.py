import requests
from bs4 import BeautifulSoup
import csv
import urllib3
import re
from datetime import datetime

startTime = datetime.now()

class Scrapper:
    """
    Clase Scrapper
    """
    def __init__(self, baseurl, headers,filename):
        self.baseurl = baseurl
        self.headers = headers
        self.filename = filename


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
            cat_links = [
                e.get('href') for e in soup.find_all('a')
                if e.get('href') and contains in e.get('href')
            ]
            category_links += cat_links
        category_links = set(category_links)
        
        for x in category_links:
            if x.startswith('https'):
                product_links.append(x)
            else:
                product_links.append(self.baseurl + x)
        return product_links

    def product_data(self, product_list,name_tag ,name_class ,price_tag ,price_class ,description_tag ,description_class):
        """

        :param product_list:
        :return:
        """
        print(f'Se extraeran: {len(product_list)} articulos')
        file = open(self.filename, 'w',newline='')
        writer = csv.writer(file)
        writer.writerow(['name', 'price', 'description' ,'options', 'link'])


        count = 0

        for product in product_list[0:len(product_list)+1]:
            r = requests.get(product, headers=self.headers)
            soup = BeautifulSoup(r.content, 'lxml')
            print(f'Extrayendo data de : {product}')
            name = soup.find(name_tag,
                             class_=name_class).text.strip()
            print(f'Nombre de Producto: {name}')
            if soup.find(price_tag, class_=price_class):
                price = soup.find(
                    price_tag, class_=price_class).text.strip()
            else:
                price = "Sin información"
            description = soup.find(
                description_tag, class_=description_class).text.strip()
            #options = soup.find(
            #    'select',
            #    class_=
            #    "single-option-selector single-option-selector-product-template product-form__input"
            #).text.strip()
            writer.writerow([name.replace("\n", ' '), price.replace("\n", ' '), description.replace("\n", ' '), product.replace("\n", ' ')])
            
            count += 1
            percentage = (count/len(product_list))*100
            print("Porcentaje: " + "{:12.2f}".format(percentage) + "%")
            
        return print(f'Productos totales: {count}, Tiempo total: '+ str(datetime.now() - startTime))