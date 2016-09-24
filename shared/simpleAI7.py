from shared.board import *
import random
from pprint import pprint

def playMove(board, turnInfo: TurnInformation):
    turns = 2
    if turnInfo.turns == 1:
        turns = 1

    moves_info = alphabeta(board, turns, -1, 101, turnInfo.player, turnInfo.turn_number, [], getItems(board))
    print('original win chance: ' + str(moves_info[0]))
    options_and_values = moves_info[2]

    from operator import itemgetter, attrgetter, methodcaller
    sorted_options = sorted(options_and_values, key=lambda x: x[0], reverse=True)
    v = 5
    best_moves = None
    index = 0
    last_index = None
    for option in sorted_options:
        move = option[1][0]
        test_board = getBoardAfterMove(board, move[0][0], move[0][1], move[1][0], move[1][1])
        if turns == 2:
            move = option[1][1]
            test_board = getBoardAfterMove(test_board, move[0][0], move[0][1], move[1][0], move[1][1])
        test_turn = TurnInformation(turnInfo.turn_number + turns)
        moves_info = alphabeta(test_board, 2, -1, 101, test_turn.player, test_turn.turn_number, [], getItems(test_board))
        value = moves_info[0]
        if value < v:
            best_moves = option[1]
            v = value
            last_index = index
        index += 1

    print('index: ' + str(last_index))
    print('their win chance: ' + str(v))
    print('our win chance: ' + str(sorted_options[last_index][0]))

    # This is the case where there are no more moves left to make.
    if moves_info[0] == 0:
        output = {}
        output['result'] = BoardResult.has_lost
        output['board'] = board
        output['moves'] = []
        return output

    moves = []
    if turnInfo.turns >= 1:
        chosen_option = best_moves[0]
        moves.append(chosen_option)
        board = getBoardAfterMove(board, chosen_option[0][0], chosen_option[0][1], chosen_option[1][0], chosen_option[1][1])

    if turnInfo.turns >= 2:
        chosen_option = best_moves[1]
        moves.append(chosen_option)
        board = getBoardAfterMove(board, chosen_option[0][0], chosen_option[0][1], chosen_option[1][0], chosen_option[1][1])

    output = {}
    output['result'] = getBoardresult(board, turnInfo.player)
    output['board'] = board
    output['moves'] = moves
    return output

def getPossibleMovesForPlayer(board, player: BoardItemType, allow_stacking):
    positions = getItemsOfType(board, player)
    all_options = []
    for pos_info in positions:
        options = getPossibleMoves(board, pos_info[0], pos_info[1], allow_stacking=allow_stacking)
        for option in options:
            all_options.append([pos_info, option])
    return all_options



import numpy as np
def alphabeta(board, depth, a, b, player, turn_number, returned_options, items):
    if depth == 0:
        turn_info = TurnInformation(turn_number-1)
        return [rateBoardForPlayer(board, turn_info.player, turn_info.opponent, items), returned_options]

    turn_info = TurnInformation(turn_number)
    options = getPossibleMovesForPlayer(board, turn_info.player, allow_stacking=turn_info.allow_stacking)
    if len(options) == 0:
        return [0, []]

    # we are maximizing our return.
    selected_move = None
    previous_moves = None
    total_move_scores = []
    if player == turn_info.player:
        v = -1
        for option in options:
            test_items = items[:]
            test_board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1], items=test_items)
            result = alphabeta(test_board, depth-1, a, b, player, turn_number+1, returned_options, test_items)
            total_move_scores.append([result[0], combineMoves(option, result[1])])
            if result[0] > v:
                v = result[0]
                selected_move = option
                previous_moves = result[1]
            a = max(a, v)
            if b <= a:
                break
    else:
        v = 101
        for option in options:
            test_items = items[:]
            test_board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1], items=test_items)
            result = alphabeta(test_board, depth-1, a, b, player, turn_number+1, returned_options, test_items)
            if result[0] < v:
                v = result[0]
                selected_move = option
                previous_moves = result[1]
            b = min(b, v)
            if b <= a:
                break

    returned_options = []
    returned_options.append(selected_move)
    for moves in previous_moves:
        returned_options.append(moves)
    return [v, returned_options, total_move_scores]

def combineMoves(new_move, previous_moves):
    combined_moves = []
    combined_moves.append(new_move)
    for moves in previous_moves:
        combined_moves.append(moves)
    return combined_moves

try:
    import pickle
    clf_f = open("classifiers/sample2_2.pickle", "rb")
    clf = pickle.load(clf_f)
except OSError as e:
    print("No preloaded classifier available. Please build a new one.")
    quit()

#return between 0 and 1. 1 is very good and 0 is very bad.
cache = {}
def rateBoardForPlayer(board, player: BoardItemType, opponent: BoardItemType, items):
    stats = getBoardStats(items)
    stats_player = stats[player]
    stats_opponent = stats[opponent]
    if stats_opponent.getHasLost():
        return 1
    elif stats_player.getHasLost():
        return 0

    features = []
    features.append(stats_player.type1_count)
    features.append(stats_player.type1_max_weight)
    features.append(stats_player.type2_count)
    features.append(stats_player.type2_max_weight)
    features.append(stats_player.type3_count)
    features.append(stats_player.type3_max_weight)
    features.append(stats_opponent.type1_count)
    features.append(stats_opponent.type1_max_weight)
    features.append(stats_opponent.type2_count)
    features.append(stats_opponent.type2_max_weight)
    features.append(stats_opponent.type3_count)
    features.append(stats_opponent.type3_max_weight)

    feature_str = ''.join('{:01x}'.format(x) for x in features)
    if feature_str in cache:
        return cache[feature_str]

    value = clf.predict([features])[0]
    cache[feature_str] = value

    return value