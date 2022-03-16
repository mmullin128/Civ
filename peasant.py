import re
from neuralnetworks import NeuralNetwork
from object import Object
from farm import Farm
from corn import Corn
from cornseed import CornSeed
from pathlib import Path
from house import House
import math
import time
statusCodesDirectory = Path("/")

def get_neighbors(pos,s,boardSize):
    n = []
    d = math.floor(s/2)
    for ix in range(-d,d+1):
        for iy in range(-d,d+1):
            if not (ix == 0 and iy == 0):
                npos = (pos[0]+ix,pos[1]+iy)
                if (npos[0] >= 0 and npos[0] < boardSize[0] and npos[1] >= 0 and npos[1] < boardSize[1]):
                    n.append((pos[0]+ix,pos[1]+iy))
                else:
                    n.append(None)
    return n

class Peasant(Object):
    def __init__(self,board,container,amount,content=[],properties={}):
        color = (100,0,0)
        Object.__init__(self,board,container,color,amount,content,properties)
        self.visionCursorPos = self.get_pos()
        self.visionCursorSize = 5
        self.type = 'Peasant'
        self.name = 'Peasant'
        self.attrs = ['actor']
        self.selected_content = 0
        self.id = 1
        self.mode = None
        self.status = 'alive'
        self.health = 10
        self.compute_error = None
        self.tiredness = 0
        self.error = 0
        self.computeErrorObjs = []
        self.hunger = 0
        self.hungerIncrement = .01
        self.hungerIntensity = .5
        self.size = 5
        self.thirst = 0
        self.max_content = 5
        self.NN = []
        self.mode, self.actions = None, None
        self.properties = properties
        if 'NeuralNetworks' in properties and 'actions' not in properties:
            print('actions must be specified for neural network')
            return

        for prop in properties:
            if prop == 'NeuralNetworks':
                for obj in properties[prop]:
                    if type(obj) == str:
                        self.NN.append(NeuralNetwork(obj))
                    elif type(obj) == NeuralNetwork:
                        self.NN.append(obj)
            if prop == 'mode':
                self.mode = properties[prop]
            if prop == 'actions':
                if type(properties[prop]) == str:
                    self.actions = {}
                    file = open(properties[prop],'r')
                    for line in file:
                        key, action = line.split()
                        self.actions[key] = eval(action)
                    file.close()
                else:
                    self.actions = properties[prop]
            if prop == 'idcodes':
                if type(properties[prop]) == str:
                    self.idcodes = []
                    i = 0
                    file = open(properties[prop],'r')
                    for line in file:
                        item = line.split()
                        self.idcodes.append(item)
                        i += 1
                    file.close()
    def get_pos(self):
        container = self.container
        foundPos = False
        while not foundPos:
            if hasattr(container,'pos'):
                pos = container.pos
                foundPos = True
            else:
                container = container.container
        return pos
    def do_nothing(self):
        pass
    def move(self,direction):
        #try:
        container = self.container
        foundPos = False
        while not foundPos:
            if hasattr(container,'pos'):
                newpos = (container.pos[0]+direction[0], container.pos[1]+direction[1])
                if newpos[0] < 0 or newpos[0] >= self.board.boardSize[0] or newpos[1] < 0 or newpos[1] >= self.board.boardSize[1]:
                    return
                newspace = self.board[str(newpos)]
                foundPos = True
            else:
                container = container.container
        if len(newspace.content) != 0:
            for item in newspace.content:
                if item.size > 10:
                    if 'enterable' not in item.attrs and 'standable' not in item.attrs:
                        return
                    if 'enterable' in item.attrs:
                        self.container.remove_content([self])
                        self.container = item
                        item.add_content([self])
                        self.move_vision_cursor(direction)
                        return
        self.move_vision_cursor(direction)
        self.container.remove_content([self])
        self.container = newspace
        newspace.add_content([self])
    def move_right(self):
        self.move((1,0))
    def move_up(self):
        self.move((0,-1))
    def move_left(self):
        self.move((-1,0))
    def move_down(self):
        self.move((0,1))
    def move_vision_cursor(self,direction):
        newpos = [self.visionCursorPos[0]+direction[0], self.visionCursorPos[1]+direction[1]]
        if newpos[0] < 0 or newpos[0] >= self.board.boardSize[0] or newpos[1] < 0 or newpos[1] >= self.board.boardSize[1]:
            return None
        self.visionCursorPos = newpos
    def move_vision_cursor_right(self):
        self.move_vision_cursor((1,0))
    def move_vision_cursor_up(self):
        self.move_vision_cursor((0,-1))
    def move_vision_cursor_left(self):
        self.move_vision_cursor((-1,0))
    def move_vision_cursor_down(self):
        self.move_vision_cursor((0,1))
    def farm(self):
        if self.container.type == 'Land':
            landmarksBool = False
            for item in self.container.content:
                if item.type == 'LandMark':
                    landmarksBool = True
            if not landmarksBool:
                self.container.add_content([Farm(self.board,self.container,1)])
    def cycle_content(self):
        self.selected_content += 1
        if self.selected_content == len(self.content):
            self.selected_content = 0
    def onFarm(self):
        onFarm = False
        farm = None
        for item in self.container.content:
            if item.type == 'Farm':
                onFarm = True
                farm = item
                break
        return onFarm, farm
    def plant(self):
        if len(self.content) == 0:
            return None
        seed = self.content[self.selected_content]
        if seed.type == 'Seed':
            onFarm, farm = self.onFarm()          
            if onFarm:
                self.content.remove(seed)
                newCrop = eval(seed.crop)(self.board,self,0)
                farm.add_crop(newCrop)
    def pick_up(self):
        if len(self.content) < self.max_content and len(self.container.content) > 0:
            for i in range(len(self.container.content)):
                item = self.container.content[i]
                if item.size > 2:
                    continue
                else:
                    self.add_content([item])
                    self.container.remove_content([self.container.content[0]])
                    break
    def drop(self):
        if len(self.content) > 0 and self.selected_content < len(self.content):
            item = self.content[self.selected_content]
            self.content.remove(item)
            self.container.add_content([item])
    def harvest(self):
        onFarm, farm = self.onFarm()
        if onFarm:
            for item in farm.content:
                if item.type == 'Crop':
                    farm.remove_content([item])
                    self.add_content([item])
                    newSeed = eval(item.seed)(self.board,self,1)
                    self.add_content([newSeed])
    def eat(self):
        if len(self.content) > 0 and self.selected_content < len(self.content):
            item = self.content[self.selected_content]
            if 'edible' in item.attrs:
                eatAmount = self.hunger/item.nutr
                if eatAmount <= item.amount:
                    item.amount -= eatAmount
                    self.hunger = 0
                elif eatAmount > item.amount:
                    self.hunger -= item.amount*item.nutr
                    self.remove_content([item])
    def add_error_function(self,fn,objs=[]):
        self.compute_error = fn
        self.computeErrorObjs = objs
    def propogate(self):
        neighbors = get_neighbors(self.visionCursorPos,self.visionCursorSize,self.board.boardSize)
        inputs = []
        for pos in neighbors:
            if pos == None:
                for a in range(20):
                    inputs.append(0)
            else:
                strPos = str(pos)
                space = self.board[strPos]
                for a in range(4):
                    if a == space.id:
                        inputs.append(1)
                    else:
                        inputs.append(0)
                if len(space.content) == 0:
                    for a in range(16):
                        inputs.append(0)
                else:
                    for a in range(16):
                        existsBool = False
                        for obj in space.content:
                            if obj.id == a:
                                existsBool = True
                        if existsBool:
                            inputs.append(1)
                        else:
                            inputs.append(0)
        out = self.NN[0].propogate(inputs)
        max = 0
        i = 0
        for n in range(len(out)):
            if out[n] > max:
                max = out[n]
                i = n
        
        outWord = str(i)
        try:
            action = self.actions[outWord]
            if self.mode == 'debug':
                print(outWord, self.actions[outWord], self.visionCursorPos)
                time.sleep(.1)
            return action
        except:
            print(outWord, ' not in actions')
            return False
    def update(self,frame):
        #hunger
        self.hunger += self.hungerIncrement
        if self.hunger > 0:
            self.health -= self.hunger*self.hungerIntensity
        if self.health <= 0:
            self.container.remove_content([self])
            self.status = 'dead'
            return
        #exposure
        self.health -= self.container.hostility
        #neural networks
        if 'NeuralNetworks' in self.properties:
            action = self.propogate()
            if not action:
                self.do_nothing()
            else:
                action(self)
        self.compute_error(self,self.board,self.computeErrorObjs)
        #time.sleep(.05) 
        #if self.actionCodes[action] != self.lastAction:
        #    if self.lastAction != None:
        #        #raise TypeError
        #        pass
        #    self.lastAction = self.actionCodes[action]