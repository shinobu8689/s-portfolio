import pygame
from sys import exit

from scr_tutorial import TutorialScr
from scene import Scene
from scr_game import GameScr
from scr_menu import MenuScr
from enum_screen_id import ScrIndex


class Display:      
    """
    Display Engine: receives user input and updates the UI (scene) as required (using pygame).
    Note: the game is currently hardcoded at a resolution of 1280 x 800.
    """

    def __init__(self, scr_res: (int, int)):
        """
        Constructor called by this file (for now)

        :scr_res: Tuple containing screen dimensions
        
        :scene: Game screen object
        :scr_res: resolution of the screen
        :screen: display object from Pygame library
        :mouse: mouse object from Pygame library
        """
        self._scene = None
        self._scr_res = scr_res
        self._screen = pygame.display.set_mode(self._scr_res)
        self._mouse = pygame.mouse
        pygame.init()
        pygame.display.set_caption("Nine Men's Morris")

    def set_scene(self, scene: Scene):
        self._scene = scene

    def run(self):
        """
        run the scene current set to, when that scene return a value, it switch to correspondence scene according to the ScreenID
        """
        clock = pygame.time.Clock()
        self.set_scene(MenuScr(self._screen, self._mouse))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            next = self._scene.display()
            if next is not None:
                if next == ScrIndex.menu:
                    self.set_scene(MenuScr(self._screen, self._mouse))
                if next == ScrIndex.game:
                    self.set_scene(GameScr(self._screen, self._mouse))
                if next == ScrIndex.tutorial:
                    self.set_scene(TutorialScr(self._screen, self._mouse))
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    display = Display((1280, 800))
    display.run()

