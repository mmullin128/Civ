from object import Object
class House(Object):
    def __init__(self,board,container,amount,content=[],properties={}):
        self.type = 'Building'
        self.name = 'House'
        self.attrs = ['enterable']
        self.size = 15
        self.occupancy = 0
        self.hostility = 0
        self.id = 7
        self.maxOccupancy = 4
        color = (60,60,20)
        Object.__init__(self,board,container,color,amount,content,properties)