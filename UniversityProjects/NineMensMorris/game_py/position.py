from enum_player import PlayerColour


class Position:
    """
    Position that represents the place of a node in the board network.
    Allows each position to know where other pieces on the board are relative to itself, its current state.
    """
    def __init__(self, location_index: int):
        """
        Constructor of position called by board to represent location

        :location_index: int representing it's location relative to the ring it is in
        :neighbours: list of position index that are neighbour to this position
        :position_types: list of position that exist on the lines intersection
        :piece: possible state that could happen on this position: None, Player.white, Player.black
        """
        self._location_index = location_index
        self._neighbours = []
        self._piece = None

    def get_index(self) -> int:
        return self._location_index

    def set_neighbours(self, lst: list):
        self._neighbours = lst

    def get_neighbours(self) -> list:
        return self._neighbours

    def set_piece(self, piece: PlayerColour):
        self._piece = piece

    def get_piece(self) -> PlayerColour:
        return self._piece

