from kingdomino import Board, Dominos

def domino_DFS(board, remaining):
    if board.is_terminal:
        return 1, 1 if board.is_filled() else 0, board.score()

    count = 0
    fcount = 0
    max_score = -1

    for i in range(len(remaining)):
        next_boards = board.enumerate_next_states(Dominos[remaining[i]])

        new_remaining = remaining[:]
        del new_remaining[i]

        for next_board in next_boards:
            c, fc, ms = domino_DFS(next_board, new_remaining)

            count += c
            fcount += fc
            max_score = max(max_score, ms)

    return count, fcount, max_score

if __name__ == '__main__':
    
    end_states = 0
    filled_end_states = 0
    max_score = -1

    unique_starts = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (2,2)]
    for x, y in unique_starts:

        b = Board(x, y)

        e,f,m = domino_DFS(b, [1]*len(Dominos))

        end_states += e
        filled_end_states += f 
        max_score = max(max_score, m)

    print("Simulation over.")
    print("Total end states: {}".format(end_states))
    print("End states that were complete tilings:{ }/{}".format(filled_end_states, end_states))
    print("Maximum possible score: {}".format(max_score))
