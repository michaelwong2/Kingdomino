from kingdomino import *

def format_board(matrix):
	b = Board()

	for x in range(5):
		for y in range(5):
			if matrix[y][x] < 7:
				b.set_tile(x, y, Tile(matrix[y][x]))
	
	return b 


if __name__ == '__main__':
	m = [[6, 7, 7, 7, 7],
		 [1, 7, 7, 7, 7],
		 [1, 7, 7, 7, 7],
		 [2, 7, 7, 7, 7],
		 [2, 7, 7, 7, 7]]

	b = format_board(m)

	print(b)

	dad = b.enumerate_next_states((Tile(1),Tile(2)))

	for d in dad:
		print(d)