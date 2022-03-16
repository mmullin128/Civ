import pygame, math
from game import *
import time
SCREENSIZE = (500,500)
OFFSET = (50,50)
BOARDSIZE = (400,400)
DISPLAY_UPDATE = True
BOARD_UPDATE = False




def main(boardFile):
    board, boardSize = load_board(boardFile)
    screen = pygame.display.set_mode(SCREENSIZE)
    #Cursor = Selector()
    done = False
    draw_board(board,boardSize,screen,BOARDSIZE,OFFSET)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    print('updating', board.time)
                    board, boardSize = update_board(board,boardSize)
                    draw_board(board,boardSize,screen,BOARDSIZE,OFFSET)
        
        #print('updating', board.time)
        #board, boardSize = update_board(board,boardSize)
        #draw_board(board,boardSize,screen,BOARDSIZE,OFFSET)
        #time.sleep(.1)
        #if Cursor.status != "null":
        #    Cursor.draw(screen,boardSize,BOARDSIZE,OFFSET)
        #    if Cursor.status == "static":
        #        print(board[str(Cursor.space)].content)
        
    pygame.quit()
    save_board(board,boardFile)
if __name__ == '__main__':
    main('saves/save3.txt')