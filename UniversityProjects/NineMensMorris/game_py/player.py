from enum_player import PlayerColour
from enum_turn_type import TurnType
from board import Board

class Player:
    '''
    for storing the player information (who is this player and the amount of pieces that have not been placed on the board yet
    '''

    def __init__(self, colour: PlayerColour, pile_pieces: int = 9):
        self._colour = colour
        self._piece_pile = [self._colour] * pile_pieces
        self._phase = TurnType.place

    def get_colour(self) -> PlayerColour:
        return self._colour

    def get_pile(self) -> list:
        return self._piece_pile

    def set_phase(self, turn_type: TurnType):
        self._phase = turn_type

    def get_phase(self) -> TurnType:
        return self._phase

    def __str__(self):
        return str(self._colour)

    def get_player_pieces_position(self, board: Board):
        return [position.get_index() for position in board.positions if position.get_piece() == self._colour]
