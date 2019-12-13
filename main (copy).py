import sys
import random
import csv
import datetime

# global variables
BOARD_SIZE = 18     # self-explanatory
MAX_LOOPS = 324     # maximum number of loops per test, generally around 270-280, added additional for buffer
TIME_MAX = 2        # maximum time per test, not used at the moment

class Board():
    # Creates the board by initializing a 2D array, 1 representing black, 0 representing white
    # Black is in the top left, not sure what orientation it'd be server side / for communication
    def __init__(self):
        self.state = init_board()
        for x in range(BOARD_SIZE):
            self.state.append([])
            for y in range(BOARD_SIZE):
                self.state[x].append((x+y+1)%2)
    
    def print(self):
        for x in self.state:
            for y in x:
                print(y, end = ' ')
            print()

    # calculate all possible moves
    # finds all possible moves
    def poss_moves(turn):
        looking = turn
        opponent = (turn + 1) % 2
        moves = []
        
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                if board[i][j] == looking:
                    # north
                    if i >= 2:  # bounds, only if i is leq 2, can you move north
                        if board[i-1][j] == opponent and board[i-2][j] == ' ':
                            moves.append(((i, j), (i-2, j)))
                    # south
                    if i < (BOARD_SIZE - 2):
                        if board[i+1][j] == opponent and board[i+2][j] == ' ':
                            moves.append(((i, j), (i+2, j)))
                    # west
                    if j >= 2:
                        if board[i][j-1] == opponent and board[i][j-2] == ' ':
                            moves.append(((i, j), (i, j-2)))
                    # east
                    if j < (BOARD_SIZE - 2):
                        if board[i][j+1] == opponent and board[i][j+2] == ' ':
                            moves.append(((i, j), (i, j+2)))
        # returns an array of tuples, first term is piece position, second term is moved location
        return moves

# Print short board, originally meant to be a more compact, aesthetics-wise of printing a board
# It gets the direction of the move and prints an arrow depending on the direction the piece moved
def print_sb(board, mp = [], d = ''):
    for i in range(0, len(board)):
        # print spaces
        print(' │', end = ' ')
        for j in range(0, len(board)):
            if (mp == [] or mp == ()):
                print(str(board[i][j]), end = ' ')
            else:
                if i == mp[0] and j == mp[1]:
                    if d == 'N':
                        print('↑', end = ' ')
                    elif d == 'S':
                        print('↓', end = ' ')
                    elif d == 'E':
                        print('→', end = ' ')
                    elif d == 'W':
                        print('←', end = ' ')
                else:
                    print(str(board[i][j]), end = ' ')
        print('│')

# Randomizes the black initial move, in the corners or in the middle
# RETURNS THE PIECE REMOVED
def rand_black_init(board):
    rand = random.randint(1, 4)
    size = len(board)

    choices = [(0, 0), (int(size / 2 - 1), int(size / 2) - 1), (int(size / 2), int(size / 2)), (size - 1, size - 1)]

    return choices[rand - 1]

# Randomizes the white initial move, adjacent to the initial black move
# RETURNS THE PIECE REMOVED
def rand_white_init(board, b_init):
    rand = 0
    size = len(board)

    choices = []

    # find the available moves for the piece, depending on where the piece is
    if b_init[0] == 0:                      # top left corner
        choices.append((0, 1))
        choices.append((1, 0))
        rand = random.randint(1, 2)
    elif b_init[0] == int(size / 2 - 1):    # middle left
        choices.append((int(size / 2 - 2), int(size / 2) - 1))
        choices.append((int(size / 2 - 1), int(size / 2) - 2))
        choices.append((int(size / 2), int(size / 2) - 1))
        choices.append((int(size / 2 - 1), int(size / 2)))
        rand = random.randint(1, 4)
    elif b_init[0] == int(size / 2):        # middle right
        choices.append((int(size / 2) + 1, int(size / 2)))
        choices.append((int(size / 2), int(size / 2) + 1))
        choices.append((int(size / 2) - 1, int(size / 2)))
        choices.append((int(size / 2), int(size / 2) - 1))
        rand = random.randint(1, 4)
    elif b_init[0] == (size - 1):           # lower right corner
        choices.append((size - 2, size - 1))
        choices.append((size - 1, size - 2))
        rand = random.randint(1, 2)

    # chooses the random choice
    return choices[rand - 1]

# remove a piece from the board
def remove(board, rp):
    board[int(rp[0])][int(rp[1])] = ' '
    return board, 'R'

# add a piece to the board, used to move piece
# may join with remove in separate function for full move command
def add(board, ap, t):
    piece = 0
    if t == 'B':
        piece = 1
    
    board[int(ap[0])][int(ap[1])] = piece
    return board, 'M'

# gets a list of possible moves and randomly chooses one
def random_walk(moves):
    size = len(moves)
    return moves[random.randint(0, size - 1)]

# what direction has the piece moved?
# can be used for signal sending to the server
def direction_calc(move):
    start = move[0]
    end = move[1]

    if start[0] > end[0]:
        return 'N'
    elif start[0] < end[0]:
        return 'S'
    elif start[1] > end[1]:
        return 'W'
    elif start[1] < end[1]:
        return 'E'

def move_piece(board, move, turn):
    r_action = ''

    # passed piece
    p_piece = [int((move[0][0] + move[1][0])/2), int((move[0][1] + move[1][1])/2)]

    # remove moving piece
    ret_val = remove(board, move[0])
    ret_board = ret_val[0]
    # remove passed over piece
    ret_val = remove(board, p_piece)
    ret_board = ret_val[0]
    # add final moving piece location
    ret_val = add(board, move[1], turn)
    ret_board = ret_val[0]
    r_action += ret_val[1]
    return board

# test for random walk
def rand_walk_test():
    # create board
    board = init_board(BOARD_SIZE)

    # run data stored in array
    # [0] is winner
    # [1] is where the first black piece was removed
    # [2] is total number of moves
    # [4] onwards are the number of available moves at that turn for the player
    run_data = ['', '', 0]

    num_loop = 0
    max_loop = MAX_LOOPS
    
    # keeps track of turn
    turn = ''

    # removed piece
    r_piece = ()
    r_action = ''

    # possible moves
    p_moves = []

    # passed piece
    p_piece = ()

    # moved direction
    dir = ''

    # black represented by 1
    # white represented by 0
    # black goes first

    while not num_loop > max_loop:
        # make possible moves empty again
        p_moves = []
        r_action = ''

        print('═' * (len(board) * 3))
        print('Loop', num_loop)
        # whose turn is it?
        if (num_loop % 2) == 1:
            turn = 'B'
        else:
            turn = 'W'

        # ignore if 0th initialization loop
        # if first loop, initialize black's first removed piece
        # if second loop, initialize white's first removed piece, adjacent to last removed piece
        # if not 0th, 1st, 2nd loop, then normal
        if num_loop == 0:
            pass
        elif num_loop == 1:
            r_piece = rand_black_init(board)
            ret_val = remove(board, r_piece)
            board = ret_val[0]
            r_action = ret_val[1]
            run_data[1] = r_piece
        elif num_loop == 2:
            r_piece = rand_white_init(board, r_piece)
            ret_val = remove(board, r_piece)
            board = ret_val[0]
            r_action = ret_val[1]
        elif num_loop not in [0, 1, 2]:
            p_moves = poss_moves(board, turn)
            
            # if there are not possible moves, game ends, last player wins
            if p_moves == []:
                print('═' * (len(board) * 3))
                print('L', num_loop, '| Turn', turn)
                print('─' * (len(board) * 3))
                print('No possible', turn, 'moves!')
                if turn == 'B':
                    print('White wins!')
                    run_data[0] = 'White'
                if turn == 'W':
                    print('Black wins!')
                    run_data[0] = 'Black'
                run_data[2] = num_loop - 2
                break
            else:
                run_data.append(len(p_moves))

            # randomly chosen move
            move = random_walk(p_moves)
            
            # calculate move direction
            dir = direction_calc(move)

            # move piece
            board = move_piece(board, move, turn)

        # after action decided, print board state and action made
        # loop and turn print
        print('═' * (len(board) * 3))
        if num_loop == 0:   # if initialization step
            print('Initial board')
        else:
            print('L', num_loop, '| Turn', turn)
        print('─' * (len(board) * 3))

        # if not initial loop, print board state and action
        if num_loop == 0:   # if initialization step
            print_sb(board)
        else:
            print_sb(board, p_piece, dir)
            print('─' * (len(board) * 3))

            # print removed piece
            if num_loop not in [0, 1, 2]:
                print('Possible moves:', p_moves)
                print('Move:', turn, move[0], '→', move[1])
                print('P:', p_piece)
            print('─' * (len(board) * 3))
            print(turn + ':', r_action, r_piece)

        num_loop += 1
    
    print('═' * (len(board) * 3))

    return run_data

# runs everything for looping/testing for data analysis purposes; random walk is very even
if __name__ == '__main__':
    # number of runs below
    runs = 5000

    # gets start time of loop
    start = datetime.datetime.now()
    with open('run_data.csv', mode = 'w') as run_data_file:
        with open('turn_data.csv', mode = 'w') as turn_data_file:
            run_writer = csv.writer(run_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            turn_writer = csv.writer(turn_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            first_row = ['win', 'fb_rem', 'tturn']

            for i in range(0, MAX_LOOPS+3):
                first_row.append('t_' + str(i))

            run_writer.writerow(first_row)

            first_row = ['turn', 'moves']

            turn_writer.writerow(first_row)

            for i in range(0, runs):
                run_data = rand_walk_test()
                print(run_data)
                run_writer.writerow(run_data)

                turn_data = run_data[3:]
                print(turn_data)
                for i in range(len(turn_data)):
                    turn_writer.writerow([i, turn_data[i]])
    
    # gets end time and calculates total time
    end = datetime.datetime.now()
    total_time = end - start

    # print total time needed to do all tests
    print('Testing time:', total_time)