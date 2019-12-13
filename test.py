import socket, sys
import main
class Player:
    def __init__(self, username, password, opponent):
        self.cur_board = main.Board()
        self.player = None #is player 0 or 1
        self.connected = 0        
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
        print("Current Board:")
        for x in self.cur_board.state:
            for y in x:
                if y is None:
                    y = ' '
                print(y, end=' ')
            print()
    
    def move(self, strat=1):
        m = self.get_move(strat)
        #TODO change format of 'm' to match server
        self.socket.sendall(m)
    
    def get_move(self, strat=1):
        #TODO
        move = None
        if strat == 0: #Random Walk
            move = Board.random_move()
        elif strat == 1: #MiniMax
            move = Board.minimax()
        return move
    
    def read_socket(self):
        data = self.socket.recv(self.buf)

        if (b'Artemis Konane Server' in data): #initial connection to server
            self.connected = 1
            print("Player connected") 
        elif (b'?Username' in data): #username authentication
            username = bytes(self.username, encoding = 'utf8') + b'\r\n'
            self.socket.sendall(username)
            print("Username sent", username)
        elif (b'?Password' in data): #password authentication
            password = bytes(self.password, encoding = 'utf8') + b'\r\n'
            self.socket.sendall(password)
            print("Password sent", password)
        elif (b'?Opponent' in data): #opponent authentication
            opponent = bytes(self.opponent, encoding = 'utf8') + b'\r\n'
            self.socket.sendall(opponent)
            print("Opponent sent", opponent)
        elif (b'Player' in data) and (b'?Remove' in data) and (b'Removed' not in data): #initial move if coinflip win
            self.socket.sendall(b'[0:0]\r\n')
            print(b'[0:0]\r\n')
        elif (b'?Remove' in data): #initial move if coinflip loss
            self.socket.sendall(b'[0:1]\r\n')
            print(b'[0:1]\r\n')     
        else:
            response = data.splitlines()
            for x in response:
                resp = str(x)
                resp = resp[2:len(resp)-1]
                print(resp)    
    def play(self):
        while True:
            self.read_socket()
buf = 1024
args = sys.argv
p = Player(args[1], args[2], args[3])
p.play()
if False:
    if (b'Game' in data): #game authentication
        continue
    elif (b'Color' in data): #color authentication
        continue
    elif (b'Player' in data) and (b'?Remove' in data) and (b'Removed' not in data): #initial move if coinflip win
        s.sendall(initial)
        send = str(initial)
        print(send[2:len(send)-5])
    elif (b'?Remove' in data): #initial move if coinflip loss
        s.sendall(secondary)
        send = str(secondary)
        print(send[2:len(send)-5])
    elif (b'?Move' in data): #make a move
        s.sendall(move)
        send = str(move)
        print(send[2:len(send)-5])
    elif (b'win' in data): #game is over someone won
        break
    elif (b'Error' in data): #game is over invalid move
        break
p.socket.close()