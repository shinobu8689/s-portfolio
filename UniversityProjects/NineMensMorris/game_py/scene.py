import pygame

from enum_sound import SoundID
from util_sound import SoundUtil


class Scene:

    """
    Parent class for game_scr. Provides access to all universal UI resources
    """
    
    # basic colour palette
    _white = (255, 255, 255)
    _l_grey = (200, 200, 200)
    _grey = (150, 150, 150)
    _black = (0, 0, 0)
    _red = (255, 0, 0)
    _green = (0, 200, 0)
    _blue = (0, 0, 255)
    _yellow = (200, 200, 0)

    pygame.font.init()
    _font = pygame.font.SysFont('sans bold', 32)



    def __init__(self, screen, mouse):
        """
        Constructor for Scene class.
        Different type of child class will be load into display as the current page

        :screen: pygame.display object with mode set to dimensions specified in display.py
        :mouse: pygame.mouse object

        :past_press: Boolean checking if the mouse is being held down (pygame.mouse.get_pressed()[0])
        :background: transformed image from pygame library
        """
        self._screen = screen
        self._mouse = mouse
        self.past_press = False
        self._background = pygame.transform.scale(pygame.image.load("res/background/wood_background.png"), (1280, 800))
        self._sound_img = pygame.transform.scale(pygame.image.load('res/button/sound.png'), (35, 35))

    def display(self):
        pass

    def _in_rect(self, mouse_pos: (int, int), xy: (int, int), wh: (int, int)):
        '''
        if the mouse pointer over the area
        '''
        return mouse_pos[0] > xy[0] and mouse_pos[0] < xy[0] + wh[0] and mouse_pos[1] > xy[1] and mouse_pos[1] < xy[1] + wh[1]

    def _button(self, location, rad, pic):  #pic res (50, 50)
        '''
        button template to put button all over the palce
        '''

        # hover colour change
        if self._in_rect(self._mouse.get_pos(), (location[0] - rad / 2, location[1] - rad / 2), (rad, rad)):
            colour = self._l_grey
        else:
            colour = self._grey
        pygame.draw.circle(self._screen, colour, location, rad / 2)
        self._screen.blit(pic, (location[0] - rad / 2, location[1] - rad / 2))

        # play sound when clicked
        # past_pressed fucked
        if self._mouse.get_pressed()[0] and self._in_rect(self._mouse.get_pos(), (location[0] - rad / 2, location[1] - rad / 2), (rad, rad)):
            SoundUtil.play_sound(SoundUtil, SoundID.button)
            return True
        return False

    def _toggle(self, location, rad, pic, state: bool): #pic res (35, 35)
        if state:
            colour = self._green
            nob = (location[0] + rad, location[1])
        else:
            colour = self._grey
            nob = location
        pygame.draw.circle(self._screen, colour, location, rad / 2)
        pygame.draw.circle(self._screen, colour, (location[0] + rad, location[1]), rad / 2)
        pygame.draw.rect(self._screen, colour, (location[0], location[1] - rad/2, rad, rad))
        # white inner circle
        pygame.draw.circle(self._screen, self._white, nob, rad / 2.5)
        self._screen.blit(pic, (nob[0] - 35 / 2, nob[1] - 35 / 2))

        # play sound when clicked
        if self._mouse.get_pressed()[0] and self._in_rect(self._mouse.get_pos(),
                                                          (location[0] - rad / 2, location[1] - rad / 2),
                                                          (rad*2, rad)) and not self.past_press:
            SoundUtil.play_sound(SoundUtil, SoundID.button)
            return True
        return False

    def sound_toggle(self):
        if self._toggle((50, 750), 50, self._sound_img, SoundUtil.enable_sound) and not self.past_press:
            SoundUtil.toggle(SoundUtil)
        sd = self._font.render('Sound', True, self._white)
        sd_rect = sd.get_rect()
        sd_rect.center = (175, 750)
        self._screen.blit(sd, sd_rect)





