import pygame, math
from spaces import *
from objects import *
grass1Color = (0, 255, 0)
water1Color = (0, 0, 255)
grass2Color = (1,1,1)
grass3Color = (1,1,1)
water1Color = (1,1,1)
water2Color = (1,1,1)
water3Color = (1,1,1)
hill1Color = (1,1,1)
hill2Color = (1,1,1)
hill3Color = (1,1,1)
ridge1Color = (1,1,1)
ridge2Color = (1,1,1)
ridge3Color = (1,1,1)



class Board:
    def __init__(self,type,time=0,board={},boardSize=[0,0]):
        self.time = time
        self.activeObjects = []
        if type == 'load':
            self.board, self.boardSize = load_board(board)
        else:
            self.board = board
            self.boardSize = boardSize
    def add_item(self,item,pos):
        if hasattr(item,'update'):
            self.activeObjects.append(item)
        self.board[str(pos)].add_content([item])
    def __setitem__(self,space: str,data):
        pos = eval(space)
        if pos[0]+1 > self.boardSize[0]:
            self.boardSize[0] = pos[0]+1
        if pos[1]+1 > self.boardSize[1]:
            self.boardSize[1] = pos[1]+1
        self.board[space] = data
    def __getitem__(self, space: str):
        return self.board[space]
    def __iter__(self):
        self.itx = -1
        self.ity = 0
        self.it = f'({self.itx}, {self.ity})'
        return self
    def __next__(self):
        if (self.itx == self.boardSize[0]-1 and self.ity == self.boardSize[1]-1):
            raise StopIteration
        else:
            if (self.itx == self.boardSize[0]-1):
                self.ity += 1
                self.itx = 0
            else:
                self.itx += 1
            self.it = f'({self.itx}, {self.ity})'
            return self.it


def create_items(Board,container,items):
    newItems = []
    for CLASS, AMOUNT, ATTR, ITEMS in items:
        C = eval(CLASS)
        item = C(Board,container,AMOUNT,content=[],properties=ATTR)
        item.add_content(create_items(Board,item,ITEMS))
        newItems.append(item)
    return newItems


def load_board(fileName):
    board = Board('new')
    boardSizeX = 0
    boardSizeY = 0
    file = open(fileName, "r")
    for line in file:

        lineString = line.split()
        SPACE_CLASS = eval(lineString[1])
        SPACE_POS = eval(lineString[0])
        SPACE_CONTENT = eval(lineString[2])
        if SPACE_POS[0] > boardSizeX:
            boardSizeX = SPACE_POS[0]
        if SPACE_POS[1] > boardSizeY:
            boardSizeY = SPACE_POS[1]
            
        space = SPACE_CLASS(board,SPACE_POS,content=[],properties={})
        content = create_items(board,space,SPACE_CONTENT)
        space.add_content(content)
        board[str(SPACE_POS)] = space
        boardSize = (boardSizeX+1, boardSizeY+1)
    return board, boardSize

def save_board(board,fileName):
    file = open(fileName, "w")
    for pos in board:
        space = board[pos]
        content = space.unpack_content()
        file.writelines(pos.replace(" ", "") + ' ' + str(type(space).__name__) + ' ' + str(content).replace(" ", "") + '\n')

def get_board_surface(board, boardSize,BOARDSIZE):
    surface = pygame.Surface(BOARDSIZE)
    surface.fill((100,0,0))
    for strPos in board:
        pos = eval(strPos)
        space = board[strPos]
        left = pos[0]*(BOARDSIZE[0]/boardSize[0])
        width = (BOARDSIZE[0]/boardSize[0])
        top = pos[1]*(BOARDSIZE[1]/boardSize[1])
        height = (BOARDSIZE[1]/boardSize[1])
        #print(left, width, top, height)
        color = (0,0,0)
        if len(space.content) == 0:
            color = space.color
        else:
            color = space.content[0].color
        pygame.draw.rect(surface,color,pygame.Rect(left,top,width,height))
    return surface
def update_content(board,container):
    for item in container.content:
        if hasattr(item,'update'):
            item.update(frame=board.time)
        update_content(board,item)
def update_board(board,boardSize):
    board.time += 1
    for obj in board.activeObjects:
        obj.update(board.time)
    return board, board.boardSize
def draw_board(board,boardSize,screen,BOARDSIZE,OFFSET):
    boardSurface = get_board_surface(board, boardSize,BOARDSIZE)
    screen.blit(boardSurface,OFFSET)
    pygame.display.update()














class Selector:
    def __init__(self,status="floating",color=(200,200,200),space=None):
        self.space = space
        self.status=status
        self.color = color
    def select(self,space):
        self.status = "static"
        self.space = space
    def deselect(self):
        self.status = "floating"
        self.space = None
    def move(self,x,y):
        currentSpace = self.space.pos
        self.deselect()
        self.select((currentSpace[0]+x,currentSpace[1]+y))
    def draw(self,surface,boardSize,BOARDSIZE,OFFSET):
        if self.status == "floating":
            mousePos = pygame.mouse.get_pos()
            pos = (int(math.floor((mousePos[0]-OFFSET[0])/(BOARDSIZE[0]/boardSize[0]))),int(math.floor((mousePos[1]-OFFSET[1])/(BOARDSIZE[1]/boardSize[1]))))
            if pos[0] >= 0 and pos[0] <= boardSize[0]-1 and pos[1] >= 0 and pos[1] <= boardSize[1]-1:
                width = int((BOARDSIZE[0]/boardSize[0]))
                height = width
                left = pos[0]*width+OFFSET[0]
                top = pos[1]*height+OFFSET[1]
                pygame.draw.rect(surface,self.color,pygame.Rect(left,top,width,height),10)
                pygame.display.update()
                pygame.draw.rect(surface,(0,0,0),pygame.Rect(left,top,width,height),10)
                if pygame.mouse.get_pressed()[0]:
                    self.space = pos
                    self.status = "static"
        elif self.status == "static":
            if pygame.mouse.get_pressed()[0]:
                    self.space = None
                    self.status = "floating"