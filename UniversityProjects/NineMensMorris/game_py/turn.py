from abc import abstractmethod, ABC
from board import Board
from enum_player import PlayerColour
from enum_turn_type import TurnType
from mill_checker import MillChecker
from player import Player


class Turn(ABC):
    """
    This class handles the turn determined by Game class and perform actions chosen by the player.
    Player made actions to the board via turn.
    """

    def __init__(self, board: Board, player: Player, mill_checker: MillChecker):
        """
        Constructor used by game.py to generate new turn

        :_board: Board object, created and passed through game.py
        :_player_of_this_turn: Player, who is playing this turn
        :_selected_piece: int coord representing location of selected piece on grid/screen
        :_selected_empty: int coord representing location of empty node point
        :_turn_type: which action will is performing this turn and enable the logic
        :_mill_checker: required to check is there any mill existing on the board to limit player moves
        """
        self._board = board
        self._player_of_this_turn = player
        self._selected_piece = None
        self._selected_empty = None
        self._turn_type = None
        self._mill_checker = mill_checker

    def set_turn_type(self, turn_type: TurnType):
        self._turn_type = turn_type

    def get_turn_type(self) -> TurnType:
        return self._turn_type

    def set_selected_piece(self, index: int):
        '''
        store where the player selected a position with a piece
        '''
        self._selected_piece = index

    def get_selected_piece(self) -> int:
        return self._selected_piece

    def get_player_of_the_turn(self) -> Player:
        return self._player_of_this_turn

    def set_selected_empty(self, index: int):
        '''
        store where the player selected a position without a piece
        '''
        self._selected_empty = index

    def get_selected_empty(self) -> int:
        return self._selected_empty

    @abstractmethod
    def action(self, index: int) -> bool:
        """
        the action on the board
        :param index: passed from game.trigger() where it is representing the position it clicked on the board
        :return: return to game, signifying is the action successfully executed
        """
        pass

    def _put_piece(self, index: int, piece: PlayerColour):
        self._board.put_piece(index, piece)

    def _remove_piece(self, index: int) -> PlayerColour:
        return self._board.remove_piece(index)
