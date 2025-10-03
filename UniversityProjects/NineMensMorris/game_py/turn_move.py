from board import Board
from enum_sound import SoundID
from enum_turn_type import TurnType
from player import Player
from turn_fly import FlyTurn
from util_sound import SoundUtil


class MoveTurn(FlyTurn):
    '''
    all the operation that happen during a turn that manipulate piece on the board (move)
    with neighbour checking
    '''
    def __init__(self, board: Board, player: Player, mill_checker):
        super().__init__(board, player, mill_checker)
        self.set_turn_type(TurnType.move)

    def _empty_position_validation(self, index: int):
        '''
        modified from parent class, with neighbour checking
        check the condition of selected empty position valid to be selected
        '''
        if self.get_selected_piece() is not None and not self._board.position_occupied(index):
            # if player has selected a piece and then selected p that is empty
            self.set_selected_empty(index)
            # if the turn is move it could only move when those nodes are neighbours
            if self.get_selected_empty() not in self._board.get_position(self.get_selected_piece()).get_neighbours():
                print(self.get_selected_empty(), "not in",
                      self._board.get_position(self.get_selected_piece()).get_neighbours())
                SoundUtil.play_sound(SoundUtil,  SoundID.invalid)
                self.set_selected_empty(None)
                return  # wont proceed to move
            print("fly/move - 2", str(self._player_of_this_turn), self.get_selected_piece(), self.get_selected_empty())
            SoundUtil.play_sound(SoundUtil,  SoundID.piece)