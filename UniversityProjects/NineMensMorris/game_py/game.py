from board import Board
from enum_player import PlayerColour
from player import Player
from turn import Turn
from enum_turn_type import TurnType
from mill_checker import MillChecker
from turn_fly import FlyTurn
from turn_move import MoveTurn
from turn_place import PlaceTurn
from turn_remove import RemovalTurn


class Game:
    """
    Initialises a game environment to play on.
    """

    def __init__(self):
        """
        Constructor called by GameManager class

        :board: Board object
        :game_result: boolean objects storing result of the match
        :current_player: Enum attribute showing what player's turn it is now (stored as int thou)
        :white_pieces_pile: List storing the pieces used for each player to place them during game start
        :black_pieces_pile: ''
        :black_phase:   current phase that that player is in
        :white_phase:   ''
        :turn: Turn object representing current turn
        :mill_checker: the MillChecker object for different mill detection happen in the game
        """
        self._board = Board()
        self._game_result = None
        self.player_white = Player(PlayerColour.white)
        self.player_black = Player(PlayerColour.black)
        self._current_player = self.player_white
        self._turn = None  # for storing the current turn, get replaced once there is a new turn
        self._mill_checker = MillChecker()
        self.set_turn(self.get_current_player(), TurnType.place)  # init the first turn for white

    """
    These are all setters and getters for this class' attributes.
    """
    def set_game_result(self, player: Player):
        self._game_result = player

    def get_game_result(self) -> Player:
        return self._game_result

    def set_current_player(self, player: Player):
        self._current_player = player

    def get_current_player(self) -> Player:
        return self._current_player

    def override_game(self, w_lst: list = [], b_lst: list = [], w_player: Player = Player(PlayerColour.white), b_player: Player = Player(PlayerColour.black)):
        self._board = Board()
        for index in w_lst:
            self._board.put_piece(index, PlayerColour.white)
        for index in b_lst:
            self._board.put_piece(index, PlayerColour.black)
        self.player_white = w_player
        self.player_black = b_player

    def get_board(self) -> Board:
        return self._board

    def get_turn(self) -> Turn:
        return self._turn

    def get_mill_checker(self) -> MillChecker:
        return self._mill_checker

    def set_turn(self, player: Player, turn_type: TurnType):
        """
        set the current turn determined by logic and game state

        :player: Player object
        :turn_type: TurnType enum
        """
        print(player, turn_type)
        if turn_type is TurnType.place:
            self._turn = PlaceTurn(self._board, player, self._mill_checker)
        elif turn_type is TurnType.move:
            self._turn = MoveTurn(self._board, player, self._mill_checker)
        elif turn_type is TurnType.fly:
            self._turn = FlyTurn(self._board, player, self._mill_checker)
        elif turn_type is TurnType.remove:
            self._turn = RemovalTurn(self._board, player, self._mill_checker)

    def _switch_phases(self, player: Player):
        """
        Switches phases/turns for the player depending on what their current board state and turn type is

        :player: Player object
        """
        if player.get_phase() == TurnType.place and len(player.get_pile()) == 0:
            player.set_phase(TurnType.move)
        if player.get_phase() == TurnType.move and len(
                [position.get_index() for position in self._board.positions if
                 (position.get_piece() == player.get_colour())]) == 3:
            player.set_phase(TurnType.fly)

    def _switch_player(self):
        """
        Switches current player and returns their phase/turn type

        :return: TurnType enum
        """
        if self.get_current_player().get_colour() == PlayerColour.white:
            self._current_player = self.player_black
        else:
            self._current_player = self.player_white
        return self.get_current_player().get_phase()

    def trigger(self, index: int):  # will run if the player clicked on the board positions
        """
        This method gets called whenever a user clicks on the board.
        Executes stored turn and calculates next turn

        index: index location of the piece to be moved/placed/deleted
        """
        turn_executed = self._turn.action(index) # perform the action of the loaded turn

        print(str(self.get_current_player()), "trigger", self._mill_checker.list_of_mills) # Background checking code

        # determine next turn when the turn does its actions
        if turn_executed:
            self._switch_phases(self.player_white)   # check switch phase for each player
            self._switch_phases(self.player_black)
            current_turn_type = self.get_turn().get_turn_type()
            # if current turn is either move or place,
            # check if we need to remove piece else set next turn to place or move
            if current_turn_type is not TurnType.remove:
                # Returns either TurnType.remove or TurnType.place
                next_move = self._mill_checker.decision_splitting(index, self._board)
                if next_move is not TurnType.remove:
                    next_turn_type = self._switch_player()
                else:  # Same player will be removing next turn
                    self.set_current_player(self.get_current_player())
                    next_turn_type = TurnType.remove
            else:
                next_turn_type = self._switch_player()

            self.set_turn(self.get_current_player(), next_turn_type)

        # ends the game if current player has lost and game phase is not place
        if self.get_turn().get_turn_type() != TurnType.place:
            if len(self.player_white.get_pile()) == 0 and len(self.player_black.get_pile()) == 0 \
                    and self._check_loss(self.get_current_player().get_colour()):
                # if this turn's player lost, the previous turn player wins
                if self.get_current_player().get_colour() == PlayerColour.white:
                    self.set_game_result(self.player_black)
                else:
                    self.set_game_result(self.player_white)
                print(str(self.get_game_result()) + " has won the game!")

    def _check_loss(self, current_player: PlayerColour):
        """
        check is the player of the current turn has lost the game
        """
        player_pieces = self._current_player.get_player_pieces_position(self._board)

        position_max_neighbour_count = {
            0: 2,
            1: 3,
            2: 2,
            3: 3,
            4: 3,
            5: 2,
            6: 3,
            7: 2,
            8: 2,
            9: 4,
            10: 2,
            11: 4,
            12: 4,
            13: 2,
            14: 4,
            15: 2,
            16: 2,
            17: 3,
            18: 2,
            19: 3,
            20: 3,
            21: 2,
            22: 3,
            23: 2
        }

        # should not make player lose in place phase
        if len(player_pieces) < 3:
            return True

        # player should be able to fly and therefor cannot lose
        elif len(player_pieces) == 3:
            return False

        elif len(player_pieces) > 3:
            for index in player_pieces:
                count = 0
                for neighbour in self.get_board().get_position(index).get_neighbours():
                    if self.get_board().get_position(neighbour).get_piece():
                        count += 1
                if count < position_max_neighbour_count.get(index):
                    return False

            # otherwise opponent is blocked
            return True


class GameManager:
    """
    makes a new instance of Game when there is none, as required.
    If others request a game it returns its instance, it make sure it give that one game only
    """

    def __init__(self):
        self._current_game = None
        self.get_game()

    def get_game(self):
        if self._current_game is None:
            self._current_game = Game()
        return self._current_game
