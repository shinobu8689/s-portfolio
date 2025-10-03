import pygame

from enum_sound import SoundID


class SoundUtil:
    '''
    SoundUtil for any part of the program to play sounds.
    All sound activation code is gathered here.
    '''
    pygame.mixer.init()
    enable_sound = True

    def play_sound(self, sd_type: SoundID):
        '''
        Play correspondent sound among the sound resources with SoundID
        '''
        if self.enable_sound:   # Play if sounds are enabled
            if sd_type is SoundID.button:
                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/button.mp3'))
            elif sd_type is SoundID.piece:
                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/piece.mp3'))
            elif sd_type is SoundID.result:
                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/result.mp3'))
            elif sd_type is SoundID.start:
                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/start.mp3'))
            elif sd_type is SoundID.invalid:
                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/invalid.mp3'))

    def get_enable_sound(self) -> bool:
        '''
        getter for self.enable_sound
        '''
        return self.enable_sound

    def toggle(self):
        '''
        toggle self.enable_sound state
        '''
        if self.enable_sound:
            self.enable_sound = False
        else:
            self.enable_sound = True