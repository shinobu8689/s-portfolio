import pygame

from scene import Scene
from enum_screen_id import ScrIndex



class MenuScr(Scene):
    '''
    resources for the Menu screen and button behaviour
    '''

    def __init__(self, screen, mouse):
        super().__init__(screen, mouse)
        self._icon_res = (200, 200)
        self._game_img = pygame.transform.scale(pygame.image.load('res/menu_icons/2_player.png'), self._icon_res)
        self._book_img = pygame.transform.scale(pygame.image.load('res/menu_icons/tuto_book.png'), self._icon_res)
        self._title_img = pygame.transform.scale(pygame.image.load('res/title.png'), (1152 * 0.5, 510 * 0.5))


    def display(self):
        # fixed element
        self._screen.blit(self._background, (0, 0))
        self._screen.blit(self._title_img, (1280 / 5+ 90, 800 / 7))

        # gae button
        if self._button((1280 / 3, 500), self._icon_res[0], self._game_img):
            return ScrIndex.game
        to_game = self._font.render('VS Game', True, self._white)
        to_game_rect = to_game.get_rect()
        to_game_rect.center = (1280 / 3, 650)
        self._screen.blit(to_game, to_game_rect)

        # tutorial button
        if self._button((1280 / 3 * 2, 500), self._icon_res[0], self._book_img):
            return ScrIndex.tutorial
        tuto = self._font.render('Tutorial', True, self._white)
        tuto_rect = tuto.get_rect()
        tuto_rect.center = (1280 / 3 * 2, 650)
        self._screen.blit(tuto, tuto_rect)

        self.sound_toggle()

        self.past_press = self._mouse.get_pressed()[0]  # check not holding the mouse button
