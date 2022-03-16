import traceback
from game import *
from neuralnetworks import *

board, boardSize = load_board('saves/save4.txt')





def Fupdate_board():
    global board
    global boardSize
    board, boardSize = update_board(board,boardSize)





if __name__ == '__main__':
    done = False
    player = None
    script = open('script1', "r")
    for strSpace in board:
        for item in board[strSpace].content:
            if type(item) == Peasant:
                player = item
    for command in script:
        try:
            if command == 'quit':
                break
            else:
                eval(command)
                print(command, player.get_pos(), player.visionCursorPos)
            for strSpace in board:
                for item in board[strSpace].content:
                    if hasattr(item,'update'):
                        item.update(board.time)
                #print(strSpace, board[strSpace].content)
        except Exception as e:
            print(traceback.format_exc())
            save_board(board,'saves/newFile.txt')
    save_board(board,'saves/newFile.txt')