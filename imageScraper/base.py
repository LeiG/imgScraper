"""
Base scraper to traverse pages and save images to file.
"""
import os
import time
import random
import requests
import shutil
import datetime
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from collections import defaultdict
from sqlalchemy import and_

from .defTable import Image

# set default header to look like human
HEADER = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
          "Referrer" : "http://www.google.com/",
          "Accept-Language" : "en-US,en;q=0.8"}


class BaseScraper(object):
    def __init__(self, mainPath, session, header = HEADER):
        self.header = header
        self.mainPath = mainPath
        self.session = session
        self.categoryList = defaultdict(str)

        # create folder for the brand if not exist
        self.brandPath = os.path.join(self.mainPath, self.brand)
        if not os.path.exists(self.brandPath):
            os.mkdir(self.brandPath)

    def getCategoryList(self, bsObj):
        pass

    def traverseCategory(self, cat, catUrl, catPath):
        print("Category", cat)
        response = requests.get(catUrl, headers = self.header)

        try:
            bsObj = BeautifulSoup(response.content, "html.parser")
            productList = self.getProductList(bsObj)

            # traverse all products in this category
            for key, value in productList.items():
                print("Product", key)
                price, salePrice = self.getProductInfo(cat, key, value)
                self.saveRecord(cat, key, value, price, salePrice)
        except HTTPError:
            print("Encountered error at " + catUrl + "! Try again in 5 min...")

            time.sleep(5 * random.randint(55, 65))
            self.traverseCategory(cat, catUrl, catPath)

    def getProductList(self, bsObj):
        productList = defaultdict(str)
        return productList

    def getProductInfo(self, cat, prod, prodUrl):
        response = requests.get(prodUrl, headers = self.header)
        bsObj = BeautifulSoup(response.content, "html.parser")

        price, salePrice = self.getPrice(bsObj)
        return price, salePrice

    def getPrice(self, bsObj):
        pass

    def saveImages(self, url, imagePath):
        os.mkdir(imagePath)

        response = requests.get(url, headers = self.header)
        bsObj = BeautifulSoup(response.content, "html.parser")

        imageList = self.getImageList(bsObj)

        for key, value in imageList.items():
            # save the main image separately in the category folder
            if key == '0':
                with open(imagePath + '.png', 'wb') as content:
                    content.write(requests.get(value).content)
            with open(os.path.join(imagePath, key + '.png'), 'wb') as content:
                content.write(requests.get(value).content)

    def getImageList(self, bsObj):
        imageList = defaultdict(str)
        return imageList

    def getImagePath(self, category, code, price, salePrice):
        return os.path.join(self.brandPath, category,
                            code + "-price-" + str(price) + "-sale-" + str(salePrice))

    def saveRecord(self, category, code, url, price, salePrice):
        # create new record
        if self.session.query(Image).filter(and_((Image.brand == self.brand), (Image.code == code))).count() == 0:

            imagePath = self.getImagePath(category, code, price, salePrice)
            self.saveImages(url, imagePath)

            image = Image(brand = self.brand,
                          category = category,
                          code = code,
                          sourceUrl = url,
                          eventDate = datetime.datetime.now().date(),
                          price = price,
                          salePrice = salePrice,
                          imagePath = imagePath)
            self.session.add(image)
            self.session.commit()

        # update existing record
        else:
            tmpProduct = self.session.query(Image).filter(and_((Image.brand == self.brand), (Image.code == code))).one()
            # skip if price doesn't change
            if tmpProduct.price == price and tmpProduct.salePrice == salePrice:
                pass
            else:
                # remove existing folder
                shutil.rmtree(tmpProduct.imagePath)

                imagePath = self.getImagePath(category, code, price, salePrice)
                self.saveImages(url, imagePath)

                # update database
                tmpProduct.sourceUrl = url
                tmpProduct.eventDate = datetime.datetime.now().date()
                tmpProduct.price = price
                tmpProduct.selfsalePrice = salePrice
                tmpProduct.imagePath = imagePath
                self.session.commit()

    def traverseSite(self):
        response = requests.get(self.url, headers = self.header)

        # validate website access
        assert response.status_code == 200
        print("Happy Shopping!")

        bsObj = BeautifulSoup(response.content, "html.parser")

        self.getCategoryList(bsObj)

        # traverse the category list
        for key, value in self.categoryList.items():
            # create folder for the category if not already exists
            catPath = os.path.join(self.brandPath, key)
            if not os.path.exists(catPath):
                os.mkdir(catPath)

            self.traverseCategory(key, value, catPath)
