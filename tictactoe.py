#!/usr/bin/env/ python2.7
import sys
import random
import math

#this is the tic-tac-toe game board
class Board:
    def __init__(self):
        #the elements in board and their corresponding location:
        #   [6,7,8]     [(0,2),(1,2),(2,2)]
        #   [3,4,5]     [(0,1),(1,1),(2,1)]
        #   [0,1,2]     [(0,0),(1,0),(2,0)]
        self.board = ['-' for i in range(9)]
        self.history = []

    #place 'x' or 'o' at the location
    def move(self, player, location):
        if self.board[location] == '-':
            self.board[location] = player

    #undo the move
    def unDo(self, location):
        self.board[location] = '-'

    #get the list of location which could be moved to in the next step
    def legalMove(self):
        move = []
        for i in range(9):
            if self.board[i] == '-':
                move.append(i)
        return move

    #check if it is time to end the game
    def terminate(self):
        move = self.legalMove()
        if len(move) == 0 or self.ifSomeoneWin() != "":
            return True
        else:
            return False

    #get the constraints of the board:
    def constraint(self):
        c = [self.board[0:3], self.board[3:6], self.board[6:9], self.board[0:9:3], 
        self.board[1:9:3], self.board[2:9:3], self.board[0:9:4], self.board[2:7:2]]
        return c

    #check if someone win
    def ifSomeoneWin(self):
        winner = ''
        constraint = self.constraint()
        if ['x','x','x'] in constraint:
            winner = 'x'
        elif ['o','o','o'] in constraint:
            winner = 'o'
        return winner

    #print the board
    def printHelper(self):
        print self.board[6] + "," + self.board[7] + "," + self.board[8]
        print self.board[3] + "," + self.board[4] + "," + self.board[5]
        print self.board[0] + "," + self.board[1] + "," + self.board[2]
        print ""
        self.history.append(self.board)

    #write output to output file
    def writeHistory(self, filename):
        with open(filename, 'w') as f:
            for item in self.history:
                for i in [0, 3, 6]:
                    record = ','.join(str(loc) for loc in item[i:i + 3])
                    f.write(record + "\n")
                f.write("" + '\n')

#this is Player A who moves randomly
class RandomPlayer:
    def __init__(self, identity, seed):
        #id could be 'x' or 'o'
        self.id = identity
        self.seed = seed
        random.seed(self.seed)

    #the action of the player    
    def move(self, board):
        move = board.legalMove()
        length = len(move)
        randIndex = int(math.floor(length * random.random()))
        return move[randIndex]

#this is AI player who use minmax algorithm to decide moves
class AIPlayer:
    def __init__(self, identity):
        #id could be 'x' or 'o'
        self.id = identity

    #this function is for AI to think
    def move(self, board):
        player = AIPlayer('o')
        if self.id == 'o':
            player = AIPlayer('x')

        v, move = self.minmax(board, player, 0)
        return move

    #this is the minmax algorithm
    def minmax(self, board, player, depth):
        bestV = 10
        if self.id == 'o':
            bestV = -10
        if board.terminate() :
            if board.ifSomeoneWin() == 'x':
                return -10 + depth, None
            elif board.ifSomeoneWin() == 'o':
                return 10 - depth, None
            else:
                return 0, None
        bestMove = None
        for move in board.legalMove() :
            board.move(self.id, move)
            val, act = player.minmax(board, self, depth+1)
            board.unDo(move)             
            if self.id == 'o' :
                if val > bestV:
                    bestV, bestMove = val, move
            else :
                if val < bestV:
                    bestV, bestMove = val, move        
        return bestV, bestMove

#this is the main function
def game(seed, output):
    s = int(seed)
    print "seed==", s
    random.seed(s)
    #initialize the participants of the game
    board = Board()
    RP = RandomPlayer('x', s)
    AI = AIPlayer('o')
    #start game
    print "GAME START!!!"
    curPlayer = RP
    winner = ""
    while True:
        curMove = curPlayer.move(board)     
        board.move(curPlayer.id, curMove)   
        board.printHelper()
        if board.terminate(): 
            winner = board.ifSomeoneWin() 
            break
        if curPlayer == RP:
            curPlayer = AI
        else:
            curPlayer = RP
    print "GAME OVER AND THE WINNER IS:", winner
    board.writeHistory(output)
    return winner

#this part is for testing
'''
AIwin = 0
Randomwin = 0
for i in [1,5,10,15,20]:
    winner = game(i)
    if winner == 'o':
        AIwin += 1
    elif winner == 'x':
        Randomwin += 1
draw = 30 - AIwin - Randomwin
print "AI win:", AIwin
print "Random win:", Randomwin
print "draw:", draw
'''

game(sys.argv[1], sys.argv[2])
