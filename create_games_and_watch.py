from shared.queueUtils import *
from shared.board import *

connection = getQueueConnection()
channel = connection.channel()
#channel.queue_declare(queue='tzaar_player_1_queue')

games_to_create = 10

import json
def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

for i in range(0, games_to_create):
    data = {}
    data['board'] = getRandomBoard()
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

mysql_con = getMysqlConnection()
def callback(ch, method, properties, body):
    dataContainer = json.loads(body.decode('utf-8'))

    if dataContainer['winner'] == BoardItemType.black:
        stats['black_wins'] += 1
    else:
        stats['white_wins'] += 1
    stats['total_turns'] += len(dataContainer['debug_moves'])
    stats['count'] += 1

    original_board = convertJSONBoardToObjBoard(dataContainer['original_board'])
    new_board = None
    turn = 0
    for item in dataContainer['debug_moves']:
        continue
        if new_board == None:
            new_board = original_board
        new_board = getBoardAfterMove(new_board, item[0][0], item[0][1], item[1][0], item[1][1])
        turn += 1
        turn_info = TurnInformation(turn)
        if turn_info.player == BoardItemType.black:
            player_stats = getBoardStatsForPlayer(new_board, BoardItemType.black)
            opponent_stats = getBoardStatsForPlayer(new_board, BoardItemType.white)
            has_won = dataContainer['winner'] == BoardItemType.black
        else:
            player_stats = getBoardStatsForPlayer(new_board, BoardItemType.white)
            opponent_stats = getBoardStatsForPlayer(new_board, BoardItemType.black)
            has_won = dataContainer['winner'] == BoardItemType.white
        new_array =[]
        new_array.append(player_stats.type1_count)
        new_array.append(player_stats.type1_max_weight)
        new_array.append(player_stats.type2_count)
        new_array.append(player_stats.type2_max_weight)
        new_array.append(player_stats.type3_count)
        new_array.append(player_stats.type3_max_weight)
        new_array.append(opponent_stats.type1_count)
        new_array.append(opponent_stats.type1_max_weight)
        new_array.append(opponent_stats.type2_count)
        new_array.append(opponent_stats.type2_max_weight)
        new_array.append(opponent_stats.type3_count)
        new_array.append(opponent_stats.type3_max_weight)
        feature_str = ''.join('{:01x}'.format(x) for x in new_array)

        cursor = mysql_con.cursor()
        wins = str(int(has_won))
        loses = str(int(has_won == False))

        query = 'INSERT INTO samples_2 (features, wins, loses) VALUES ("' + feature_str + '", ' + wins + ', ' + loses + ')'
        query += ' ON DUPLICATE KEY UPDATE'
        if has_won:
            query += ' wins=wins+1'
        else:
            query += ' loses=loses+1'
        cursor.execute(query)
        cursor.close()
        mysql_con.commit()


    if stats['count'] == games_to_create:
        print("Black wins: " + str(stats['black_wins']))
        print("White wins: " + str(stats['white_wins']))
        print("Average turns: " + str(stats['total_turns'] / games_to_create))
        print("Time: " + str(time.time() - stats['start']))
        mysql_con.close()


channel.basic_qos(prefetch_count=100)
channel.basic_consume(callback,
                      queue='tzaar_results',
                      no_ack=True)
channel.start_consuming()