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
        print(moves)
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


if __name__ == '__main__':
    unittest.main()

#board = getDefaultBoard()
#print(getPossibleMoves(board, 4, 5))