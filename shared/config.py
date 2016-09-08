import mysql.connector

def getConfig():
    config = {}
    config['queue_username'] = 'jeroen'
    config['queue_password'] = 'jerdenen12'
    config['mysql_host'] = '127.0.0.1'
    config['mysql_user'] = 'root'
    config['mysql_password'] = ''
    config['mysql_port'] = '3305'
    config['mysql_database'] = 'tzaar'
    return config

def getMysqlConnection():
    config = getConfig()
    cnx = mysql.connector.connect(user=config['mysql_user'], password=config['mysql_password'], port=config['mysql_port'], host=config['mysql_host'], database=config['mysql_database'])
    return cnx