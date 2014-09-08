import pika
from fetchXml import *
import lowesConfig
import VictoriaConfig

class Producer:
    def __init__(self):      
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='XmlQueue')
        f = FetchXml()
        
        #print lowesConfig.site_map_url
        #url_list = f.getXml(lowesConfig.site_map_url)

        print VictoriaConfig.site_map_url
        url_list = f.extractUrl(VictoriaConfig.site_map_url)
        self.ListUrl(url_list)

    def ListUrl(self,url_list):
        for url in url_list:
            print url
            self.addUrl(url)
            
        print "[Info]Done adding to queue!"
        self.connection.close()

    def addUrl(self,url):
            self.channel.basic_publish(exchange='',
                                  routing_key='XmlQueue',
                                  body=url)
p  = Producer()
