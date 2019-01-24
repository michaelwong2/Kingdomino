import argparse
from collections import deque

global BOARD_SIZE
BOARD_SIZE = 4

NEIGHBORHOOD = [(1,0), (-1,0), (0,1), (0,-1)]

class DBoard:
    def __init__(self, sx=0, sy=0):
        self.board = [[-1] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        if BOARD_SIZE % 2 != 0:
            self.board[sx][sy] = 0
        self.starting = (sx, sy)

    def set(self, c1, c2):
        v = 1 if c1[1] == c2[1] else 2

        self.board[c1[0]][c1[1]] = v
        self.board[c2[0]][c2[1]] = v

    def enumerate_next_states(self):
        q = deque([self.starting])
        visited = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        candidates = deque()

        while len(q) > 0:
            x,y = q.popleft()

            visited[x][y] = True

            for dx, dy in NEIGHBORHOOD:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and not visited[nx][ny]:
                    if self.board[nx][ny] != -1:
                        q.append((nx, ny))
                    else:
                        candidates.append((nx,ny))

        seen = set()
        next_states = deque()

        for x,y in candidates:
            for dx,dy in NEIGHBORHOOD:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.board[nx][ny] == -1:
                    new_board = self.copy()
                    new_board.set((x,y), (nx, ny))
                    
                    h = new_board.get_hash()
                    if h not in seen:
                        seen.add(h)
                        next_states.append(new_board)

        return next_states

    def in_bounds(self, x, y):
        return x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE
  
    # return if state is terminal or not
    def is_terminal(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] == -1:
                    for dx, dy in NEIGHBORHOOD:
                        if self.in_bounds(x + dx, y + dy) and self.board[x + dx][y + dy] == -1:
                            return False

        return True

    def is_complete(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] == -1:
                    return False
        return True

    def copy(self):
        new_board = DBoard(self.starting[0], self.starting[1])
        new_board.board = [[val for val in col] for col in self.board]
        return new_board

    def __str__(self):
        s = ''
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                v = self.board[x][y]
                if v == -1:
                    v = '_'

                s += ' | ' + str(v)
            s += ' |\n'

        return s

    def get_hash(self):
        s = ''
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                v = self.board[x][y]
                if v == -1:
                    v = '.'
                s += str(v)

        return s

def domino_DFS(board, memo):
    if board.is_terminal():
        if len(memo) % 10000 == 0:
            print('States visited:',len(memo))
            print(board)
        return 1, 1 if board.is_complete() else 0

    count = 0
    fcount = 0

    for next_board in board.enumerate_next_states():
        h = next_board.get_hash()
        if h in memo:
            continue

        c, fc = domino_DFS(next_board, memo)

        memo.add(h)

        count += c
        fcount += fc

    return count, fcount

def simulate_tilings(bsize):
    global BOARD_SIZE
    BOARD_SIZE = bsize

    end_states = 0
    filled_end_states = 0

    unique_starts = [(0,0)]

    if BOARD_SIZE % 2 != 0:
        unique_starts = [(x,y) for y in range(BOARD_SIZE//2) for x in range(BOARD_SIZE // 2 + 1)]
        unique_starts.append((BOARD_SIZE//2, BOARD_SIZE//2))
        print(unique_starts)

    for i in range(len(unique_starts)):
        x, y = unique_starts[i]

        print('Completed {} branches'.format(i))

        memo = set()

        b = DBoard(x, y)

        e,f = domino_DFS(b, memo)

        end_states += e
        filled_end_states += f 

    print('\n\n' + '*'*40)
    print("Simulation over.")
    print("Total end states: {}".format(end_states))
    print("End states that were complete tilings: {} / {}".format(filled_end_states, end_states))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', '--N_size', help='board dimensiosn', type=int, default=3)
    args = parser.parse_args()

    simulate_tilings(args.N_size)
  

