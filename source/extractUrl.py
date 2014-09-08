from bs4 import *
import urllib2
from bs4 import BeautifulSoup
import re
from xlwt import Workbook

#uncomment the line which you want script to run.
from VictoriaConfig import *
#from lowesConfig import *

from pymongo import *

class Crawler:
    
    def __init__(self):
        #This variables are present in config.py
        self.title_css_path = title_css_path
        self.img_css_path = img_css_path
        self.price_css_path = price_css_path
        self.brand_css_path = brand_css_path
        self.filename = filename
        self.db_name = db_name
    
    def imgUrlExtract(self,data):
        soup = BeautifulSoup(data)
        if "http:" in str(soup.img["src"]):
            return soup.img["src"]#This is for lowes
        else:
            return "https:"+soup.img["src"]#This is for VS

    def priceExtract(self,data):
        soup = BeautifulSoup(data)
        price = soup.p.text
        #This is to strip the price of all the \n,\t,\r if they exist
        regex = re.compile(r'[\n\t\r]')
        price = regex.sub("",price)
        price = price.replace(" ","")
        #TO extract the the price from "Orig.$48.50Sale$36"
        match = re.search(r'Orig..\d*.\d+', price)
        if match:
            price = match.group()[5:]
        else:
            #If the price is the form "$48.50Sale$36"
            match = re.search(r'.\d+.\d+',price)
            if match:
                price = match.group()

        return price

    def titleExtract(self,data):
        soup = BeautifulSoup(data)
        return soup.h1.text

    def brandExtract(self,data):
        soup = BeautifulSoup(data)
        return soup.h2.text

    def idExtract(self,url):
        if "ProductID" in url:
            urlP = url.rsplit("ProductID=")[1]#This is for VS.com
        if "productId" in url:
            urlP = url.rsplit("productId=")[1]#This is for lowes.com
        PID = urlP.rsplit("&")[0]
        return PID
    
    def categoryExtract(self,url):
        #site_name is in the file config.py
        regex = "https:\/\/"+site_name+"\/\w+"
        match = re.search(regex, url)
        if match:
            return match.group().rsplit("https://"+site_name+"/")[1]
        else:
            return ""

    def extractData(self,url):
        extract_list = []
        response = urllib2.urlopen(url)
        page = response.read()
        soup = BeautifulSoup(page)
        extract_data = {}
            
        img_data = soup.select(self.img_css_path)
        if len(img_data) != 0:
            img_url = self.imgUrlExtract(str(img_data[0]))
            extract_data["img_url"] = img_url
                
        price_data = soup.select(self.price_css_path)
        if len(price_data) != 0:
            price = self.priceExtract(str(price_data[0]))
            extract_data["price"] = price
            
        title_data = soup.select(self.title_css_path)
        if len(title_data) != 0:
            title = self.titleExtract(str(title_data))
            extract_data["title"] = title
            
        brand_data = soup.select(self.brand_css_path)
        if len(brand_data) !=0:
            extract_data["brand"] = self.brandExtract(str(brand_data))
            
        extract_data["page_url"] = url
        extract_data["category"] = self.categoryExtract(url)
        extract_data["product_id"] = self.idExtract(str(url))
    
        print extract_data
        extract_list.append(extract_data)

        #self.xlsWrite(extract_list)
        self.dbWrite(extract_list)

    # this is used to write the data into xls file, PLZ MAKE SURE THAT THERE ARE NO OTHER FILES WITH
    #THE SAME NAME, ie this does not append the exsiting file, it will throw an exception if you do so.
    
    def dbWrite(self,extract_list):
        db = Connection()[self.db_name]["data"]
        db.insert(extract_list)

