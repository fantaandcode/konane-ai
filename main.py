import sys
import random
import csv
import datetime
import copy

# global variables
BOARD_SIZE = 18     # self-explanatory
MAX_LOOPS = 324     # maximum number of loops per test, generally around 270-280, added additional for buffer
TIME_MAX = 2        # maximum time per test, not used at the moment

class Board():
    # Creates the self.state by initializing a 2D array, 1 representing black, 0 representing white
    # Black is in the top left, not sure what orientation it'd be server side / for communication
    children = []
    parent = None
    state = []

    def __init__(self):
        for x in range(BOARD_SIZE):
            self.state.append([])
            for y in range(BOARD_SIZE):
                self.state[x].append((x+y+1)%2)
    
    # weight function
    def weight(self, turn):
        return len(self.poss_moves(turn)) - len(self.poss_moves((turn + 1) % 2))

    def print(self):
        for x in self.state:
            for y in x:
                print(y, end = ' ')
            print()

    # calculate all possible moves
    # finds all possible moves
    def poss_moves(self, turn):
        looking = turn
        opponent = (turn + 1) % 2
        moves = []
        
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                if self.state[i][j] == looking:
                    # north
                    if i >= 2:  # bounds, only if i is leq 2, can you move north
                        if self.state[i-1][j] == opponent and self.state[i-2][j] == ' ':
                            moves.append(((i, j), (i-2, j)))
                    # south
                    if i < (BOARD_SIZE - 2):
                        if self.state[i+1][j] == opponent and self.state[i+2][j] == ' ':
                            moves.append(((i, j), (i+2, j)))
                    # west
                    if j >= 2:
                        if self.state[i][j-1] == opponent and self.state[i][j-2] == ' ':
                            moves.append(((i, j), (i, j-2)))
                    # east
                    if j < (BOARD_SIZE - 2):
                        if self.state[i][j+1] == opponent and self.state[i][j+2] == ' ':
                            moves.append(((i, j), (i, j+2)))
        # returns an array of tuples, first term is piece position, second term is moved location
        return moves
    
    # returns a copy of the board
    def copy_state(self):
        x = Board()
        x.state = copy.deepcopy(self.state)
        return x

    # possible board states
    def poss_boards(self, turn):
        moves = self.poss_moves(turn)
        boards = []
        for m in moves:
            board_copy = self.copy_state()
            boards.append(board_copy.move_piece(m))
        
        return boards
    
    # remove a piece from the board
    # rp: remove piece, tuple of position
    def remove(self, rp):
        self.state[int(rp[0])][int(rp[1])] = ' '

    # add a piece to the board, used to move piece
    # may join with remove in separate function for full move command
    def add(self, ap):        
        self.state[int(ap[0])][int(ap[1])] = (ap[0] + ap[1] + 1) % 2
    
    # move a piece, takes in tuple of tuples of positions
    def move_piece(self, move):
        # passed piece
        p_piece = (int((move[0][0] + move[1][0])/2), int((move[0][1] + move[1][1])/2))

        # remove moving piece
        self.remove(move[0])
        # remove passed over piece
        self.remove(p_piece)
        # add final moving piece location
        self.add(move[1])
    

# Print short self.state, originally meant to be a more compact, aesthetics-wise of printing a self.state
# It gets the direction of the move and prints an arrow depending on the direction the piece moved
def print_sb(board, mp = [], d = ''):
    for i in range(0, len(board.state)):
        # print spaces
        print(' │', end = ' ')
        for j in range(0, len(board.state)):
            if (mp == [] or mp == ()):
                print(str(board.state[i][j]), end = ' ')
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
                    print(str(board.state[i][j]), end = ' ')
        print('│')

# Randomizes the black initial move, in the corners or in the middle
# RETURNS THE PIECE REMOVED
def rand_black_init():
    rand = random.randint(1, 4)
    size = BOARD_SIZE

    choices = [(0, 0), (int(size / 2 - 1), int(size / 2) - 1), (int(size / 2), int(size / 2)), (size - 1, size - 1)]

    return choices[rand - 1]

# Randomizes the white initial move, adjacent to the initial black move
# RETURNS THE PIECE REMOVED
def rand_white_init(b_init):
    rand = 0
    size = BOARD_SIZE

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

def test(runs):
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
                run_data = []
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

def board_test():
    b = Board()
    b.print()
    black_first = rand_black_init()
    white_first = rand_white_init(black_first)
    b.remove(black_first)
    b.remove(white_first)
    b.add(black_first)
    b.add(white_first)
    print()
    b.print()

# runs everything for looping/testing for data analysis purposes; random walk is very even
if __name__ == '__main__':
    # number of runs below
    # runs = 5

    # test(runs)
    board_test()