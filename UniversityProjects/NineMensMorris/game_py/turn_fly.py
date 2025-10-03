from board import Board
from enum_sound import SoundID
from player import Player
from turn import Turn
from util_sound import SoundUtil
from enum_turn_type import TurnType


class FlyTurn(Turn):
    '''
    all the operation that happen during a turn that manipulate piece on the board (move/fly)
    move action is a child class of this class, the different is with/without neighbour checking
    '''
    def __init__(self, board: Board, player: Player, mill_checker):
        super().__init__(board, player, mill_checker)
        self.set_turn_type(TurnType.fly)

    def action(self, index: int):
        '''
        See class Turn.action(index)
        '''
        self._piece_position_validation(index)
        self._empty_position_validation(index)
        if self.get_selected_piece() is not None and self.get_selected_empty() is not None:
            # both position are selected to perform the fly action
            self._put_piece(self.get_selected_empty(), self._remove_piece(self.get_selected_piece()))
            self.set_selected_piece(None)  # reset
            self.set_selected_empty(None)
            self._mill_checker.update_mills(self._board)
            return True
        return False

    def _piece_position_validation(self, index: int):
        '''
        check the condition of selected position w/ piece valid to be selected
        '''
        if self._board.position_occupied(index) and self._board.get_position(index).get_piece() == self._player_of_this_turn.get_colour():
            # if player select it own piece and that p has a piece -> player click to select that piece
            self.set_selected_piece(index)
            print("fly/move - 1", str(self._player_of_this_turn), self.get_selected_piece(), self.get_selected_empty())
            SoundUtil.play_sound(SoundUtil, SoundID.piece)

    def _empty_position_validation(self, index: int):
        '''
        check the condition of selected empty position valid to be selected
        '''
        if self.get_selected_piece() is not None and not self._board.position_occupied(index):
            # if player has selected a piece and then selected p that is empty
            self.set_selected_empty(index)
            print("fly/move - 2", self._player_of_this_turn, self.get_selected_piece(), self.get_selected_empty())
            SoundUtil.play_sound(SoundUtil, SoundID.piece)
