import pika
from extractUrl import *


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='XmlQueue')
c = Crawler()
def callback(ch, method, properties, body):
    print "[Received]", body
    url = body
    c.extractData(url)
    print " [x] Done"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='XmlQueue',
                      no_ack=True)

channel.start_consuming()
