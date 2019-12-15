import random
import copy
import math

BOARD_SIZE = 18

class Board:

	def __init__(self):
		self.board=[]
		for x in range(18):
			self.board.append([])
			for y in range(18):
				self.board[x].append((x+y+1)%2)
		self.move = None
		self.weight = 0

    # plays the game
	def play_game(self, depth, flag=False, iterations=4):
		alpha = float('-inf')
		beta  = float('inf')
		
		color = self.initial_moves()
		#self.print_board()

		if flag:
			for i in range(iterations):
				if color:
					new_move = self.minimax(self, depth+2, alpha, beta, True, 1)
					self = new_move
					color = self.change_color(color)
				else:
					new_move = self.minimax(self, depth+2, alpha, beta, True, 0)
					self = new_move
					color = self.change_color(color)

				self.print_board()
				print('\n')
		
		turns = 0
		random_turn = random.randint(5, 10)

		while not self.game_over(color):
			self.print_board()
			if turns == random_turn:
				new_move = self.random_move(color)
				self.make_move(new_move.move)
				color = self.change_color(color)
				turns = 0
				random_turn = random.randint(5, 10)
			else:
				if color:
					new_move = self.minimax(self, depth, alpha, beta, True, 1)
					self.make_move(new_move.move)
					color = self.change_color(color)
				else:
					new_move = self.minimax(self, depth, alpha, beta, True, 0)
					self.make_move(new_move.move)
					color = self.change_color(color)
			turns += 1
			
			print('\n')
		self.print_board()
		self.winner((color+1)%2)

    # minimax function
	def minimax(self, board, depth, alpha, beta, maxPlayer, color):

		if depth == 0 or self.game_over(color):
			return board

		if maxPlayer:
			# initially set to negative infinity
			maxEval = board
			maxEval.weight = float('-inf')
			for child in board.get_boards(color):
				move = self.minimax(child, depth-1, alpha, beta, False, self.change_color(color))
				move.weight = move.heuristic(color)
				maxEval = self.max_board(maxEval, move, color)
				alpha = max(alpha, move.weight)
				if beta <= alpha:
					break
			return maxEval

		else:
			# initially set to positive infinity
			minEval = board
			minEval.weight = float('inf')
			for child in board.get_boards(color):
				move = self.minimax(child, depth-1, alpha, beta, True, self.change_color(color))
				move.weight = move.heuristic(color)
				minEval = self.min_board(minEval, move, color)
				beta = min(beta, move.weight)
				if beta <= alpha:
					break
			return minEval

    # randomly select a move, this is implemented in the random case of using a random move to throw off opponent's algorithms
	def random_move(self, color):
		moves = self.get_boards(color)
		random_index = random.randint(0, len(moves)-1)
		return moves[random_index]
    
    # get all possible board states from the current board state
	def get_boards(self, turn):
        # gets all possible moves from current board state
		moves = self.get_moves(turn)
		boards = []
        # iterate over all possible moves to get possible board states, all of which are deepcopy'd
		for m in moves:
			board_copy = self.new_board()
			board_copy.make_move(m)
			boards.append(board_copy)
			board_copy.move = m
		return boards

    # get all possible moves from current board state
	def get_moves(self, turn):
		opponent = (turn + 1) % 2
		moves = []

        # iterate through all board cells to see if there can be moves
		for i in range(0, BOARD_SIZE):
			for j in range(0, BOARD_SIZE):
				if self.board[i][j] == turn:
					# north, bounded so that you can't move into -1 or -2
					if i >= 2:
						if self.board[i-1][j] == opponent and self.board[i-2][j] == ' ':
							moves.append(((i, j), (i-2, j)))
					# south, bounded so that you can't move into BOARD_SIZE or BOARD_SIZE+1, out of index
					if i < (BOARD_SIZE - 2):
						if self.board[i+1][j] == opponent and self.board[i+2][j] == ' ':
							moves.append(((i, j), (i+2, j)))
					# west
					if j >= 2:
						if self.board[i][j-1] == opponent and self.board[i][j-2] == ' ':
							moves.append(((i, j), (i, j-2)))
					# east
					if j < (BOARD_SIZE - 2):
						if self.board[i][j+1] == opponent and self.board[i][j+2] == ' ':
							moves.append(((i, j), (i, j+2)))
		# returns an array of tuples, first term is piece position, second term is moved location, ((x1, y1). (x2, y2))
		return moves

    # gets all possible first moves and randomly picks
	def initial_moves(self):
		# All possible initial moves
		first_black_moves = [(0, 0), (17, 17), (8, 8), (9, 9)]
		first_white_moves = [(0, 17), (17, 0), (8, 9), (9, 8)] 
		all_first_moves   = [(0, 0), (0, 17), (17, 0), (17, 17), 
						     (8, 8), (8, 9),   (9, 8), (9, 9)]

		# Selection of the first move
		first_move = all_first_moves[random.randint(0, len(all_first_moves)-1)]
		x, y = first_move[0], first_move[1]

		# Color is determined -> Either 0=white or 1=black
		first_color = self.board[x][y]

		# First move is made
		self.remove_piece(first_move)

		if first_color:
			second_move = first_white_moves[random.randint(0, len(first_white_moves)-1)]
			x, y = second_move[0], second_move[1]
			self.remove_piece(second_move)
		else:
			second_move = first_black_moves[random.randint(0, len(first_black_moves)-1)]
			x, y = second_move[0], second_move[1]
			self.remove_piece(second_move)
		

		return first_color

    # makes a move given a move
	def make_move(self, move):
		removed_piece, added_piece = move[0], move[1]
		jumped_piece = (int((move[0][0] + move[1][0])/2), int((move[0][1] + move[1][1])/2))

		self.remove_piece(removed_piece)
		self.remove_piece(jumped_piece)
		self.add_piece(added_piece)

    # weights assigned to each board, difference of possible moves of self and opponent
	def heuristic(self, color):
		return len(self.get_moves(color)) - len(self.get_moves((color + 1) % 2))

    # get max board weight
	def max_board(self, board1, board2, color):
		if board1.weight > board2.weight:
			return board1
		else:
			return board2

    # get minimum board weight
	def min_board(self, board1, board2, color):
		if board1.weight > board2.weight:
			return board2
		else:
			return board1

    # add a piece to the board, given the position
	def add_piece(self, ap):
		self.board[int(ap[0])][int(ap[1])] = (ap[0] + ap[1] + 1) % 2

    # removes a piece on the board, given the position
	def remove_piece(self, rp):
		self.board[int(rp[0])][int(rp[1])] = ' '

    # creates a new board and deep copies
	def new_board(self):
		new_board = Board()
		new_board.board = copy.deepcopy(self.board)
		return new_board

    # returns opposite color
	def change_color(self, color):
		return 0 if color else 1

    # check if game ends
	def game_over(self, color):
		return True if len(self.get_moves(color))==0 else False

    # simulates coin toss
	def coin_toss(self):
		return random.randint(0, 1)

    # resets board
	def reset_board(self):
		self.board = [[1, 0]*9, [0, 1]*9]*9

    # who wins? prints
	def winner(self, color):
		if color:
			print('Winner: Black')
		else:
			print('Winner: White')

    # print board
	def print_board(self):
		for x in self.board:
			for y in x:
				print(y, end = ' ')
			print()
		print('\n')

