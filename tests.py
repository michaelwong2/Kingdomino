from kingdomino import *

def format_board(matrix):
	b = Board()

	for x in range(3):
		for y in range(3):
			if matrix[y][x] < 7:
				b.board[x][y] = Tile(matrix[y][x])
	
	return b 

if __name__ == '__main__':
	m = [[6, 5, 0, 2, -1],
		 [0, 5, 7, 2, -1],
		 [3, 5, 7, -1, -1],
		 [2, -1, -1, -1, -1],
		 [1, 1, 1, 1, -1]]

	b = format_board(m)

	print(b)

	# print(b.is_complete())

	dad = b.enumerate_next_states((Tile(SWAMP), Tile(MOUNTAIN,2)))

	print(b)

	# for d in dad:
		# print(d.score(),'\n' + str(d))
