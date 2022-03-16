from object import Object
class WheatSeed(Object):
    def __init__(self,board,container,amount,content=[],properties={}):
        self.type = 'Seed'
        self.name = 'Wheat'
        self.crop = 'Wheat'
        self.attrs = ['edible','plantable']
        self.nutr = .1
        self.id = 6
        self.size = 1
        color = (90,90,20)
        Object.__init__(self,board,container,color,amount,content,properties)