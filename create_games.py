from shared.queueUtils import *
from shared.board import *

connection = getQueueConnection()
channel = connection.channel()
#channel.queue_declare(queue='tzaar_player_1_queue')

import json
def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

for i in range(0, 50):
    data = {}
    data['board'] = getDefaultBoard()
    data['turn'] = 1
    data['game_id'] = i
    data['debug_moves'] = []
    channel.basic_publish(exchange='',
                      routing_key='tzaar_player_1_queue',
                      body=json.dumps(data, default=jdefault))
connection.close()