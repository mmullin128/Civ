from scripts import *
from farmTrain import *
if __name__ == '__main__':
    trainer = Trainer('titeBoards','Training1','actions1.txt','record.txt',shape=[480,10,5,16],generationSize=300,surviveThreshold=100,randomizeThreshold=5)
    trainer.train(200)
    see_best('record.txt','titeBoards')
    #generate_boards('titeBoards',100)
    #see_boards('titeBoards')
    #see_best('record.txt')