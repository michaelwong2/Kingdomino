from kingdomino import Board, Dominos
import sys

def domino_DFS(board, remaining, memo):
    if board.is_terminal():
        if len(memo) % 1000 == 0:
            print(board)
        return 1, 1 if board.is_filled() else 0, board.score(), board

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

    # unique_starts = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (2,2)]
    unique_starts = [(1,0), (0,0), (1,1)]

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
