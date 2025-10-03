import time

import pygame

from enum_sound import SoundID
from enum_turn_type import TurnType
from scene import Scene
from game import GameManager
from enum_player import PlayerColour
from enum_screen_id import ScrIndex
from util_sound import SoundUtil


class GameScr(Scene):
    """
    Loads assets and draws them on the users actual screen as required.
    """

    def __init__(self, screen, mouse):
        """
        Constructor called by display.py
        
        :screen: pygame.display object
        :mouse: pygame.mouse object

        :game_creator: GameManager instance
        :game: Game object created by GameManager
        """
        super().__init__(screen, mouse)

        # game resources
        self._button_res = (50, 50)
        self._board_res = (600, 600)
        self._piece_rad = 30
        self._highlight_rad = self._piece_rad + 5
        self._player_icon_res = (100, 100)
        self._next_p_arrow_res = (48, 48)
        self._click_rect = (68, 68)
        self._pile_piece_res = (80, 46)
        self._display_to_cord = [(398, 120), (642, 119), (882, 119), (398, 361), (881, 362), (399, 602), (641, 604),
                                 (882, 603), (472, 194), (642, 193), (806, 194), (474, 360), (808, 363), (473, 528),
                                 (640, 528), (806, 528), (549, 271), (642, 272), (732, 269), (548, 361), (733, 364),
                                 (548, 452), (639, 452), (731, 452)]
        self._click_to_cord = [(398, 120), (642, 119), (882, 119), (398, 361), (881, 362), (399, 602), (641, 604),
                                 (882, 603), (472, 194), (642, 193), (806, 194), (474, 360), (808, 363), (473, 528),
                                 (640, 528), (806, 528), (549, 271), (642, 272), (732, 269), (548, 361), (733, 364),
                                 (548, 452), (639, 452), (731, 452)]

        self._game_board_img = pygame.transform.scale(pygame.image.load('res/board/board.png'), self._board_res)
        self._player_w_img = pygame.transform.scale(pygame.image.load('res/player_heads/player_w.png'),
                                                    self._player_icon_res)
        self._player_b_img = pygame.transform.scale(pygame.image.load('res/player_heads/player_b.png'),
                                                    self._player_icon_res)
        self._pw_arrow_img = pygame.transform.scale(pygame.image.load("res/player_arrow/player_left.png"),
                                                    self._next_p_arrow_res)
        self._pb_arrow_img = pygame.transform.scale(pygame.image.load("res/player_arrow/player_right.png"),
                                                    self._next_p_arrow_res)
        self._piece_b_img = pygame.transform.scale(pygame.image.load("res/piece_b.png"), self._pile_piece_res)
        self._piece_w_img = pygame.transform.scale(pygame.image.load("res/piece_w.png"), self._pile_piece_res)
        self._back_img = pygame.transform.scale(pygame.image.load("res/button/arrow_left.png"), self._button_res)
        self._hint_img = pygame.transform.scale(pygame.image.load("res/button/hint.png"), (35, 35))
        self._play_again_img = pygame.transform.scale((pygame.image.load("res/button/play_again.png")),
                                                      self._button_res)

        self._game_creator = GameManager()
        self._game = self._game_creator.get_game()
        time.sleep(0.5)  # avoid holding the button longer than a tick that put a new piece
        SoundUtil.play_sound(SoundUtil, SoundID.start)
        self._ended = False  # for has the result overlay already displayed or not
        self._hint_state = False

    def display(self):
        # fixed element
        self._screen.blit(self._background, (0, 0))
        self._screen.blit(self._game_board_img, (340, 60))
        self._screen.blit(self._player_w_img, (132, 500))
        self._screen.blit(self._player_b_img, (1047, 500))

        if not self._game.get_turn().get_turn_type() == TurnType.remove:
            # next player indicator
            if self._game.get_current_player().get_colour() == PlayerColour.white:
                self._screen.blit(self._pw_arrow_img, (365 + 60, 703.5))
                self._screen.blit(self._player_w_img, (530, 675))
            else:
                self._screen.blit(self._pb_arrow_img, (867 - 60, 703.5))
                self._screen.blit(self._player_b_img, (530, 675))
            text = self._font.render('\'s turn', True, self._white)
            text_rect = text.get_rect()
            text_rect.center = (685, 730)
            self._screen.blit(text, text_rect)
        else:  # if removal turn
            # remove piece indicator
            text = self._font.render('Remove one', True, self._white)
            text_rect = text.get_rect()
            text_rect.center = (685 - 30, 730)
            self._screen.blit(text, text_rect)
            if self._game.get_current_player().get_colour() is PlayerColour.white:
                self._screen.blit(self._player_w_img, (475 - 30, 675))
                pygame.draw.circle(self._screen, self._white, (835 - 30, 730), 35)
                pygame.draw.circle(self._screen, self._black, (835 - 30, 730), 30)
            else:
                self._screen.blit(self._player_b_img, (475 - 30, 675))
                pygame.draw.circle(self._screen, self._black, (835 - 30, 730), 35)
                pygame.draw.circle(self._screen, self._white, (835 - 30, 730), 30)

        # pile amount display
        pygame.draw.rect(self._screen, self._red, (142 - 15, 235, 110, 225))
        for i in range(len(self._game.player_white.get_pile())):
            self._screen.blit(self._piece_w_img, (142, 400 - i * 18))

        pygame.draw.rect(self._screen, self._red, (1057 - 15, 235, 110, 225))
        for i in range(len(self._game.player_black.get_pile())):
            self._screen.blit(self._piece_b_img, (1057, 400 - i * 18))

        # registering click of the intersections
        if self._mouse.get_pressed()[0] and self._game.get_game_result() is None:
            index = self._get_clicked_board_position()
            if index is not None:  # it clicked sth
                self._game.trigger(index)

        if self._hint_state:
            self._hint_highlight()
        self._print_mills()
        self._print_pieces()


        # back button
        if self._button((132 + 50, 100), self._button_res[0], self._back_img):
            return ScrIndex.menu
        back_text = self._font.render('Back', True, self._white)
        back_text_rect = back_text.get_rect()
        back_text_rect.center = (180, 147)
        self._screen.blit(back_text, back_text_rect)


        # hint button
        if self._toggle((1047+25, 100), self._button_res[0], self._hint_img, self._hint_state):
            if self._hint_state:
                self._hint_state = False
            else:
                self._hint_state = True
        hint_text = self._font.render('Hint', True, self._white)
        hint_text_rect = hint_text.get_rect()
        hint_text_rect.center = (1094, 151)
        self._screen.blit(hint_text, hint_text_rect)



        self.sound_toggle()

        # result overlay
        result_option = None
        if self._game.get_game_result() is not None:
            result_option = self._result_overlay(self._game.get_game_result().get_colour())
        if result_option is not None:
            return result_option

        self.past_press = self._mouse.get_pressed()[0]  # check not holding the mouse button

    def _print_pieces(self):  # scan through game.board.positions and print pieces

        for i in range(len(self._display_to_cord)):
            # pygame.draw.rect(scr, self.red, (self.display_to_cord[i][0] - self.click_rect[0]/2, self.display_to_cord[i][1] - self.click_rect[1]/2, self.click_rect[0], self.click_rect[1]))
            if i == self._game.get_turn().get_selected_piece() and self._game.get_board().position_occupied(
                    i) and not self._game.get_turn().get_turn_type() == TurnType.remove:
                pygame.draw.circle(self._screen, self._green, self._display_to_cord[i], self._highlight_rad)
            if self._game.get_board().get_position(i).get_piece() == PlayerColour.white:
                pygame.draw.circle(self._screen, self._white, self._display_to_cord[i], self._piece_rad)
            elif self._game.get_board().get_position(i).get_piece() == PlayerColour.black:
                pygame.draw.circle(self._screen, self._black, self._display_to_cord[i], self._piece_rad)

    def _print_mills(self):
        for mill in self._game.get_mill_checker().list_of_mills:
            pygame.draw.line(self._screen, self._yellow, self._display_to_cord[mill[0]], self._display_to_cord[mill[1]],
                             10)
            pygame.draw.line(self._screen, self._yellow, self._display_to_cord[mill[1]], self._display_to_cord[mill[2]],
                             10)
            pygame.draw.circle(self._screen, self._yellow, self._display_to_cord[mill[0]],
                               self._highlight_rad)  # circle
            pygame.draw.circle(self._screen, self._yellow, self._display_to_cord[mill[1]], self._highlight_rad)
            pygame.draw.circle(self._screen, self._yellow, self._display_to_cord[mill[2]], self._highlight_rad)

    def _get_clicked_board_position(self) -> int:
        for i in range(len(self._click_to_cord)):
            if self._in_rect(self._mouse.get_pos(), (
                    self._click_to_cord[i][0] - self._click_rect[0] / 2,
                    self._click_to_cord[i][1] - self._click_rect[1] / 2),
                             self._click_rect) and not self.past_press:  # if clicked on any piece registering area
                return i
        return None

    def _hint_highlight(self):
        if self._game.get_turn().get_turn_type() == TurnType.move:
            if self._game.get_turn().get_selected_piece() is not None:
                for index in self._game.get_board().get_position(
                        self._game.get_turn().get_selected_piece()).get_neighbours():
                    if not self._game.get_board().position_occupied(index):
                        pygame.draw.circle(self._screen, self._green, self._display_to_cord[index], 5)  # circle
        elif self._game.get_turn().get_turn_type() == TurnType.fly:
            for index in range(24):
                if not self._game.get_board().position_occupied(index) and self._game.get_turn().get_selected_piece() is not None:
                    pygame.draw.circle(self._screen, self._green, self._display_to_cord[index], 5)  # circle
        elif self._game.get_turn().get_turn_type() == TurnType.remove:
            for index in range(24):
                if self._game.get_board().get_position(index).get_piece() != self._game.get_current_player().get_colour() and self._game.get_board().get_position(index).get_piece() is not None:
                    pygame.draw.circle(self._screen, self._red, self._display_to_cord[index], self._highlight_rad)

    def _result_overlay(self, winner):

        # only play sound once
        if not self._ended:
            SoundUtil.play_sound(SoundUtil, SoundID.result)
            self._ended = True

        if winner == PlayerColour.white:
            colour = (255, 255, 255)
            result_text = self._font.render('White wins!', True, self._black)
        elif winner == PlayerColour.black:
            colour = (0, 0, 0)
            result_text = self._font.render('Black wins!', True, self._white)
        elif winner == PlayerColour.draw:  # draw
            colour = (128, 128, 128)
            result_text = self._font.render('Draw!', True, self._white)

        s = pygame.Surface((1280, 800))
        s.set_alpha(100)
        s.fill(colour)
        self._screen.blit(s, (0, 0))

        if self._button((1280 / 2.3 - 10, 800 / 1.9), self._button_res[0], self._back_img):
            return ScrIndex.menu
        if self._button((1280 / 1.7 - 20, 800 / 1.9), self._button_res[0],
                        self._play_again_img) and not self.past_press:
            return ScrIndex.game

        result_text_rect = result_text.get_rect()
        result_text_rect.center = (1280 / 2, 800 / 2.5)
        self._screen.blit(result_text, result_text_rect)
