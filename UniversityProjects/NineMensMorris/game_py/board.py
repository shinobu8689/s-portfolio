from position import Position
from enum_player import PlayerColour


class Board:
    """
    This class 'Board' contains all 'Position' positions which can have different states (i.e. piece) as well as initialises the relationship between positions.
    It contains the methods to place and remove pieces, as well as get pieces from positions (None if they there isn't one in a position).
    """

    def __init__(self):
        """
        Constructor called by game.py

        :positions: list holding the position objects that link to each other
        """
        self.positions = []

        for location in range(24):  # 0 - 23
            self.positions.append(Position(location))

        """
        Representation of the board
        0-------------------1--------------------2
        |                   |                    |
        |                   |                    |
        |       8-----------9-----------10       |
        |       |           |            |       |
        |       |           |            |       |
        |       |      16---17---18      |       |
        |       |      |          |      |       |
        3-------11-----19        20-----12-------4
        |       |      |          |      |       |
        |       |      21---22---23      |       |
        |       |           |            |       |
        |       |           |            |       |
        |       13----------14----------15       |
        |                   |                    |
        |                   |                    |
        5-------------------6--------------------7
        """

        # setup the board network
        self.positions[0].set_neighbours([1, 3])
        self.positions[1].set_neighbours([0, 2, 9])
        self.positions[2].set_neighbours([1, 4])
        self.positions[3].set_neighbours([0, 11, 5])
        self.positions[4].set_neighbours([12, 2, 7])
        self.positions[5].set_neighbours([3, 6])
        self.positions[6].set_neighbours([5, 14, 7])
        self.positions[7].set_neighbours([6, 4])
        self.positions[8].set_neighbours([9, 11])
        self.positions[9].set_neighbours([8, 1, 10, 17])
        self.positions[10].set_neighbours([9, 12])
        self.positions[11].set_neighbours([3, 8, 19, 13])
        self.positions[12].set_neighbours([20, 10, 4, 15])
        self.positions[13].set_neighbours([11, 14])
        self.positions[14].set_neighbours([13, 22, 15, 6])
        self.positions[15].set_neighbours([14, 12])
        self.positions[16].set_neighbours([17, 19])
        self.positions[17].set_neighbours([16, 9, 18])
        self.positions[18].set_neighbours([17, 20])
        self.positions[19].set_neighbours([11, 16, 21])
        self.positions[20].set_neighbours([18, 12, 23])
        self.positions[21].set_neighbours([19, 22])
        self.positions[22].set_neighbours([21, 23, 14])
        self.positions[23].set_neighbours([22, 20])

    def put_piece(self, index: int, piece: PlayerColour):
        '''
        apply the put action to the position
        '''
        self.positions[index].set_piece(piece)

    def remove_piece(self, index: int) -> PlayerColour:
        '''
        apply the remove action to the position
        '''
        previous_piece = self.positions[index].get_piece()
        self.positions[index].set_piece(None)
        return previous_piece

    def get_position(self, index: int) -> Position:
        return self.positions[index]

    def position_occupied(self, index: int) -> bool:
        return self.positions[index].get_piece() is not None
