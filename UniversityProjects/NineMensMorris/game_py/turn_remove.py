from board import Board
from enum_sound import SoundID
from enum_turn_type import TurnType
from mill_checker import MillChecker
from player import Player
from turn import Turn
from util_sound import SoundUtil


class RemovalTurn(Turn):
    '''
    all the operation that happen during a removal turn
    '''
    def __init__(self, board: Board, player: Player, mill_checker: MillChecker):
        super().__init__(board, player, mill_checker)
        self.set_turn_type(TurnType.remove)

    def action(self, index: int):
        '''
        See Turn.action(index)
        '''
        if self._board.position_occupied(index) and self._board.get_position(index).get_piece() != self._player_of_this_turn.get_colour():
            # if the position has a piece and that piece is owned by the player of that turn
            self.set_selected_piece(index)
            # checks if all opponent pieces are in mills
            opponent_pieces_in_mills = []
            for piece_index in [position.get_index() for position in self._board.positions
                                if (position.get_piece() != self._player_of_this_turn.get_colour()
                                and position.get_piece() is not None)]:
                opponent_pieces_in_mills.append(self._mill_checker.check_if_in_mill(piece_index))

            # removes piece if not in mill
            if False in opponent_pieces_in_mills:
                if not self._mill_checker.check_if_in_mill(index):
                    return self._remove_piece_action()

            # removes any pieces as all opponent pieces are in mills
            else:
                return self._remove_piece_action()

        return False

    def _remove_piece_action(self) -> bool:
        '''
        do the piece removal on the board
        '''
        self._remove_piece(self.get_selected_piece())  # get rid of that piece
        print("removal", self._player_of_this_turn, self.get_selected_piece(), self.get_selected_empty())
        self.set_selected_piece(None)  # reset selected position
        SoundUtil.play_sound(SoundUtil, SoundID.piece)
        self._mill_checker.update_mills(self._board)
        return True  # signaling the end of the turn
