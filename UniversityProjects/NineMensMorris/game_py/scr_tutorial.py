import pygame

from enum_player import PlayerColour
from enum_screen_id import ScrIndex
from enum_turn_type import TurnType
from enum_sound import SoundID
from util_sound import SoundUtil
from player import Player
from scr_game import GameScr


class TutorialScr(GameScr):

    def __init__(self, screen, mouse):
        super().__init__(screen, mouse)

        self.total_page = 5     # page: 1 <= page <= total_page
        self.current_page = 1
        self._button_res = (50, 50)
        self._next_img = pygame.transform.scale(pygame.image.load("res/button/arrow_right.png"), self._button_res)
        self._down_img = pygame.transform.scale(pygame.image.load("res/down_arrow.png"), (205 * 0.3, 288 * 0.3))
        self.default_click_to_cord = [(398, 120), (642, 119), (882, 119), (398, 361), (881, 362), (399, 602), (641, 604),
                                 (882, 603), (472, 194), (642, 193), (806, 194), (474, 360), (808, 363), (473, 528),
                                 (640, 528), (806, 528), (549, 271), (642, 272), (732, 269), (548, 361), (733, 364),
                                 (548, 452), (639, 452), (731, 452)]
        self.p3 = False
        self.p4 = False
        self.p5 = False

    def page1(self):    # UI intro
        pygame.draw.rect(self._screen, self._grey, (940, 171, 340, 485))
        self._click_to_cord = [(-20, -20)] * 24 # player cannot interact with the board yet

        self._hint_state = True

        text = self._font.render('Your piece pile', True, self._yellow)
        text_rect = text.get_rect()
        text_rect.center = (182, 475)
        self._screen.blit(text, text_rect)

        text = self._font.render('<- Current Turn Indicator', True, self._yellow)
        text_rect = text.get_rect()
        text_rect.center = (954, 720)
        self._screen.blit(text, text_rect)

        text = self._font.render('Welcome to Nine Men\'s Morris.', True, self._white)
        self._screen.blit(text, (945, 175))
        text = self._font.render('In this guide, You will know:', True, self._white)
        self._screen.blit(text, (945, 200))
        text = self._font.render('1. UI introduction', True, self._white)
        self._screen.blit(text, (945, 225))
        text = self._font.render('2. Place Action', True, self._white)
        self._screen.blit(text, (945, 250))
        text = self._font.render('3. Move & Mill & Removal', True, self._white)
        self._screen.blit(text, (945, 275))
        text = self._font.render('4. Removing Mill Pieces', True, self._white)
        self._screen.blit(text, (945, 300))
        text = self._font.render('5. Move Phase', True, self._white)
        self._screen.blit(text, (945, 325))
        text = self._font.render('6. Fly Phase', True, self._white)
        self._screen.blit(text, (945, 350))

        text = self._font.render('The buttons are indicated with', True, self._white)
        self._screen.blit(text, (945, 400))
        text = self._font.render('words.', True, self._white)
        self._screen.blit(text, (945, 425))
        text = self._font.render('Those non-clickable elements', True, self._white)
        self._screen.blit(text, (945, 450))
        text = self._font.render('are indicated on this page with', True, self._white)
        self._screen.blit(text, (945, 475))
        text = self._font.render('yellow.', True, self._white)
        self._screen.blit(text, (945, 500))
        text = self._font.render('In the middle is the board, that', True, self._white)
        self._screen.blit(text, (945, 525))
        text = self._font.render('made with Lines and Dots.', True, self._white)
        self._screen.blit(text, (945, 550))

        self.next_button()

    def page2(self):    # page2 place interaction
        pygame.draw.rect(self._screen, self._grey, (940, 171, 340, 485))
        self._hint_state = True
        if self._game.get_current_player() == self._game.player_white:
            self._click_to_cord = self.default_click_to_cord

        text = self._font.render('Place Phase', True, self._white)
        self._screen.blit(text, (945, 175))

        text = self._font.render('Place pieces from your pile', True, self._white)
        self._screen.blit(text, (945, 225))
        text = self._font.render('until it ran out.', True, self._white)
        self._screen.blit(text, (945, 250))
        text = self._font.render('Try placing a piece on the', True, self._white)
        self._screen.blit(text, (945, 275))
        text = self._font.render('board. Click on any dots on', True, self._white)
        self._screen.blit(text, (945, 300))
        text = self._font.render('the board.', True, self._white)
        self._screen.blit(text, (945, 325))

        if self._game.get_current_player() != self._game.player_white:
            self._click_to_cord = [(-20, -20)] * 24
            text = self._font.render('You just placed a piece!', True, self._white)
            self._screen.blit(text, (945, 375))
            text = self._font.render('At the bottom, you can see the', True, self._white)
            self._screen.blit(text, (945, 400))
            text = self._font.render('turns has handover to another', True, self._white)
            self._screen.blit(text, (945, 425))
            text = self._font.render('player.', True, self._white)
            self._screen.blit(text, (945, 450))
            text = self._font.render('Next ->', True, self._white)
            self._screen.blit(text, (945, 500))
            self.next_button()
            self._click_to_cord = [(-10, -10)] * 24

    def page3(self):    # page3 Mill creation & remove (non mill pieces)
        pygame.draw.rect(self._screen, self._grey, (940, 171, 340, 485))
        if not self.p3:
            self._game.override_game([8, 9, 18, 3, 19, 18, 20], [1, 2, 4, 7, 10, 12, 16, 17, 23],
                                     Player(PlayerColour.white, 0), Player(PlayerColour.black, 0))
            self._game._mill_checker.update_mills(self._game.get_board())
            self._game.set_current_player(self._game.player_white)
            self._game.set_turn(self._game.player_white, TurnType.move)
            self._click_to_cord = [(-10, -10)] * 24
            self._click_to_cord[8] = self.default_click_to_cord[8]
            self._click_to_cord[11] = self.default_click_to_cord[11]
            self.p3 = True

        self._click_to_cord = [(-10, -10)] * 24
        self._click_to_cord[8] = self.default_click_to_cord[8]
        self._click_to_cord[11] = self.default_click_to_cord[11]
        text = self._font.render('Move & Mill & Removal', True, self._white)
        self._screen.blit(text, (945, 175))

        text = self._font.render('Mills are where 3 pieces of yours ', True, self._white)
        self._screen.blit(text, (945, 225))
        text = self._font.render('form a line, highlight in yellow', True, self._white)
        self._screen.blit(text, (945, 250))
        text = self._font.render('Once a mill is formed, you could', True, self._white)
        self._screen.blit(text, (945, 275))
        text = self._font.render('remove an opponent piece.', True, self._white)
        self._screen.blit(text, (945, 300))
        text = self._font.render('Try to move pieces following the', True, self._white)
        self._screen.blit(text, (945, 325))
        text = self._font.render('arrow.', True, self._white)
        self._screen.blit(text, (945, 350))
        text = self._font.render('In move phase, your could only', True, self._white)
        self._screen.blit(text, (945, 375))
        text = self._font.render('move by following the line.', True, self._white)
        self._screen.blit(text, (945, 400))


        if self._game.get_turn().get_turn_type() == TurnType.move and self._game.get_current_player().get_colour() == PlayerColour.white :
            self._screen.blit(self._down_img, (440, 240))
            text = self._font.render('Click on the piece you want ', True, self._white)
            self._screen.blit(text, (945, 425))
            text = self._font.render('to move, then click where you', True, self._white)
            self._screen.blit(text, (945, 450))
            text = self._font.render('want it to go.', True, self._white)
            self._screen.blit(text, (945, 475))

        if self._game.get_turn().get_turn_type() == TurnType.remove:
            self._click_to_cord = [(-20, -20)] * 24
            approved_lst = [1, 10, 16, 17, 12, 23]
            for i in approved_lst:
                self._click_to_cord[i] = self.default_click_to_cord[i]
            text = self._font.render('You just created a mill!', True, self._white)
            self._screen.blit(text, (945, 425))
            text = self._font.render('Now try remove a piece.', True, self._white)
            self._screen.blit(text, (945, 450))
            text = self._font.render('Click on the piece you want', True, self._white)
            self._screen.blit(text, (945, 475))
            text = self._font.render('to remove.', True, self._white)
            self._screen.blit(text, (945, 500))

        if self._game.get_current_player() != self._game.player_white:
            self._click_to_cord = [(-10, -10)] * 24

            text = self._font.render('You removed an opponent ', True, self._white)
            self._screen.blit(text, (945, 425))
            text = self._font.render('piece!', True, self._white)
            self._screen.blit(text, (945, 450))
            text = self._font.render('Your goal is to reduce opponent', True, self._white)
            self._screen.blit(text, (945, 475))
            text = self._font.render('pieces to 2', True, self._white)
            self._screen.blit(text, (945, 500))
            text = self._font.render('Next ->', True, self._white)
            self._screen.blit(text, (945, 525))
            self.next_button()


    def page4(self):    # page4 remove mill piece
        pygame.draw.rect(self._screen, self._grey, (940, 171, 340, 485))
        if not self.p4:
            self._hint_state = True
            self._game.override_game([0,3,5], [2,4,7],
                                     Player(PlayerColour.white, 5), Player(PlayerColour.black, 6))
            self._game._mill_checker.update_mills(self._game.get_board())
            self._game.set_current_player(self._game.player_white)
            self._game.set_turn(self._game.player_white, TurnType.remove)
            approved_lst = [2,4,7]
            for i in approved_lst:
                self._click_to_cord[i] = self.default_click_to_cord[i]
            self.p4 = True
        text = self._font.render('Removing Mill Piece', True, self._white)
        self._screen.blit(text, (945, 175))

        text = self._font.render('If there are piece not in a mill,', True, self._white)
        self._screen.blit(text, (945, 225))
        text = self._font.render('you could only remove them.', True, self._white)
        self._screen.blit(text, (945, 250))
        text = self._font.render('You could only remove a piece', True, self._white)
        self._screen.blit(text, (945, 275))
        text = self._font.render('within a mill is the only', True, self._white)
        self._screen.blit(text, (945, 300))
        text = self._font.render('remaining piece is in a mill.', True, self._white)
        self._screen.blit(text, (945, 325))
        text = self._font.render('Try remove one mill piece.', True, self._white)
        self._screen.blit(text, (945, 350))
        if self._game.get_current_player() != self._game.player_white:
            text = self._font.render('Next ->', True, self._white)
            self._screen.blit(text, (945, 500))
            self._click_to_cord = [(-10, -10)] * 24
            self.next_button()


    def page5(self):    # page5 fly
        pygame.draw.rect(self._screen, self._grey, (940, 171, 340, 485))
        if not self.p5:
            self._hint_state = True
            self._game.override_game([0, 5, 7], [1, 8, 10],
                                     Player(PlayerColour.white, 0), Player(PlayerColour.black, 0))
            self._game._mill_checker.update_mills(self._game.get_board())
            self._game.set_current_player(self._game.player_white)
            self._game.set_turn(self._game.player_white, TurnType.fly)
            self._click_to_cord = [(-10, -10)] * 24
            approved_lst = [7,3,1]
            for i in approved_lst:
                self._click_to_cord[i] = self.default_click_to_cord[i]
            self.p5 = True

        text = self._font.render('Fly Phase', True, self._white)
        self._screen.blit(text, (945, 175))

        text = self._font.render('When you only have 3 pieces ', True, self._white)
        self._screen.blit(text, (945, 225))
        text = self._font.render('left, your movement are no', True, self._white)
        self._screen.blit(text, (945, 250))
        text = self._font.render('longer limited by the line', True, self._white)
        self._screen.blit(text, (945, 275))
        text = self._font.render('Try make your opponent lose', True, self._white)
        self._screen.blit(text, (945, 300))
        text = self._font.render('within one turn.', True, self._white)
        self._screen.blit(text, (945, 325))
        text = self._font.render('You can turn hint on when ', True, self._white)
        self._screen.blit(text, (945, 375))
        text = self._font.render('you need some guidance.', True, self._white)
        self._screen.blit(text, (945, 400))




    def display(self):
        # overlay and switch pre define board

        result_option = super().display()
        if result_option is not None:
            return result_option

        if self._game.get_game_result() is None:
            if self.current_page == 1:
                self.page1()
            elif self.current_page == 2:
                self.page2()
            elif self.current_page == 3:
                self.page3()
            elif self.current_page == 4:
                self.page4()
            elif self.current_page == 5:
                self.page5()



        # back button
        if self._button((132 + 50, 100), self._button_res[0], self._back_img):
            return ScrIndex.menu

        page_indicator = str(self.current_page) + " / " + str(self.total_page)
        page_text = self._font.render(page_indicator, True, self._white)
        page_text_rect = page_text.get_rect()
        page_text_rect.center = (1102, 590)
        self._screen.blit(page_text, page_text_rect)

    def next_button(self) -> bool:
        if self._button((1102, 629), self._button_res[0], self._next_img):
            self.current_page = max(1, min(self.current_page + 1, self.total_page))
            return True
        return False

    def _result_overlay(self, dont_care):   # page 6 win condition and return
        # only play sound once
        if not self._ended:
            SoundUtil.play_sound(SoundUtil, SoundID.result)
            self._ended = True

        colour = (255, 255, 255)
        result_text = self._font.render('You Just win! Try think of strategies to win a battle with friends!', True, self._black)

        s = pygame.Surface((1280, 800))
        s.set_alpha(100)
        s.fill(colour)
        self._screen.blit(s, (0, 0))

        if self._button((1280 / 2, 800 / 1.9), self._button_res[0], self._back_img):
            return ScrIndex.menu

        result_text_rect = result_text.get_rect()
        result_text_rect.center = (1280 / 2, 800 / 2.5)
        self._screen.blit(result_text, result_text_rect)


