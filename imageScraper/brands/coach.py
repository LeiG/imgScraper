"""
Image scraper specifically for www.coach.com
"""
import re
import math
from collections import defaultdict
from bs4 import BeautifulSoup

from ..base import BaseScraper


class CoachScraper(BaseScraper):
    def __init__(self, *args, **kwargs):
        self.url = 'http://www.coach.com/'
        self.brand = 'Coach'
        super(CoachScraper, self).__init__(*args, **kwargs)

    def getCategoryList(self, bsObj):
        for cat in bsObj.findAll('a', {'data-id':re.compile('^category-'), 'class':'level-2'}):
            catName = re.sub('category-', '', cat.attrs['data-id'])
            self.categoryList[catName] = cat.attrs['href']

    def getProductList(self, bsObj):
        productList = defaultdict(str)
        for prod in bsObj.findAll('h2'):
            if prod.find('a', {'class':'name-link'}) is not None:
                prodUrl = prod.find('a').attrs['href']
                try:
                    prodName = re.search('/([A-Za-z0-9]+?)\.html', prodUrl).group(1)
                    productList[prodName] = prodUrl
                except AttributeEr:
                    pass
        return productList

    def getImageList(self, bsObj):
        imageList = defaultdict(str)
        imageCounter = 0
        for img in bsObj.findAll('img', {'data-large-image':re.compile('.+')}):
            if img.attrs['class'][0] != 'set-to-fullscreen':
                imageList[str(imageCounter)] = img.attrs['data-large-image']
                imageCounter += 1
        return imageList

    def getPrice(self, bsObj):
        # if on sale
        try:
            price = bsObj.find('span', {'class':'standardprice'}).text
            price = re.search(r'\$([0-9]+?)\n', price, re.M).group(1)

            salePrice = bsObj.find('span', {'class':'salesprice'}).text
            salePrice = re.search(r'\$([0-9]+?)\n', salePrice, re.M).group(1)

            return math.ceil(float(price)), math.ceil(float(salePrice))
        # not on sale
        except AttributeError:
            try:
                price = bsObj.find('span', {'class':'price-sales'}).text
                price = re.search(r'\$([0-9]+?)\n', price, re.M).group(1)
            except AttributeError:
                price = 0

            salePrice = price
            return math.ceil(float(price)), math.ceil(float(salePrice))
