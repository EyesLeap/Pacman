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

    munch_sound_state = 1
    def __init__(self):
        pass
    @staticmethod
    def playBeginningSound():
        beginning_sound = mixer.Sound('Music/pacman_beginning.wav')
        beginning_sound.play()

    @staticmethod
    def playMunchSound():

        if MusicSystem.munch_sound_state == 1:
            munch_sound = mixer.Sound('Music/munch_1.wav')
            munch_sound.play()
            MusicSystem.munch_sound_state = 2

        elif MusicSystem.munch_sound_state == 2:
            munch_sound = mixer.Sound('Music/munch_2.wav')
            munch_sound.play()
            MusicSystem.munch_sound_state = 1

    @staticmethod
    def playSirenMusic(siren_variant):
        siren_music = mixer.music.load(f'Music/siren_{siren_variant}.wav')
        mixer.music.play(-1)
        