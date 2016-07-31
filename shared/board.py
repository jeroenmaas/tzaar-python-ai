class BoardResult:
    none = 0
    has_won = 1
    has_lost = 2

class BoardStatsPerPlayer:
    type1_count = None
    type2_count = None
    type3_count = None

    def __init__(self, type1_count, type2_count, type3_count):
        self.type1_count = type1_count
        self.type2_count = type2_count
        self.type3_count = type3_count

    # Returns if the player has lost by the count of its items
    def getHasLost(self):
        if self.type1_count == 0 or self.type2_count == 0 or self.type3_count == 0:
            return True
        return False

    def getLowestCount(self):
        lowest = 500
        if self.type1_count < lowest:
            lowest=self.type1_count
        if self.type2_count < lowest:
            lowest=self.type2_count
        if self.type3_count < lowest:
            lowest=self.type3_count
        return lowest

class TurnInformation:
    turn_number = None
    player = None
    opponent = None
    turns = None

    def __init__(self, turn_number):
        self.turn_number = turn_number

        self.turns = 2
        if turn_number == 1:
            self.turns = 1
            self.player = BoardItemType.white
            self.opponent = BoardItemType.black
        elif turn_number % 4 == 2:
            self.player = BoardItemType.black
            self.opponent = BoardItemType.white
        else:
            self.player = BoardItemType.white
            self.opponent = BoardItemType.black


class BoardItemType:
    none = 0
    free = 1
    white = 2
    black = 3

    @staticmethod
    def display(type):
        if type == BoardItemType.none:
            return "None"
        if type == BoardItemType.free:
            return "Free"
        if type == BoardItemType.white:
            return "White"
        if type == BoardItemType.black:
            return "Black"


class BoardItem:
    type = None         # 'white', 'black', 'none', 'free'
    sub_type = None     # 1, 2, 3 or None for none & free
    Weight = None       # default: 1

    def __init__(self, type, sub_type, weight):
        self.type = type
        self.sub_type = sub_type
        self.weight = weight
    def __repr__(self):
        return 'Type: ' + BoardItemType.display(self.type) + ' sub_type: ' + str(self.sub_type) + ' Weight: ' + str(self.weight)

# Global variable.
board_size = 9

# Reads default board from txt file.
# Used for unittesting and starting the game.
def getDefaultBoard():
    board_file_pointer = open("resources/default-board.txt", "rb")

    board = [None] * board_size
    for x in range(0, board_size):
        board[x] = [None] * board_size

    y = 0
    for line in board_file_pointer.readlines():
        items = str(line).replace("b'", '').replace("'", '').replace('\\n', '').split(' ')
        while('' in items):
            items.remove('')
        x = 0
        for item in items:
            if item[:1] == 'n':
                board[x][y] = BoardItem(BoardItemType.none, None, None)
            if item[:1] == 'f':
                board[x][y] = BoardItem(BoardItemType.free, None, None)
            if item[:1] == 'w':
                board[x][y] = BoardItem(BoardItemType.white, int(item[1:2]), 1)
            if item[:1] == 'b':
                board[x][y] = BoardItem(BoardItemType.black, int(item[1:2]), 1)
            x += 1
        y += 1

    return board

# Checks if its an valide move or that we need to stop looking.
# Returns false if we need to continue looking.
# Adds possible actions to the list.
def validateMove(type, board, x, y, possibleActions, allow_stacking=False):
    position = board[x][y]
    if position.type == BoardItemType.free:
        return True
    elif position.type == BoardItemType.none:
        return False
    elif allow_stacking:
        possibleActions.append([x, y])
        return False
    elif position.type != type:
        possibleActions.append([x, y])
        return False
    else:
        return False

# Returns all available moves. Including those that might not be nice.
# Its needed to evaluate the board and check what is the best move.
def getPossibleMoves(board, x, y, allow_stacking=False):
    origin = board[x][y]
    type = origin.type

    # pos + piece
    possible_actions = []

    # left
    for i in reversed(range(0, x)):
        if validateMove(type, board, i, y, possible_actions, allow_stacking=allow_stacking) is False:
            break

    # right
    for i in range(x+1, board_size):
        if validateMove(type, board, i, y, possible_actions, allow_stacking=allow_stacking) is False:
            break

    # up
    for i in reversed(range(0, y)):
        if validateMove(type, board, x, i, possible_actions, allow_stacking=allow_stacking) is False:
            break

    # down
    for i in range(y+1, board_size):
        if validateMove(type, board, x, i, possible_actions, allow_stacking=allow_stacking) is False:
            break

    # top-left
    for i in range(1, min(x,y)+1):
        if validateMove(type, board, x-i, y-i, possible_actions, allow_stacking=allow_stacking) is False:
            break

    # bottom-right
    for i in range(1, board_size-max(x,y)):
        if validateMove(type, board, x+i, y+i, possible_actions, allow_stacking=allow_stacking) is False:
            break

    return possible_actions

# Returns all items for a certain player. (White/Black)
def getItemsOfType(board, type):
    positions = []
    for x in range(0, board_size):
        for y in range(0, board_size):
            position = board[x][y]
            if position.type == type:
                positions.append([x,y])
    return positions

# Gets a fresh new board after a certain move took place.
# Used for the AI to give a value to the board.
import numpy as np
def getBoardAfterMove(board, x, y, dest_x, dest_y):
    new_board=np.array(board, copy=True).tolist()

    origin = new_board[x][y]
    new_board[x][y] = BoardItem(BoardItemType.free, None, None)
    dest = new_board[dest_x][dest_y]
    if dest.type != origin.type:
        # Check if origin is powerfull enough to take out the destination.
        # If not the case then its by by origin.
        if origin.weight >= dest.weight:
            new_board[dest_x][dest_y] = origin
    else:
        new_board[dest_x][dest_y] = BoardItem(origin.type, origin.sub_type, origin.weight+1)

    return new_board

# Returns BoardResult in players perspective.
# Will most of the time just result BoardResult.none.
def getBoardresult(board, player):
    if player == BoardItemType.black:
        opponent = BoardItemType.white
    else:
        opponent = BoardItemType.black

    if hasPlayerLost(board, opponent):
        return BoardResult.has_won
    elif hasPlayerLost(board, player):
        return BoardResult.has_lost
    else:
        return BoardResult.none

# Returns true or false if a player has lost the game.
# Currently only checks for available items on the board. Not if the player can move. This happends somewhere else.
def hasPlayerLost(board, player):
    board_status = getBoardStatsForPlayer(board, player)
    if board_status.getHasLost():
        return True
    else:
        return False

def getBoardStatsForPlayer(board, player):
    player_positions = getItemsOfType(board, player)
    type1_count = 0
    type2_count = 0
    type3_count = 0
    for pos in player_positions:
        item = board[pos[0]][pos[1]]
        if item.sub_type == 1:
            type1_count += 1
        if item.sub_type == 2:
            type2_count += 1
        if item.sub_type == 3:
            type3_count += 1
    return BoardStatsPerPlayer(type1_count, type2_count, type3_count)
