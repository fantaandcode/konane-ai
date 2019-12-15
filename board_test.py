# TEST FILE FOR BOARD

from board_class import Board 

alpha = float('-inf')
beta = float('inf')

# print works
board = Board()
#board.print_board()
#print('\n')

# new board works
new_board = board.new_board()

# Inital Move Test
# Takes two optional parameters flag and iterations
# if flag == True Will run k iterations with depth+2 depth
# iterations = number of times to run the extended depth 

board.play_game(3)

# minimax testing
#move = board.minimax(board, 5, alpha, beta, True, color)
#print(move.move)