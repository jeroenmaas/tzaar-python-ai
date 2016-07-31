import pika
from shared.config import *

def getQueueConnection():
    config = getConfig()
    credentials = pika.PlainCredentials(config['queue_username'], config['queue_password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    return connection