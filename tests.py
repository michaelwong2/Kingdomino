from domino import *

def format_board(matrix):
	b = DBoard()

	for x in range(3):
		for y in range(3):
			if matrix[y][x] < 7:
				b.board[x][y] = matrix[y][x]
	
	return b 

if __name__ == '__main__':
	m = [[2, -1, -1, 2, -1],
		 [2, 1, 1, 2, -1],
		 [2, -1, -1, -1, -1],
		 [2, -1, -1, -1, -1],
		 [1, 1, 1, 1, -1]]

	b = format_board(m)

	print(b)

	# print(b.is_complete())

	# dad = b.enumerate_next_states()

	# for d in dad:
		# print(d)
