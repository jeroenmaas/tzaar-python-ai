from shared.queueUtils import *
from shared.board import *
import shared.simpleAI4
import json

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

def callback(ch, method, properties, body):
    dataContainer = json.loads(body.decode('utf-8'))
    game_id = dataContainer['game_id']
    board = dataContainer['board']
    turn = dataContainer['turn']
    debug_moves = dataContainer['debug_moves']

    for x in range(0, board_size):
        for y in range(0, board_size):
            item = board[x][y]
            board[x][y] = BoardItem(item['type'], item['sub_type'], item['weight'])

    turn_info = TurnInformation(turn)

    import time
    start_time = time.time()
    output = shared.simpleAI4.playMove(board, turn_info)
    print("--- %s seconds ---" % (time.time() - start_time))

    new_state = {}
    new_state['game_id'] = game_id
    new_state['board'] = output['board']
    new_state['turn'] = turn_info.turn_number + turn_info.turns
    new_state['debug_moves'] = debug_moves + output['moves']
    new_state['original_board'] = dataContainer['original_board']

    if output['result'] == BoardResult.none:
        channel.basic_publish(exchange='',
                               routing_key='tzaar_player_1_queue',
                               body=json.dumps(new_state, default=jdefault))
        ch.basic_ack(delivery_tag = method.delivery_tag)
    else:
        if output['result'] == BoardResult.has_lost:
            new_state['winner'] = turn_info.opponent
            print("LOSE")
        else:
            new_state['winner'] = turn_info.player
            print("WIN")

        channel.basic_publish(exchange='',
                              routing_key='tzaar_results',
                              body=json.dumps(new_state, default=jdefault))
        ch.basic_ack(delivery_tag = method.delivery_tag)


connection = getQueueConnection()
channel = connection.channel()
channel.basic_qos(prefetch_count=10)
channel.basic_consume(callback,
                      queue='tzaar_player_2_queue',
                      no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()