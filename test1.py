from game import *
from neuralnetworks import *
board, boardSize = load_board('saves/save1.txt')
def write(pos):
    space = board[str(pos)]
    content = space.unpack_content()
    print(pos, '\n',
    space, '\n',
    'content: ', content,
    )

if __name__ == '__main__':
    generate_csv('poop.csv',3,5,5,2)
    generate_csv('poop1.csv',3,5,5,2)
    NN = NeuralNetwork(file='poop.csv')
    NN1 = NeuralNetwork(file='poop1.csv')
    NN2 = NN.reproduce(NN1)
    NN2.save('poop2.csv')
    #input = [1] * 578
    #NN.propogate(input)
    #for i in range(100):
    #    NN.mutate_random()
    #NN.save('poop.csv')
    