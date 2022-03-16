from objects import *


class Space:
    def __init__(self,board,pos,color,content=[],properties={}):
        self.board = board
        self.pos = pos
        self.color = color
        self.content = content
        self.properties = properties
    def add_content(self,content): #list of items to add
        for item in content:
            if hasattr(item,'update'):
                self.board.activeObjects.append(item)
            self.content.append(item)
    def remove_content(self,content): #list of items to add
        for item in content:
            if hasattr(item,'update'):
                self.board.activeObjects.remove(item)
            self.content.remove(item)
    def unpack_content(self):
        unpacked_content = []
        for item in self.content:
            unpacked_content.append((str(type(item).__name__),item.amount,item.properties,item.unpack_content()))
        return unpacked_content
class Grass1(Space):
    def __init__(self,board,pos,content=[],properties={}):
        self.id = 1
        self.type = 'Land'
        self.name = 'Grass1'
        self.attrs = ['enterable']
        self.hostility = .05
        self.baseFertility = 1.0
        Space.__init__(self,board,pos,(10,200,10),content,properties)
    def compute_fertility(self,crop):
        return self.baseFertility*crop.baseFertility
    def update(self,neighbors):
        pass
        #print(self.pos, self.content)
class Grass2(Space):
    def __init__(self,board,pos,content=[],properties={}):
        self.id = 2
        self.type = 'Land'
        self.name = 'Grass2'
        self.attrs = ['enterable']
        self.hostility = .08
        self.baseFertility = .8
        Space.__init__(self,board,pos,(10,150,10),content,properties)
    def compute_fertility(self,crop):
        print(crop)
        return self.baseFertility*crop.baseFertility