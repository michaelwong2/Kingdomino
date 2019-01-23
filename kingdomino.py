from collections import deque

BOARD_SIZE = 3

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
        # each candidate is an empty space. Check that the neighborhood is clear, and for 
        # each empty neighbor, we can add a domino with the correct side facing 
        # (in the case of the kingdom its both sides) 
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
        score = 0
        visited = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] is not None and self.board[x][y].crowns > 0 and not visited[x][y]:
                    crowns, count = self._count_crowns(x,y, self.board[x][y].type, visited)
                    score += count * crowns

        return score

    def _count_crowns(self, x, y, t, v):
        crowns = self.board[x][y].crowns
        count = 1

        v[x][y] = True

        for dx, dy in NEIGHBORHOOD:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and self.board[nx][ny] is not None and self.board[nx][ny].type == t and not v[nx][ny]:
                cw, co = self._count_crowns(nx, ny, t, v)
                crowns += cw
                count += co 

        return crowns, count

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

    def is_complete(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] is None:
                    return False
        return True

    def copy(self):
        new_board = Board(self.starting[0], self.starting[1])
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

    def get_hash(self):
        s = ''
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                v = self.board[x][y]
                if v is None:
                    v = '.'
                s += str(v)

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

def domino_DFS(board, remaining, memo):
    if board.is_terminal():
        if len(memo) % 10000 == 0:
            print('States visited:',len(memo))
            print(board)
        return 1, 1 if board.is_complete() else 0, board.score(), board

    count = 0
    fcount = 0
    max_score = -1
    max_board = None

    for i in range(len(remaining)):
        next_boards = board.enumerate_next_states(Dominos[remaining[i]])

        new_remaining = remaining[:]
        del new_remaining[i]

        for next_board in next_boards:

            h = next_board.get_hash()
            if h in memo:
                continue

            c, fc, ms, mb = domino_DFS(next_board, new_remaining, memo)

            memo.add(h)

            count += c
            fcount += fc
            if ms > max_score:
                max_score = ms
                max_board = mb

    return count, fcount, max_score, max_board

if __name__ == '__main__':
    
    end_states = 0
    filled_end_states = 0
    max_score = -1
    max_board = None

    unique_starts = [(0,0), (1,0), (1,1)]

    for i in range(len(unique_starts)):
        x, y = unique_starts[i]

        print('Completed {} branches'.format(i))

        memo = set()

        b = Board(x, y)

        e,f,m,mb = domino_DFS(b, [k for k in range(len(Dominos))], memo)

        end_states += e
        filled_end_states += f 
        if m > max_score:
            max_score = m
            max_board = mb

    print('\n\n' + '*'*40)
    print("Simulation over.")
    print("Total end states: {}".format(end_states))
    print("End states that were complete tilings: {} / {}".format(filled_end_states, end_states))
    print("Maximum possible score: {}, shown below:".format(max_score))
    print(max_board)

    