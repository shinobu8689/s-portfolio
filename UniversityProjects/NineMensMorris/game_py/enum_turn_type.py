from enum import Enum


class TurnType(Enum):
    '''
    id to identify each turns
    '''
    place = 1
    move = 2
    fly = 3
    remove = 4
