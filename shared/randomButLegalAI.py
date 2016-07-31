from shared.board import *
import random

def playMove(turn_number, board):
    if turn_number == 1:
        player = BoardItemType.white
        opponent = BoardItemType.black
        turns = 1
    elif turn_number % 4 == 2:
        player = BoardItemType.black
        opponent = BoardItemType.white
        turns = 2
    else:
        player = BoardItemType.white
        opponent = BoardItemType.black
        turns = 2

    moves = []
    hasLost = False
    hasWon = False
    if turns >= 1:
        positions = getItemsOfType(board, player)
        all_options = []
        for pos_info in positions:
            options = getPossibleMoves(board, pos_info[0], pos_info[1])
            for option in options:
                all_options.append([pos_info, option])
        if len(all_options) == 0:
            output = {}
            output['result'] = BoardResult.has_lost
            output['player'] = player
            output['opponent'] = opponent
            output['board'] = board
            output['moves'] = moves
            output['next_turn'] = turn_number + turns
            return output
        option = random.choice(all_options)
        moves.append(option)
        board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1])
    if turns >= 2:
        positions = getItemsOfType(board, player)
        all_options = []
        for pos_info in positions:
            options = getPossibleMoves(board, pos_info[0], pos_info[1], allow_stacking=True)
            for option in options:
                all_options.append([pos_info, option])
        if len(all_options) > 0:
            option = random.choice(all_options)
            moves.append(option)
            board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1])
    output = {}
    output['result'] = getBoardresult(board, player)
    output['player'] = player
    output['opponent'] = opponent
    output['board'] = board
    output['moves'] = moves
    output['next_turn'] = turn_number + turns
    return output