from board import Board
from enum_turn_type import TurnType


class MillChecker:

    def __init__(self):
        self.list_of_mills = []

    """
    Mill checker needs to do a few things
    
    1 it needs to check if the piece is in a mill
    2 if the piece is in a mill, you cannot remove it
    3 if the piece is not in a mill, you can remove it
    4 add the piece to a list of mills if it is in a mill
    """

    # Only gets called if the current turn is place/move
    def decision_splitting(self, index, board):
        """
        decide should next turn be removal turn
        """
        self.update_mills(board)  # Re-add them back into the list
        if self.check_if_in_mill(index):  # If there is still a mill with this index, return remove turn
            print(self.list_of_mills, "decision split")
            return TurnType.remove
        else:
            return

    # Legacy Function here for just incase lol
    # def clean_mill_list(self, index):
    #     updated_list_of_mill = []
    #     for set_of_mills in self.list_of_mills:
    #         if index not in set_of_mills:
    #             updated_list_of_mill.append(set_of_mills)
    #     self.list_of_mills = updated_list_of_mill

    def check_if_in_mill(self, index):
        for mill in self.list_of_mills:
            if index in mill:
                return True
        return False

    # Legacy Function here for just incase lol
    # def calculate_mill(self, index, board: Board):
    #     mill_exists = False
    #     millLocations = [(0, 1, 2), (0, 3, 5), (5, 6, 7), (2, 4, 7), (8, 9, 10), (8, 11, 13), (13, 14, 15),
    #                      (10, 12, 15), (16, 17, 18), (16, 19, 21), (21, 22, 23), (18, 20, 23), (3, 11, 19), (20, 12, 4),
    #                      (1, 9, 17), (22, 14, 6)]
    #
    #     for mill in millLocations:
    #         if index in mill:
    #             temp_list = []
    #             for x in mill:
    #                 temp_list.append(board.get_position(x).get_piece())
    #             if None not in temp_list:
    #                 if board.get_position(mill[0]).get_piece() == board.get_position(mill[1]).get_piece() == board.get_position(mill[2]).get_piece():
    #                     self.list_of_mills.append(mill)
    #                     mill_exists = True
    #     return mill_exists

    def update_mills(self, board: Board):
        '''
        update mills location
        '''
        self.list_of_mills = []
        mill_locations = [(0, 1, 2), (0, 3, 5), (5, 6, 7), (2, 4, 7), (8, 9, 10), (8, 11, 13), (13, 14, 15),
                          (10, 12, 15), (16, 17, 18), (16, 19, 21), (21, 22, 23), (18, 20, 23), (3, 11, 19),
                          (20, 12, 4),
                          (1, 9, 17), (22, 14, 6)]

        for mill in mill_locations:
            first_piece = board.get_position(mill[0]).get_piece()
            second_piece = board.get_position(mill[1]).get_piece()
            third_piece = board.get_position(mill[2]).get_piece()

            if first_piece == second_piece == third_piece is not None:
                self.list_of_mills.append(mill)

    """
    Mill checker is always called
    
    Decision_splitting decides what should happen
    
    It will check if the position creates a mill. If yes, it returns a value indicating the next turn should be a delete turn (same player will delete a piece)
    If no, it returns a value indicating the next turn should be a place turn (enemy gets to place a piece). 
    """
