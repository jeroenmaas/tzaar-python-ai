from shared.board import *
import unittest

class TestAttackMoves(unittest.TestCase):
    def test_leftright(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 5, 5)
        self.assertEqual([4, 5] in moves, True)
        self.assertEqual([6, 5] in moves, True)

        # same loc
        self.assertEqual([5, 5] in moves, False)

        #we cant step over stones..
        self.assertEqual([3, 5] in moves, False)
        self.assertEqual([7, 5] in moves, False)
    def test_topbottom(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 5, 5)
        self.assertEqual([5, 4] in moves, True)
        self.assertEqual([5, 6] in moves, False)

        # same loc
        self.assertEqual([5, 5] in moves, False)
    def test_diagonal(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 6, 3)
        self.assertEqual([7, 4] in moves, True)
        self.assertEqual([5, 2] in moves, False)

        # same loc
        self.assertEqual([6, 3] in moves, False)
    def test_integration(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 7, 7)
        self.assertEqual([8, 7] in moves, True)
        self.assertEqual([7, 6] in moves, True)
        self.assertEqual(len(moves), 2)
    def test_integration2(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 4, 3)
        self.assertEqual([3, 3] in moves, True)
        self.assertEqual([3, 2] in moves, True)
        self.assertEqual([5, 4] in moves, True)
        self.assertEqual(len(moves), 3)

class TestAllMoves(unittest.TestCase):
    def test_leftright(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 4, 5, allow_stacking=True)
        self.assertEqual([3, 5] in moves, True)
        self.assertEqual([5, 5] in moves, True)

        # same loc
        self.assertEqual([4, 5] in moves, False)

        #we cant step over stones..
        self.assertEqual([2, 5] in moves, False)
        self.assertEqual([6, 5] in moves, False)
    def test_topbottom(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 5, 5, allow_stacking=True)
        self.assertEqual([5, 4] in moves, True)
        self.assertEqual([5, 6] in moves, True)

        # same loc
        self.assertEqual([5, 5] in moves, False)
    def test_diagonal(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 6, 3, allow_stacking=True)
        self.assertEqual([7, 4] in moves, True)
        self.assertEqual([5, 2] in moves, True)

        # same loc
        self.assertEqual([6, 3] in moves, False)
    def test_integration(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 7, 7, allow_stacking=True)
        self.assertEqual([6, 7] in moves, True)
        self.assertEqual([8, 7] in moves, True)
        self.assertEqual([7, 6] in moves, True)
        self.assertEqual([7, 8] in moves, True)
        self.assertEqual([6, 6] in moves, True)
        self.assertEqual([8, 8] in moves, True)
        self.assertEqual(len(moves), 6)
    def test_integration2(self):
        board = getDefaultBoard()
        moves = getPossibleMoves(board, 4, 3, allow_stacking=True)
        self.assertEqual([3, 3] in moves, True)
        self.assertEqual([3, 2] in moves, True)
        self.assertEqual([5, 4] in moves, True)
        self.assertEqual([4, 2] in moves, True)
        self.assertEqual([5, 3] in moves, True)
        self.assertEqual(len(moves), 5)

class TestBoard(unittest.TestCase):
    # Added this test because getBoardAfterMove changed original board.
    def test_move_does_not_change_orignal(self):
        board = getDefaultBoard()
        new_board = getBoardAfterMove(board, 0, 1, 0, 0)
        self.assertEqual(new_board[0][1] == board[0][1], False)
    def test_move_happend(self):
        board = getDefaultBoard()
        new_board = getBoardAfterMove(board, 0, 1, 0, 0)
        self.assertEqual(new_board[0][1].type, BoardItemType.free)
        self.assertEqual(new_board[0][0].type, BoardItemType.black)
    def test_get_items(self):
        board = getDefaultBoard()
        items = getItems(board)
        self.assertEqual(len(items), 60)
        new_board = getBoardAfterMove(board, 0, 1, 0, 0, items=items)
        self.assertEquals(len(getItems(new_board)), 59)
        self.assertEquals(len(items), 59)

        # test stacking.
        new_board = getBoardAfterMove(new_board, 5, 6, 6, 6, items=items)
        self.assertEquals(len(getItems(new_board)), 58)
        self.assertEquals(len(items), 58)

        max_stack_1 = 0
        max_stack_2 = 0
        items2 = getItems(new_board)
        for i in range(58):
            item1 = items[i]
            item2 = items2[i]
            if item1.weight > max_stack_1:
                max_stack_1 = item1.weight
            if item2.weight > max_stack_2:
                max_stack_2 = item2.weight
        self.assertEquals(max_stack_1, 2)
        self.assertEquals(max_stack_2, 2)


class TestTurnPosition(unittest.TestCase):
    def test_turn_1(self):
        info = TurnInformation(1)
        self.assertEqual(info.player, BoardItemType.white)
        self.assertEqual(info.opponent, BoardItemType.black)
        self.assertEqual(info.allow_stacking, False)
    def test_turn_2(self):
        info = TurnInformation(2)
        self.assertEqual(info.player, BoardItemType.black)
        self.assertEqual(info.opponent, BoardItemType.white)
        self.assertEqual(info.allow_stacking, False)
    def test_turn_3(self):
        info = TurnInformation(3)
        self.assertEqual(info.player, BoardItemType.black)
        self.assertEqual(info.opponent, BoardItemType.white)
        self.assertEqual(info.allow_stacking, True)
    def test_turn_4(self):
        info = TurnInformation(4)
        self.assertEqual(info.player, BoardItemType.white)
        self.assertEqual(info.opponent, BoardItemType.black)
        self.assertEqual(info.allow_stacking, False)
    def test_turn_5(self):
        info = TurnInformation(5)
        self.assertEqual(info.player, BoardItemType.white)
        self.assertEqual(info.opponent, BoardItemType.black)
        self.assertEqual(info.allow_stacking, True)
    def test_turn_6(self):
        info = TurnInformation(6)
        self.assertEqual(info.player, BoardItemType.black)
        self.assertEqual(info.opponent, BoardItemType.white)
        self.assertEqual(info.allow_stacking, False)

# class TestSpeed(unittest.TestCase):
#     def test_getBoardAfterChange(self):
#         boards = []
#         origins = []
#         targets = []
#         iterations = round(10000 / 30)
#         for i in range(0, iterations):
#             board = getRandomBoard()
#
#             positions = getItemsOfType(board, BoardItemType.black)
#             for position in positions:
#                 possible_moves = getPossibleMoves(board, position[0], position[1], allow_stacking=True)
#                 boards.append(board)
#                 origins.append(position)
#                 targets.append(possible_moves[0])
#
#         import time
#         start_time = time.time()
#         print(len(targets))
#         for i in range(0, len(targets)):
#             board = boards[i]
#             origin = origins[i]
#             target = targets[i]
#             new_board = getBoardAfterMove(board, origin[0], origin[1], target[0], target[1])
#
#         print("--- board generation %s seconds ---" % (time.time() - start_time))
#     def test_getBoardStatsForPlayer(self):
#         boards = []
#         items_for_board = []
#         iterations = 1000
#         for i in range(0, iterations):
#             board = getRandomBoard()
#             items = getItems(board)
#             for i in range(5):
#                 if i == 2 or i == 3:
#                     player = BoardItemType.black
#                 else:
#                     player = BoardItemType.white
#
#                 position = getItemsOfType(board, player)[0]
#                 moves = getPossibleMoves(board, position[0], position[1], allow_stacking=True)
#                 for move in moves:
#                     items = items[:]
#                     new_board = getBoardAfterMove(board, position[0], position[1], move[0], move[1], items=items)
#                     boards.append(new_board)
#                     items_for_board.append(items)
#
#         import time
#         start_time = time.time()
#         print(len(boards))
#         for i in range(len(boards)):
#             getBoardStats(items_for_board[i])
#
#         print("--- Stats %s seconds ---" % (time.time() - start_time))




if __name__ == '__main__':
    unittest.main()

#board = getDefaultBoard()
#print(getPossibleMoves(board, 4, 5))