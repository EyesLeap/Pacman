import pygame
from pygame import mixer

class MusicSystem:

    #siren_sound1 = mixer.music.load('Music/siren_1.wav')
    #siren_sound2 = mixer.music.load('Music/siren_2.wav')
    #siren_sound3 = mixer.music.load('Music/siren_3.wav')
    #siren_sound4 = mixer.music.load('Music/siren_4.wav')
    #siren_sound5 = mixer.music.load('Music/siren_5.wav')

    #munch_sound1 = mixer.music.load('Music/munch_1.wav')
    #munch_sound2 = mixer.music.load('Music/munch_2.wav')

    def __init__(self):
        pass
    @staticmethod
    def playBeginningSound():
        beginning_sound = mixer.Sound('Music/pacman_beginning.wav')
        beginning_sound.play()