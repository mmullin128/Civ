from object import Object
class CornSeed(Object):
    def __init__(self,board,container,amount,content=[],properties={}):
        self.type = 'Seed'
        self.name = 'Corn'
        self.crop = 'Corn'
        self.attrs = ['edible','plantable']
        self.nutr = .1
        self.id = 4
        self.size = 1
        color = (0,30,0)
        Object.__init__(self,board,container,color,amount,content,properties)