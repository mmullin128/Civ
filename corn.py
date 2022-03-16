from object import Object
class Corn(Object):
    def __init__(self,board,container,amount,content=[],properties={}):
        self.type = 'Crop'
        self.name = 'Corn'
        self.seed = 'CornSeed'
        self.attrs = ['edible']
        self.id = 3
        self.nutr = .8
        self.size = 1
        color = (80,200,80)
        Object.__init__(self,board,container,color,amount,content,properties)