from shared.board import *
import random
from pprint import pprint

def playMove(board, turnInfo: TurnInformation):
    turns = 2
    if turnInfo.turns == 1:
        turns = 1

    moves_info = alphabeta(board, turns, -1, 101, turnInfo.player, turnInfo.turn_number, [])

    # This is the case where there are no more moves left to make.
    if moves_info[0] == 0:
        output = {}
        output['result'] = BoardResult.has_lost
        output['board'] = board
        output['moves'] = []
        return output

    moves = []
    if turnInfo.turns >= 1:
        chosen_option = moves_info[1][0]
        moves.append(chosen_option)
        print(chosen_option)
        board = getBoardAfterMove(board, chosen_option[0][0], chosen_option[0][1], chosen_option[1][0], chosen_option[1][1])

    if turnInfo.turns >= 2:
        chosen_option = moves_info[1][1]
        moves.append(chosen_option)
        print(chosen_option)
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
def alphabeta(board, depth, a, b, player, turn_number, returned_options):
    if depth == 0:
        turn_info = TurnInformation(turn_number-1)
        return [rateBoardForPlayer(board, turn_info.player, turn_info.opponent), returned_options]

    turn_info = TurnInformation(turn_number)
    options = getPossibleMovesForPlayer(board, turn_info.player, allow_stacking=turn_info.allow_stacking)
    if len(options) == 0:
        return [0, []]

    # we are maximizing our return.
    selected_move = None
    previous_moves = None
    if player == turn_info.player:
        v = -1
        for option in options:
            test_board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1])
            result = alphabeta(test_board, depth-1, a, b, player, turn_number+1, returned_options)
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
            test_board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1])
            result = alphabeta(test_board, depth-1, a, b, player, turn_number+1, returned_options)
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
    return [v, returned_options]

try:
    import pickle
    clf_f = open("classifiers/sample2.pickle", "rb")
    clf = pickle.load(clf_f)
except OSError as e:
    print("No preloaded classifier available. Please build a new one.")
    quit()

#return between 0 and 1. 1 is very good and 0 is very bad.
cache = {}
def rateBoardForPlayer(board, player: BoardItemType, opponent: BoardItemType):
    stats_player = getBoardStatsForPlayer(board, player)
    stats_opponent = getBoardStatsForPlayer(board, opponent)
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
