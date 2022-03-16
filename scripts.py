from tokenize import String
from unittest import result
from main import *
from board import *
from peasant import Peasant
import os

def get_best(recordFile):
    results = []
    with open(recordFile, 'r') as f:
        for line in f:
            lineString = line.split()
            scores, networks = eval(lineString[0]), eval(lineString[1])
            results.append([scores,networks])
    return results[::-1]

def see_best(recordFile,boardsDirectory):
    b = 0
    boards = os.listdir(boardsDirectory)
    results = get_best(recordFile)
    for i in range(len(results)):
        print(results[i])
        scores, networks = results[i]
        for n in range(len(scores)):
            boardFile = boards[i%len(boards)]
            print(scores[n], networks[n], boardFile)
            board = Board('load',0,os.path.join(boardsDirectory,boardFile))
            p = Peasant(board,board['(3, 3)'],1,content=[],properties={'mode':'debug','NeuralNetworks':[networks[n]],'actions': 'actions1.txt'})
            board['(3, 3)'].add_content([p])
            save_board(board,'scriptTest.txt')
            main('scriptTest.txt')


def see_boards(boardsDirectory):
    for boardFile in os.listdir(boardsDirectory):
        print(boardFile)
        main(os.path.join(boardsDirectory,boardFile))
        #print('Directory: ', boardsDirectory, ' does not exist!')

def generate_actions(fileName,specified={}):
    for binStr in specified:
        if type(binStr) != str:
            print('action IDs must be string. not ', type(binStr))
            return
        if len(binStr) != 8:
            print(binStr + ' is not an 8 bit binary string')
            return
        for n in binStr:
            if n != '1' and n != '0':
                print(binStr, ' must only contain 1 or 0. Found: ', n)
                return
    file = open(fileName,'w')
    for a in range(256):
        binStr = format(a,'08b')
        if binStr in specified:
            fn = specified[binStr]
            file.writelines(binStr + ' ' + fn + '\n')
        else:
            fn = 'Peasant.do_nothing'
