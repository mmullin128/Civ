from object import Object
class Wheat(Object):
    def __init__(self,board,container,amount,content=[],properties={}):
        self.type = 'Crop'
        self.name = 'Wheat'
        self.attrs = ['edible']
        self.nutr = 1
        self.id = 5
        self.size = 1
        color = (0,0,0)
        Object.__init__(self,board,container,color,amount,content,properties)