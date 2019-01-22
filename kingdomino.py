from collections import deque

BOARD_SIZE = 5

WHEAT = 0
PLAIN = 1
LAKE = 2
SWAMP = 3
FOREST = 4
MOUNTAIN = 5
KINGDOM = 6

NEIGHBORHOOD = [(1,0), (-1,0), (0,1), (0,-1)]

class Tile:
    def __init__(self, t, crowns=0):
        assert t <= 6
        self.type = t # 0-6, 0-5 are landscapes, 6 is starting tile
        self.crowns = crowns
        
    def copy(self):
        return Tile(self.type, self.crowns)

    def __str__(self):
        return str(self.type)
  
class Board:
    def __init__(self, sx=0, sy=0):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board[sx][sy] = Tile(KINGDOM)
        self.starting = (sx, sy)
    
    # place a domino on the board
    def set_domino(self, t1, t2, p1, p2):
        self.set_tile(p1[0], p1[1], t1)
        self.set_tile(p2[0], p2[1], t2)
    
    def set_tile(self, x, y, t):
        self.board[x][y] = t
  
    # return list of next possible board states
    def enumerate_next_states(self, domino):

        dtypes = [domino[0].type, domino[1].type]

        # find candidates
        q = deque([self.starting])
        visited = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        considered = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        candidates = deque()
        
        # for each neighbor, if it has not been visited and is a tile, enqueue it
        # if it is a empty, add it to the candidates if the curr tile is compatible 
        # with either side of the domino
        while len(q) > 0:
            x,y = q.popleft()
            t = self.board[x][y]

            visited[x][y] = True

            for dx, dy in NEIGHBORHOOD:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and not visited[nx][ny] and not considered[nx][ny]:
                    if self.board[nx][ny] is not None:
                        q.append((nx, ny))
                    elif t.type == KINGDOM or t.type in dtypes:
                        candidates.append((nx,ny, t.type))
                        considered[nx][ny] = True

        # evaluate candidates
        # each candidate is an empty space. Check that the moore neighborhood is clear, and for 
        # each empty neighbor, we can add a domino with the side facing 

        next_states = deque()

        for x,y,adj_type in candidates:
            for dx,dy in NEIGHBORHOOD:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.board[nx][ny] is None:

                    head, tail = domino

                    if adj_type == KINGDOM:
                        nb1 = self.copy()
                        nb2 = self.copy()

                        nb1.set_tile(x,y,head)
                        nb1.set_tile(nx,ny,tail)

                        nb2.set_tile(x,y,tail)
                        nb2.set_tile(nx,ny,head)

                        next_states.append(nb1)
                        next_states.append(nb2)

                    else:
                        new_board = self.copy()

                        if domino[0].type != adj_type:
                            tail, head = domino

                        new_board.set_tile(x,y,head)
                        new_board.set_tile(nx,ny,tail)

                        next_states.append(new_board)

        return next_states
  
    def score(self):
        pass

    def in_bounds(self, x, y):
        return x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE
  
    # return if state is terminal or not
    def is_terminal(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] is None:
                    for dx, dy in NEIGHBORHOOD:
                        if self.in_bounds(x + dx, y + dy) and self.board[x + dx][y + dy] is None:
                            return False

        return True

    def copy(self):
        new_board = Board()
        new_board.board = [[val.copy() if val is not None else None for val in col] for col in self.board]
        return new_board

    def __str__(self):
        s = ''
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                v = self.board[x][y]
                if v is None:
                    v = '_'

                s += ' | ' + str(v)
            s += ' |\n'

        return s

global Dominos
Dominos = [
    (Tile(WHEAT), Tile(WHEAT)),
    (Tile(WHEAT), Tile(WHEAT)),
    (Tile(FOREST), Tile(FOREST)),
    (Tile(FOREST), Tile(FOREST)),
    (Tile(FOREST), Tile(FOREST)),
    (Tile(FOREST), Tile(FOREST)),
    (Tile(LAKE), Tile(LAKE)),
    (Tile(LAKE), Tile(LAKE)),
    (Tile(LAKE), Tile(LAKE)),
    (Tile(PLAIN), Tile(PLAIN)),
    (Tile(PLAIN), Tile(PLAIN)),
    (Tile(SWAMP), Tile(SWAMP)),
    (Tile(WHEAT), Tile(FOREST)),
    (Tile(WHEAT), Tile(LAKE)),
    (Tile(WHEAT), Tile(PLAIN)),
    (Tile(WHEAT), Tile(SWAMP)),
    (Tile(FOREST), Tile(LAKE)),
    (Tile(FOREST), Tile(PLAIN)),
    (Tile(WHEAT,1), Tile(FOREST)),
    (Tile(WHEAT,1), Tile(LAKE)),
    (Tile(WHEAT,1), Tile(PLAIN)),
    (Tile(WHEAT,1), Tile(SWAMP)),
    (Tile(WHEAT,1), Tile(MOUNTAIN)),
    (Tile(FOREST,1), Tile(WHEAT)),
    (Tile(FOREST,1), Tile(WHEAT)),
    (Tile(FOREST,1), Tile(WHEAT)),
    (Tile(FOREST,1), Tile(WHEAT)),
    (Tile(FOREST,1), Tile(LAKE)),
    (Tile(FOREST,1), Tile(PLAIN)),
    (Tile(LAKE,1), Tile(WHEAT)),
    (Tile(LAKE,1), Tile(WHEAT)),
    (Tile(LAKE,1), Tile(FOREST)),
    (Tile(LAKE,1), Tile(FOREST)),
    (Tile(LAKE,1), Tile(FOREST)),
    (Tile(LAKE,1), Tile(FOREST)),
    (Tile(WHEAT), Tile(PLAIN,1)),
    (Tile(PLAIN), Tile(SWAMP,1)),
    (Tile(MOUNTAIN,1), Tile(WHEAT)),
    (Tile(WHEAT), Tile(SWAMP,2)),
    (Tile(LAKE), Tile(PLAIN,1)),
    (Tile(WHEAT), Tile(SWAMP,1)),
    (Tile(WHEAT), Tile(PLAIN,2)),
    (Tile(LAKE), Tile(PLAIN,2)),
    (Tile(PLAIN), Tile(SWAMP,2)),
    (Tile(MOUNTAIN,2), Tile(WHEAT)),
    (Tile(SWAMP), Tile(MOUNTAIN,2)),
    (Tile(SWAMP), Tile(MOUNTAIN,2)),
    (Tile(WHEAT), Tile(MOUNTAIN,3))
]
    