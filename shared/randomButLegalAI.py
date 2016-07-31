from shared.board import *
import random

def playMove(board, turnInfo: TurnInformation):
    moves = []
    if turnInfo.turns >= 1:
        positions = getItemsOfType(board, turnInfo.player)
        all_options = []
        for pos_info in positions:
            options = getPossibleMoves(board, pos_info[0], pos_info[1])
            for option in options:
                all_options.append([pos_info, option])
        if len(all_options) == 0:
            output = {}
            output['result'] = BoardResult.has_lost
            output['board'] = board
            output['moves'] = moves
            return output
        option = random.choice(all_options)
        moves.append(option)
        board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1])
    if turnInfo.turns >= 2:
        positions = getItemsOfType(board, turnInfo.player)
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
    output['result'] = getBoardresult(board, turnInfo.player)
    output['board'] = board
    output['moves'] = moves
    return output