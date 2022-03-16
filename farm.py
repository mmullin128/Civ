from object import Object
from corn import Corn
class Farm(Object):
    def __init__(self,board,container,amount,content=[],properties={}):
        color = (180,180,30)
        Object.__init__(self,board,container,color,amount,content,properties)
        self.attrs = ['landmark','standable']
        self.type = 'Farm'
        self.name = 'Farm'
        self.harvest = 0
        self.crop = None
        self.size = 20
        self.id = 2
        self.current = 0
        self.growingRate = .2
        self.maximum = 9
        #for arg in properties:
        #    if arg == 'crop':
        #        self.crop = eval(properties[arg])(board,self,0)
        #        self.add_content([self.crop])
    def add_crop(self,crop):
        self.crop = crop
        self.add_content([crop])
    def update(self,frame):
        if self.crop:
            #self.growingRate = self.container.compute_fertility(self.crop)
            if self.current + self.growingRate < self.maximum: 
                self.current = self.current + self.growingRate
                self.crop.amount = self.current
            #print('growing rate: ', self.growingRate, 'amount: ', self.current)