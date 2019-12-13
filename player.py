import socket, sys
import main

class Player:
    def __init__(self, username, password, opponent):
        self.cur_board = main.Board()
        self.player = None #is player 0 or 1
        self.connected = 0
        self.game = None

        self.username = username
        self.password = password
        self.opponent = opponent
        
        self.port = 4705
        self.buf = 1024
        self.ip = socket.gethostbyname('artemis.engr.uconn.edu')
        self.socket = socket.socket()
        self.socket.connect((self.ip, self.port))
        print("Player connected to server")
        
    def print(self):
        print("Player: " + self.player)
        print("Playing game: " + self.game)
        print("Current Board:")
        for x in self.cur_board.state:
            for y in x:
                if y is None:
                    y = ' '
                print(y, end=' ')
            print()

    def move(self, strat=1):
        m = self.get_move(strat)
        self.socket.sendall(self.parse_move(m))

    def get_move(self, strat=1):
        move = None
        if strat == 0: #Random Walk
            move = Board.random_move(self.player)
        elif strat == 1: #MiniMax
            move = Board.minimax(self.player)
        return move
     
    def read_socket(self):
        data = self.socket.recv(self.buf)

        if (b'Artemis Konane Server' in data): #initial connection to server
            self.connected = 1
            print("Player connected") 
        elif (b'?Username' in data): #username authentication
            username = bytes(self.username, encoding = 'utf8') + b'\r\n'
            self.socket.sendall(username)
            print("Username sent")
        elif (b'?Password' in data): #password authentication
            password = bytes(self.password, encoding = 'utf8') + b'\r\n'
            self.socket.sendall(password)
            print("Password sent")
        elif (b'?Opponent' in data): #opponent authentication
            opponent = bytes(self.opponent, encoding = 'utf8') + b'\r\n'
            self.socket.sendall(opponent)
            print("Opponent sent")
        elif (b'Game' in data): #game authentication
            self.game = str(data)[7:-3]
            print("Got Game ID: " + self.game)
        elif (b'Color' in data): #color authentication
            color = str(data)[8:-3]
            print("Got Color: " + color)
            if "B" in color:
                self.player = 1
            elif "W" in color:
                self.player = 0
            else:
                print("ERROR")
            print("Player: " + str(self.player))
        elif (b'Player' in data) and (b'?Remove' in data) and (b'Removed' not in data): #initial move if coinflip win
            self.initial(0)
        elif (b'?Remove' in data): #initial move if coinflip loss
            self.initial(1)
        elif (b'?Move' in data): #make a move
            self.move()
        elif (b'Move[' in data):
            self.board.move(clean_move(data))
        elif (b'win' in data):
            print("The game has ended")
            print(data)
            print("")
        elif (b'Error' in data):
            print("There was an error")

        else:
            response = data.splitlines()
            for x in response:
                resp = str(x)
                resp = resp[2:len(resp)-1]
                print(resp)

    def clean_move(move):
        a = str(move)[6:-3]
        index = a.find(':')
        start = a[:index][1:-1]
        end = a[index + 1:][1:-1]
 
        index = start.find(',')
        start = (int(start[:index]), int(start[index + 1:]))
 
        index = end.find(',')
        end = (int(end[:index]), int(end[index + 1:]))
 
        return (start, end)

    def parse_move(move):
        return bytes('Move['+str(move[0][0])+','+str(move[0][1])+']:['+str(move[1][0])+','+str(move[1][1])+']\n', 'utf8')

    def play(self):
        while True:
            self.read_socket()
    
    def initial(self, choice):
        board = self.board.state
        if choice == 0:
            x = randint(0, 3)
            if x == 0:
                self.remove((0, 0))
            elif x == 1:
                self.remove((0, 17))
            elif x == 2:
                self.remove((17, 0))
            elif x == 3:
                self.remove((17, 17))
        elif choice == 1:
            if board[0][0] == ' ':
                self.remove((1, 0))
            elif board[0][17] == ' ':
                self.remove((1, 17))
            elif board[17][0] == ' ':
                self.remove((16, 0))
            elif board[17][17] == ' ':
                self.remove((16, 17))
            elif board[8][8] == ' ':
                self.remove((9, 8))
            elif board[8][9] == ' ':
                self.remove((9, 9))
            elif board[9][8] == ' ':
                self.remove((8, 8))
            elif board[9][9] == ' ':
                self.remove((8, 9))
        
    def remove(self, move):
        self.Board.remove(move)

buf = 1024
args = sys.argv
p = Player(args[1], args[2], args[3])
p.play()	
