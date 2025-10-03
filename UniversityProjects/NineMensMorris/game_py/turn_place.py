from board import Board
from enum_sound import SoundID
from mill_checker import MillChecker
from player import Player
from turn import Turn
from util_sound import SoundUtil
from enum_turn_type import TurnType


class PlaceTurn(Turn):
    '''
    all the operation that happen during a place turn
    '''
    def __init__(self, board: Board, player: Player, mill_checker: MillChecker):
        super().__init__(board, player, mill_checker)
        self.set_turn_type(TurnType.place)

    def action(self, index: int):
        '''
        see Turn.action(index)
        '''
        if not self._board.position_occupied(index):  # the selected position is empty
            self.set_selected_empty(index)
            piece = self._player_of_this_turn.get_pile().pop()  # take a piece from the pile
            self._put_piece(self.get_selected_empty(), piece)  # put that piece there
            print("place", self._player_of_this_turn, self.get_selected_piece(), self.get_selected_empty())
            self.set_selected_empty(None)  # reset selected position
            SoundUtil.play_sound(SoundUtil, SoundID.piece)
            self._mill_checker.update_mills(self._board)
            return True     # signaling the end of the turn
        return False

