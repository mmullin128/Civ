from scripts import *
from farmTrain import *
if __name__ == '__main__':
    generate_actions('actions1.txt',{
        '00000001': 'Peasant.farm',
        '00000010': 'Peasant.move_right',
        '00000011': 'Peasant.move_up',
        '00000100': 'Peasant.move_down',
        '00000101': 'Peasant.farm',
        '00000110': 'Peasant.move_vision_cursor_right',
        '00000111': 'Peasant.move_vision_cursor_up',
        '00001000': 'Peasant.move_vision_cursor_left',
        '00001001': 'Peasant.move_vision_cursor_down',
        '00001010': 'Peasant.farm',
        '00001011': 'Peasant.plant',
        '00001100': 'Peasant.harvest',
        '00001101': 'Peasant.eat',
        '00001110': 'Peasant.drop',
        '00001111': 'Peasant.pick_up'     
        })
    #generate_boards('titeBoards',100)
    #see_boards('titeBoards')
    #see_best('record.txt')