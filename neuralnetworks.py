import math, csv, random
import numpy as np


def linear(x):
    return x
def sigmoid(x,cap=10):
    if x < -cap:
        x = -cap
    if x > cap:
        x = cap
    return 1/(1+math.pow(math.e,-x))

class NeuralNetwork:
    def __init__(self,file,shape=None):
        if file == 'random':
            if shape == None:
                print('provide shape for random Neural Network')
                return
            numOfIn, numOfHid, nodesPerLayer, numOfOut = shape
            self.numOfIn, self.numOfHid, self.nodesPerLayer, self.numOfOut = numOfIn, numOfHid, nodesPerLayer, numOfOut
            inputWeights = []
            hiddenWeights = []
            outputWeights = []
            for node in range(numOfIn):
                data = [random.random()*2-1 for i in range(nodesPerLayer)]
                inputWeights.append(data)
            self.inputWeights = (np.array(inputWeights))
            self.hiddenWeights = []
            for h in range(numOfHid-1):
                hiddenWeights.append([])
                for node in range(nodesPerLayer):
                    data = [random.random()*2-1 for i in range(nodesPerLayer)]
                    hiddenWeights[h].append(data)
                
                self.hiddenWeights.append(np.array(hiddenWeights[h]))
            self.hiddenWeights = np.array(self.hiddenWeights)
            for node in range(nodesPerLayer):
                data = [random.random()*2-1 for i in range(numOfOut)]
                outputWeights.append(data)
            self.outputWeights = np.array(outputWeights)
            return
        file = open(file, "r")
        datareader = csv.reader(file)
        dimensions = datareader.__next__()
        numOfIn, numOfHid, nodesPerLayer, numOfOut = int(dimensions[0]),int(dimensions[1]),int(dimensions[2]),int(dimensions[3])
        self.numOfIn, self.numOfHid, self.nodesPerLayer, self.numOfOut = numOfIn, numOfHid, nodesPerLayer, numOfOut
        self.shape = (numOfIn, numOfHid, nodesPerLayer, numOfOut)
        inputWeights = []
        hiddenWeights = []
        outputWeights = []
        for node in range(numOfIn):
            data = datareader.__next__()
            inputWeights.append([float(i) for i in data])
        self.inputWeights = (np.array(inputWeights))
        self.hiddenWeights = []
        for h in range(numOfHid-1):
            hiddenWeights.append([])
            for node in range(nodesPerLayer):
                data = datareader.__next__()
                hiddenWeights[h].append([float(i) for i in data])
            
            self.hiddenWeights.append(np.array(hiddenWeights[h]))
        self.hiddenWeights = np.array(self.hiddenWeights)
        for node in range(nodesPerLayer):
            data = datareader.__next__()
            outputWeights.append([float(i) for i in data])
        self.outputWeights = np.array(outputWeights)
    def propogate(self,input):
        inArray = np.array([input])
        nw = np.matmul(inArray, self.inputWeights)
        vfunc = np.vectorize(sigmoid)
        #print(np.shape(inArray),np.shape(self.inputWeights))
        h1 = vfunc(nw)
        #print(h1)
        for h in self.hiddenWeights:
            #print(np.shape(h1),np.shape(h))
            hnw = np.matmul(h1, h)
            h1 = vfunc(hnw)
            #print(h1)
        fnw = np.matmul(h1, self.outputWeights)
        final = vfunc(fnw)
        #print(final)
        return final[0]
    def reproduce(self,NN,w=.4):
        if self.shape == NN.shape:
            self.inputWeights = ((1-w)*self.inputWeights) + (w * NN.inputWeights)
            self.hiddenWeights = ((1-w)*self.hiddenWeights) + (w * NN.hiddenWeights)
            self.outputWeights = ((1-w)*self.outputWeights) + (w * NN.outputWeights)
            return self
    def mutate_random(self,dW=.01):
        directionBool = random.choice((-1,1))
        nLayers = 2 + self.hiddenWeights.shape[0]
        layer = random.randrange(0,nLayers)
        if layer == 0:
            node = random.randrange(0,self.inputWeights.shape[0])
            weight = random.randrange(0,self.inputWeights.shape[1])
            location = [layer,node,weight]
            oldVal = self.inputWeights[node,weight]
            self.inputWeights[node,weight] += dW*directionBool
        elif layer == nLayers-1:
            node = random.randrange(0,self.outputWeights.shape[0])
            weight = random.randrange(0,self.outputWeights.shape[1])
            location = [layer,node,weight]
            oldVal = self.outputWeights[node,weight]
            self.outputWeights[node,weight] += dW*directionBool
        else:
            node = random.randrange(0,self.hiddenWeights.shape[1])
            weight = random.randrange(0,self.hiddenWeights.shape[2])
            location = [layer,node,weight]
            oldVal = self.hiddenWeights[layer-1,node,weight]
            self.hiddenWeights[layer-1,node,weight] += dW*directionBool
        return self
        #print(location, oldVal)
    def save(self,fileName):
        numOfIn, numOfHid,nodesPerLayer, numOfOut = self.numOfIn, self.numOfHid, self.nodesPerLayer, self.numOfOut
        with open(fileName, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([numOfIn,numOfHid,nodesPerLayer,numOfOut])
            writer.writerows(
                self.inputWeights
            )
            #writer.writerow([])
            for h in range(numOfHid-1):
                writer.writerows(
                            self.hiddenWeights[h]
                        )
            writer.writerows(
                self.outputWeights
            )

def generate_csv(fileName,numOfIn,numOfHid,nodesPerLayer,numOfOut):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([numOfIn,numOfHid,nodesPerLayer,numOfOut])
        inputWeights = []
        for node in range(numOfIn):
            inputWeights.append([])
            for node2 in range(nodesPerLayer):
                inputWeights[node].append(random.random()*2-1)
        writer.writerows(
            inputWeights
        )
        #writer.writerow([])
        for h in range(numOfHid-1):
            hiddenLayer = []
            for node in range(nodesPerLayer):
                hiddenLayer.append([])
                for node2 in range(nodesPerLayer):
                    hiddenLayer[node].append(random.random()*2-1)
            writer.writerows(
                        hiddenLayer
                    )

        outputWeights = []
        for node in range(nodesPerLayer):
            outputWeights.append([])
            for node2 in range(numOfOut):
                outputWeights[node].append(random.random()*2-1)
        writer.writerows(
            outputWeights
        )
