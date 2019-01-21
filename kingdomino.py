
STARTING_TILE = 6

# 0 - Wheat field
# 1 - Plain
# 2 - Lake
# 3 - Swamp
# 4 - Forest
# 5 - Mountain
# 6 - Kingdom


class Tile:
    def __init__(self, type, crowns=0):
        self.type = type # 0-6, 0-5 are landscapes, 6 is starting tile
        self.crowns = crowns
        
    def copy(self):
        return Tile(self.type, self.crowns)
  
class Board:
    def __init__(self, sx=0, sy=0):
        self.board = [[None] * 5 for _ in range(5)]
        self.board[sx][sy] = Tile(STARTING_TILE)
    
    # place a domino on the board
    def set_domino(self, t1, t2, p1, p2):
        self.set_tile(p1[0], p1[1], t1)
        self.set_tile(p2[0], p2[1], t2)
    
    def set_tile(self, x, y, t):
        self.board[x][y] = t
  
    #def can_place(self, x, y, t):
    #neighbors = [(1,1), (1,-1), (-1,1), (-1,-1)]
      #for nx, ny in neighbors:
    # self.board[x + nx][y + ny]
  
    # return list of next possible board states
    def enumerate_next_states(self, domino):
        pass
  
    # return integer score
    def score(self):
        pass
  
    # return if state is terminal or not
    def is_terminal(self):
        pass
  
    def copy(self):
        new_board = Board()
        new_board.board = [[val.copy() for val in self.board[col]] for col in self.board]
        return new_board

Dominos = [
    (Tile(0), Tile(0)),
    (Tile(0), Tile(0)),
    (Tile(4), Tile(4)),
    (Tile(4), Tile(4)),
    (Tile(4), Tile(4)),
    (Tile(4), Tile(4)),
    (Tile(2), Tile(2)),
    (Tile(2), Tile(2)),
    (Tile(2), Tile(2)),
    (Tile(1), Tile(1)),
    (Tile(1), Tile(1)),
    (Tile(3), Tile(3)),
    (Tile(0), Tile(4)),
    (Tile(0), Tile(2)),
    (Tile(0), Tile(1)),
    (Tile(0), Tile(3)),
    (Tile(4), Tile(2)),
    (Tile(4), Tile(1)),
    (Tile(0,1), Tile(4)),
    (Tile(0,1), Tile(2)),
    (Tile(0,1), Tile(1)),
    (Tile(0,1), Tile(3)),
    (Tile(0,1), Tile(5)),
    (Tile(4,1), Tile(0)),
    (Tile(4,1), Tile(0)),
    (Tile(4,1), Tile(0)),
    (Tile(4,1), Tile(0)),
    (Tile(4,1), Tile(2)),
    (Tile(4,1), Tile(1)),
    (Tile(2,1), Tile(0)),
    (Tile(2,1), Tile(0)),
    (Tile(2,1), Tile(4)),
    (Tile(2,1), Tile(4)),
    (Tile(2,1), Tile(4)),
    (Tile(2,1), Tile(4)),
    (Tile(0), Tile(1,1)),
    (Tile(1), Tile(3,1)),
    (Tile(5,1), Tile(0)),
    (Tile(0), Tile(3,2)),
    (Tile(2), Tile(1,1)),
    (Tile(0), Tile(3,1)),
    (Tile(0), Tile(1,2)),
    (Tile(2), Tile(1,2)),
    (Tile(1), Tile(3,2)),
    (Tile(5,2), Tile(0)),
    (Tile(3), Tile(5,2)),
    (Tile(3), Tile(5,2)),
    (Tile(0), Tile(5,3))
]
    