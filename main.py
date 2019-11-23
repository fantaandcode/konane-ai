import sys
import random

def init_board(size):
    board = []

    for i in range(0, size):
        temp = []
        for j in range(0, size):
            temp.append((i + j + 1) % 2)
        board.append(temp)
    
    return board

def print_b(board):
    for i in range(0, len(board)):
        # print in between spacers
        if i != 0 and i != len(board) + 1:
            print('├' + ('───┼' * (len(board) - 1)) + '───┤')
        elif i == 0:
            print('┌' + ('───┬' * (len(board) - 1)) + '───┐')
        
        # print spaces
        for j in range(0, len(board)):
            print('│' + ' ' + str(board[i][j]) + ' ', end = '')
            if j == len(board) - 1:
                print('│')
        
        if i == (len(board) - 1):
            print('└' + ('───┴' * (len(board) - 1)) + '───┘')

def print_sb(board):
    for i in range(0, len(board)):
        # print spaces
        for j in range(0, len(board)):
            print(str(board[i][j]), end = ' ')
        print()

def rand_black_init(board):
    rand = random.randint(1, 4)
    size = len(board)

    choices = [(0, 0), (int(size / 2 - 1), int(size / 2) - 1), (int(size / 2), int(size / 2)), (size - 1, size - 1)]

    return choices[rand - 1]

def rand_white_init(board, b_init):
    rand = 0
    size = len(board)

    choices = []

    if b_init[0] == 0:
        choices.append((0, 1))
        choices.append((1, 0))
        rand = random.randint(1, 2)
    elif b_init[0] == int(size / 2 - 1):
        choices.append((int(size / 2 - 2), int(size / 2) - 1))
        choices.append((int(size / 2 - 1), int(size / 2) - 2))
        choices.append((int(size / 2), int(size / 2) - 1))
        choices.append((int(size / 2 - 1), int(size / 2)))
        rand = random.randint(1, 4)
    elif b_init[0] == int(size / 2):
        choices.append((int(size / 2) + 1, int(size / 2)))
        choices.append((int(size / 2), int(size / 2) + 1))
        choices.append((int(size / 2) - 1, int(size / 2)))
        choices.append((int(size / 2), int(size / 2) - 1))
        rand = random.randint(1, 4)
    elif b_init[0] == (size - 1):
        choices.append((size - 2, size - 1))
        choices.append((size - 1, size - 2))
        rand = random.randint(1, 2)

    return choices[rand - 1]

def remove(board, rp):
    board[int(rp[0])][int(rp[1])] = ' '
    return board, 'R'

def add(board, ap, t):
    piece = 0
    if t == 'B':
        piece = 1
    
    board[int(ap[0])][int(ap[1])] = piece
    return board, 'M'

def poss_moves(board, turn):
    looking = 0
    moves = []

    if turn == 'B':
        looking == 1
    
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if board[i][j] == looking:
                # north
                if i >= 2:
                    if board[i-1][j] != looking and board[i-2][j] == ' ':
                        moves.append(((i, j), (i-2, j)))
                # south
                if i < (len(board) - 2):
                    if board[i+1][j] != looking and board[i+2][j] == ' ':
                        moves.append(((i, j), (i+2, j)))

    # returns an array of tuples, first term is piece position, second term is moved location
    return moves

def random_walk(moves):
    size = len(moves)
    return moves[random.randint(0, size - 1)]
        
if __name__ == '__main__':
    board = init_board(8)

    num_loop = 0
    max_loop = 3
    
    # keeps track of turn
    turn = ''

    # removed piece
    r_piece = ()
    r_action = ''

    # possible moves
    p_moves = []

    # black represented by 1
    # white represented by 0
    # black goes first

    while not num_loop > max_loop:
        print('Loop', num_loop)
        # whose turn is it?
        if (num_loop % 2) == 1:
            turn = 'B'
        else:
            turn = 'W'

        # if first loop, initialize black's first removed piece
        # if second loop, initialize white's first removed piece, adjacent to last removed piece
        if num_loop == 0:
            pass
        if num_loop == 1:
            r_piece = rand_black_init(board)
            ret_val = remove(board, r_piece)
            board = ret_val[0]
            r_action = ret_val[1]
        elif num_loop == 2:
            r_piece = rand_white_init(board, r_piece)
            ret_val = remove(board, r_piece)
            board = ret_val[0]
            r_action = ret_val[1]
        elif num_loop not in [0, 1, 2]:
            p_moves = poss_moves(board, turn)
            move = random_walk(p_moves)
            
            # passed piece
            p_piece = (int((move[0][0] + move[1][0])/2), int((move[0][1] + move[1][1])/2))
            ret_val = remove(board, p_piece)
            board = ret_val[0]
            r_action = ret_val[1]
            ret_val = add(board, move[1], turn)
            board = ret_val[0]
            r_action += ret_val[1]

        # after action decided, print board state and action made
        # loop and turn print
        print('═' * (len(board) * 2))
        if num_loop == 0:
            print('Initial board')
        else:
            print('L', num_loop, '| Turn', turn)
        print('─' * (len(board) * 2))

        # if not initial loop, print board state and action
        if num_loop == 0:
            print_sb(board)
        else:
            print_sb(board)

            # print removed piece
            print('─' * (len(board) * 2))
            if num_loop not in [0, 1, 2]:
                print('Possible moves:', p_moves)
            print(turn + ':', r_action, r_piece)

        num_loop += 1
    
    print('═' * (len(board) * 2))