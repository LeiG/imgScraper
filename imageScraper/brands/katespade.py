"""
Image scraper specifically for www.coach.com
"""
import re
import math
from collections import defaultdict
from bs4 import BeautifulSoup

from ..base import BaseScraper


class KateSpadeScraper(BaseScraper):
    def __init__(self, *args, **kwargs):
        self.url = 'https://www.katespade.com/'
        self.brand = 'KateSpade'
        super(KateSpadeScraper, self).__init__(*args, **kwargs)

    def getCategoryList(self, bsObj):
        for cat in bsObj.findAll('a', {'class':'level-2'}):
            catUrl = cat.attrs['href']
            if 'view-all' in catUrl:
                catName = re.search('/([a-z\-]+?)/view\-all', catUrl).group(1)
                self.categoryList[catName] = catUrl

    def getProductList(self, bsObj):
        productList = defaultdict(str)
        for prod in bsObj.findAll('a', {'class':'name-link'}):
            prodUrl = prod.attrs['href']
            try:
                prodName = re.search('/([A-Za-z0-9]+?)\.html', prodUrl).group(1)
                productList[prodName] = prodUrl
            except AttributeError:
                pass
        return productList

    def getImageList(self, bsObj):
        imageList = defaultdict(str)
        imageCounter = 0
        for img in bsObj.findAll('a', {'class':'thumbnail-link'}):
            imageList[str(imageCounter)] = img.attrs['href']
            imageCounter += 1
        return imageList

    def getPrice(self, bsObj):
        # if on sale
        try:
            price = bsObj.find('span', {'class':'price-standard'}).text
            price = re.search('\$([0-9\.]+?)$', price).group(1)

            salePrice = bsObj.find('span', {'class':'price-sales'}).text
            salePrice = re.search('\$([0-9\.]+?)$', salePrice).group(1)

            return math.ceil(float(price)), math.ceil(float(salePrice))
        # not on sale
        except:
            price = bsObj.find('span', {'class':'price-sales'}).text
            price = re.search('\$([0-9\.,]+?)$', price).group(1)

            salePrice = price
            return math.ceil(float(price)), math.ceil(float(salePrice))
