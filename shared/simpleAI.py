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

        best_option = None
        best_board = None
        best_value = None
        for option in all_options:
            test_board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1])
            board_value = rateBoardForPlayer(board, turnInfo.player, turnInfo.opponent)
            if best_value is None or board_value > best_value:
                best_value = board_value
                best_board = test_board
                best_option = option
        option = best_option
        board = best_board
        moves.append(option)

    if turnInfo.turns >= 2:
        positions = getItemsOfType(board, turnInfo.player)
        all_options = []
        for pos_info in positions:
            options = getPossibleMoves(board, pos_info[0], pos_info[1], allow_stacking=True)
            for option in options:
                all_options.append([pos_info, option])
        if len(all_options) > 0:
            best_option = None
            best_board = None
            best_value = None
            for option in all_options:
                test_board = getBoardAfterMove(board, option[0][0], option[0][1], option[1][0], option[1][1])
                board_value = rateBoardForPlayer(test_board, turnInfo.player, turnInfo.opponent)
                if best_value is None or board_value > best_value:
                    best_value = board_value
                    best_board = test_board
                    best_option = option

            option = best_option
            board = best_board
            moves.append(option)
    output = {}
    output['result'] = getBoardresult(board, turnInfo.player)
    output['board'] = board
    output['moves'] = moves
    return output

#return between 0 and 1. 1 is very good and 0 is very bad.
def rateBoardForPlayer(board, player: BoardItemType, opponent: BoardItemType):
    stats_player = getBoardStatsForPlayer(board, player)
    stats_opponent = getBoardStatsForPlayer(board, opponent)
    if stats_opponent.getHasLost():
        return 1
    elif stats_player.getHasLost():
        return 0

    lowest_player_count = stats_player.getLowestCount()
    lowest_opponent_count = stats_opponent.getLowestCount()
    diff = lowest_player_count - lowest_opponent_count
    if diff > 0:
        return 0.5 + (0.5 - 0.45/diff)
    elif diff < 0:
        return 0.45/abs(diff)
    else:
        return 0.5
