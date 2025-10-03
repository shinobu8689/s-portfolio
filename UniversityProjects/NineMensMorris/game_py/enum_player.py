from enum import Enum

class PlayerColour(Enum):
    '''
    possible pieces colour or winner
    '''
    draw = 0 # indicate no one wins only
    white = 1
    black = 2
