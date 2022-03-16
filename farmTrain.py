from fileinput import filename
import traceback
from game import *
from neuralnetworks import *
from board import *
from peasant import Peasant
import time
from quicksort import *
import random
from os import listdir, mkdir
from os.path import isfile, join, exists
import copy
directory = 'FarmTraining/'
SHAPE = (32,5,5,1)
generationSize = 1000
surviveThreshold = 10
minimumTime = 40
goal = 100

scores = []

def parseData(data):
    return str(data).replace(" ", "")

def populate(fileName,num,shape):
    files = []
    for i in range(num):
        generate_csv(directory + fileName + str(i) + '.csv',shape[0],shape[1],shape[2],shape[3])
        files.append(directory + fileName + str(i) + '.csv')
    return files
def add_player(board,pos,networkFile):
    player = Peasant(board,board[str(pos)],1,content=[],properties={'NeuralNetworks':[networkFile]})
    board[str(pos)].add_content([player])
    return player

def test(networkFile,boardFile):
    #print(networkFile)
    board, boardSize = load_board(boardFile)
    pos = (3,1)
    player = add_player(board,pos,networkFile)
    while player.status != 'dead':
        board, boardSize = update_board(board,boardSize)
    return board.time*3 + player.farmed*1.5 + player.pickedUp*2 + player.ate*40 + player.traveled*0 + player.planted*2 + player.harvested*2
#def read_index(indexFile):


def train(boards,new=True,fileName='network'):
    if new:
        files = populate(fileName,generationSize,SHAPE)
    else:
        files = [directory + f for f in listdir(directory) if isfile(join(directory, f))]
        #files = [f for f in listdir(directory)]
    done = False
    t = 0
    while not done:
        scores = []
        
        boardFile = boards[random.randrange(0,len(boards))]
        for file in files:
            score = test(file,boardFile)
            scores.append(score)
        quicksort(scores,0,len(scores)-1,keys=[files])
        i = len(scores)
        children = []
        parentScores = []
        parentFiles = []
        for a in range(surviveThreshold):
            i -= 1
            Parent1 = NeuralNetwork(files[i])
            Parent2 = NeuralNetwork(files[i-1])
            #Parent2.mutate_random()
            #Parent2.save(files[i-1])
            if scores[i] == scores[i-1]:
                children.append(Parent2.mutate_random(dW=.1))
            else:
                children.append(Parent1.reproduce(Parent2))
            parentFiles.append(files[i])
            parentScores.append(scores[i])
        a = 0
        while i >= 0:
            if a == len(children):
                a = 0
            if i > 0:
                mutatedChild = children[a].mutate_random(dW=.1)
                mutatedChild.save(files[i])
            elif i == 0:
                generate_csv(files[i],SHAPE[0],SHAPE[1],SHAPE[2],SHAPE[3])
            a += 1
            i -= 1
        #generate_csv(files[a],SHAPE[0],SHAPE[1],SHAPE[2],SHAPE[3])
        record = open('record.txt', 'a')
        record.writelines(str(t) + ' ' + parseData(parentScores) + ' ' + boardFile + ' ' + parseData(parentFiles) + '\n')
        t += 1
    record.close()

def generate_boards(testBoardsDirectory,n,boardSize=[10,10]):
    if not exists(testBoardsDirectory):
        mkdir(testBoardsDirectory)
    itemsList = [(('Farm',1,{},[]),1),(('Corn',1,{},[]),1),(('CornSeed',1,{},[]),1)]
    print(n)
    for a in range(n):
        items = {}
        for item in itemsList:
            for i in range(item[1]):
                pos = (random.randrange(0,boardSize[0]),random.randrange(0,boardSize[1]))
                while str(pos) in items:
                    pos = (random.randrange(0,boardSize[0]),random.randrange(0,boardSize[1]))
                items[str(pos)] = item[0]
        fileName = testBoardsDirectory + '/' + testBoardsDirectory + str(a) + '.txt'
        file = open(fileName,'w')
        for x in range(boardSize[0]):
            for y in range(boardSize[1]):
                content = []
                if str((x,y)) in items:
                    content.append(items[str((x,y))])
                file.writelines(str((x,y)).replace(" ", "") + ' ' + 'Grass1' + ' ' + str(content).replace(" ", "") + '\n')
        file.close()

def get_random_board_pos(board):
    pos = (random.randrange(0,board.boardSize[0]),random.randrange(0,board.boardSize[1]))
    while len(board[str(pos)].content) != 0:
        pos = (random.randrange(0,board.boardSize[0]),random.randrange(0,board.boardSize[1]))
    return pos


def goToHouseError(player,board,objs):
    print('computing error')

class Trainer:
    def __init__(self,boardsDirectory,networkDirectory,actionsFile,recordFile,shape=None,generationSize=100,surviveThreshold=3,randomizeThreshold=300):
        self.boardDirectory = boardsDirectory
        self.actionsFile = actionsFile
        self.networkDirectory = networkDirectory
        self.recordFile = recordFile
        self.generationSize = generationSize
        self.baseNetworks = []
        self.shape = shape
        self.surviveThreshold = surviveThreshold
        self.randomizeThreshold = randomizeThreshold
        self.networkFiles = []
        self.Networks = []
        self.boardFiles = []
        self.Boards = []
        self.Actions = {}
        #networkDirectory 
        if not exists(networkDirectory):
            mkdir(networkDirectory)
        l = len(listdir(networkDirectory))
        if l == 0 and shape == None:
            print('To create a new network, <shape>, must be specified')
            return
        while l < generationSize:
            fileName = networkDirectory + '/' + networkDirectory + str(l) + '.csv'
            generate_csv(fileName,shape[0],shape[1],shape[2],shape[3])
            l += 1
        #boardDirectory
        if not exists(boardsDirectory):
            mkdir(boardsDirectory)
        l = len(listdir(boardsDirectory))
        if l == 0:
            generate_boards(boardsDirectory,100)
        
        #store data
        for boardFile in listdir(boardsDirectory):
            board, size = load_board(join(boardsDirectory,boardFile))
            self.boardFiles.append(boardFile)
            self.Boards.append(board)
        for networkFile in listdir(networkDirectory):
            self.networkFiles.append(networkFile)
            self.Networks.append(NeuralNetwork(join(networkDirectory,networkFile)))
        #actionsFile
        file = open(actionsFile,'r')
        for line in file:
            key, action = line.split()
            self.Actions[key] = eval(action)
    def train(self,quitThreshold):
        highScore = 0
        boardIndex = 0
        networkIndex = 0
        boardsNum = len(self.Boards)
        networksNum = len(self.Networks)
        scores = []
        
        while highScore < quitThreshold:
            board = copy.deepcopy(self.Boards[boardIndex])
            pos = get_random_board_pos(board)
            #player = Peasant(board,board[str(pos)],1,[],{'NeuralNetworks':[self.Networks[networkIndex]],'actions':self.Actions})
            foundNetwork = False
            while not foundNetwork:
                player = Peasant(board,board[str(pos)],1,[],{'NeuralNetworks':[self.Networks[networkIndex]],'actions':self.Actions})
                if player.propogate() != False:
                    #print(self.baseNetworks)
                    foundNetwork = True
                    #self.baseNetworks.append(self.Networks[networkIndex])
                else:
                    #if len(self.baseNetworks) > 0:
                    #    self.Networks[networkIndex] = self.baseNetworks[0]
                    #else:
                    self.Networks[networkIndex] = NeuralNetwork('random',self.shape)
            #player.add_content([Corn(board,player,1,[],{})])
            hpos = get_random_board_pos(board)
            player.add_error_function(goToHouseError,[house])
            board.add_item(player,pos)
            while player.status == 'alive':
                if board.time > quitThreshold:
                    print('survived longer than ', quitThreshold)
                    #break
                board, size = update_board(board,board.boardSize)
            scores.append(board.time)
            networkIndex += 1
            #print(networkIndex)
            if networkIndex == networksNum: 
                #print(len(scores),' = ',networksNum)
                #time.sleep(1)
                net = self.Networks
                netF = self.networkFiles
                quicksort(scores,0,networksNum-1,keys=[net,netF])
                #print(scores,self.networkFiles)
                self.Networks = net
                self.networkFiles = netF
                survived = []
                highScores = []
                survivedFiles = []
                for a in range(-1,-self.surviveThreshold-1,-1):
                    survived.append(self.Networks[a])
                    highScores.append(scores[a])
                    survivedFiles.append(self.networkDirectory + '/' + self.networkFiles[a])
                    self.Networks[a].save(self.networkDirectory + '/' + self.networkFiles[a])
                highScore = highScores[0]
                recordFile = open(self.recordFile,'a')
                recordFile.writelines(str(highScores).replace(' ','') + ' ' + str(survivedFiles).replace(' ','') + '\n')
                recordFile.close()
                for a in range(self.surviveThreshold,len(self.Networks)-self.randomizeThreshold):
                    sI = a % self.surviveThreshold + 1
                    child = copy.deepcopy(self.Networks[-sI])
                    #self.Networks[-sI].mutate_random(dW=.01)
                    child.mutate_random(dW=.01)
                    self.Networks[-a-1] = child
                    self.Networks[-a-1].save(self.networkDirectory + '/' + self.networkFiles[-a-1])
                for a in range(self.randomizeThreshold):
                    self.Networks[a] = NeuralNetwork('random',shape=self.shape)
                    self.Networks[a].save(self.networkDirectory + '/' + self.networkFiles[a])
                scores = []
                networkIndex = 0
            boardIndex += 1
            if boardIndex == boardsNum: boardIndex = 0
        #files = [f for f in listdir(directory)]
        #if len(listdir(networkDirectory)) == 0:












if __name__ == '__main__':
    files = [directory + f for f in listdir(directory) if isfile(join(directory, f))]
    if len(files) == 0:
        new = True
    else:
        new = False
    boards = ['saves/' + f for f in listdir('saves') if isfile(join('saves', f))]
    train(boards,new=True)
