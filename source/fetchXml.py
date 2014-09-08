import urllib2
from bs4 import BeautifulSoup
import re
import lowesConfig
import VictoriaConfig

class FetchXml:

    def extractUrl(self,url,productId="ProductID"):
        response = urllib2.urlopen(url)
        site_map = response.read()
        soup = BeautifulSoup(site_map)
        locs = soup.find_all("loc")
        valid_url = []
        count = 0
        for item in locs:
            item = str(item)
            #<loc>https://www.victoriassecret.com/panties/free-t-shirt-thong-panty/thong-panty-everyday-perfect?ProductID=200758&amp;CatalogueType=OLS</loc>
            #To strip the <loc> tags from the url.
            item = item[5:-6]
            count += 1
            check = re.search(productId,item)
            if check:
                check1 = re.search("&amp",item)
                if check1:
                    item = re.sub("&amp;","&",item)
                valid_url.append(item)
                    
        return valid_url

    def getXml(self,url):
        response = urllib2.urlopen(url)
        site_map = response.read()
        soup = BeautifulSoup(site_map)
        locs = soup.find_all("loc")
        eurls = []
        #This is the a sample item.
        #<loc>http://www.lowes.com/detail8.xml</loc>
        for item in locs:
            item = str(item)
            item = item[5:-6]#This is used to strip away <loc> and </loc>
            match = re.search(r'/detail\d+',item)
            if match:
                extracted_urls = self.extractUrl(item,"productId")
                eurls.append(extracted_urls)
        
        valid_urls = []
        for item1 in eurls:
            for item2 in item1:
                    valid_urls.append(item2)

        return valid_urls

