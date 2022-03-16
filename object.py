class Object:
    def __init__(self,board,container,color,amount,content=[],properties={}):
        self.board = board
        self.container = container
        self.amount = amount
        self.color = color
        self.content = content
        self.properties = properties
    def add_content(self,content):
        for item in content:
            if hasattr(item,'update'):
                self.board.activeObjects.append(item)
            self.content.append(item)
    def remove_content(self,content):
        for item in content:
            if hasattr(item,'update'):
                self.board.activeObjects.remove(item)
            self.content.remove(item)
    def change_container(self,newContainer):
        self.container = newContainer
    def unpack_content(self):
        unpacked_content = []
        for item in self.content:
            unpacked_content.append((str(type(item).__name__),item.amount,item.properties,item.unpack_content()))
        return unpacked_content