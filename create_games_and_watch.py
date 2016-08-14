from shared.queueUtils import *
from shared.board import *

connection = getQueueConnection()
channel = connection.channel()
#channel.queue_declare(queue='tzaar_player_1_queue')

games_to_create = 50

import json
def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

for i in range(0, games_to_create):
    data = {}
    data['board'] = getDefaultBoard()
    data['original_board'] = data['board']
    data['turn'] = 1
    data['game_id'] = i
    data['debug_moves'] = []
    channel.basic_publish(exchange='',
                      routing_key='tzaar_player_1_queue',
                      body=json.dumps(data, default=jdefault))


stats = {}
stats['black_wins'] = 0
stats['white_wins'] = 0
stats['total_turns'] = 0
stats['count'] = 0

import time
stats['start'] = time.time()
def callback(ch, method, properties, body):
    dataContainer = json.loads(body.decode('utf-8'))

    if dataContainer['winner'] == BoardItemType.black:
        stats['black_wins'] += 1
    else:
        stats['white_wins'] += 1
    stats['total_turns'] += len(dataContainer['debug_moves'])
    stats['count'] += 1

    if stats['count'] == games_to_create:
        print("Black wins: " + str(stats['black_wins']))
        print("White wins: " + str(stats['white_wins']))
        print("Average turns: " + str(stats['total_turns'] / games_to_create))
        print("Time: " + str(time.time() - stats['start']))


channel.basic_consume(callback,
                      queue='tzaar_results',
                      no_ack=True)
channel.start_consuming()