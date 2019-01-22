from kingdomino import *

def format_board(matrix):
	b = Board()

	for x in range(5):
		for y in range(5):
			if matrix[y][x] < 7:
				b.set_tile(x, y, Tile(matrix[y][x]))
	
	return b 


if __name__ == '__main__':
	m = [[6, 7, 3, 2, 7],
		 [1, 1, 7, 1, 3],
		 [1, 1, 3, 3, 3],
		 [1, 2, 2, 2, 7],
		 [1, 1, 2, 2, 7]]

	b = format_board(m)

	print(b)

	print(b.is_terminal())

	# dad = b.enumerate_next_states((Tile(1),Tile(2)))

	# for d in dad:
	# 	print(d)