import pygame
from pygame import mixer


class MusicSystem:

    munch_sound_state = 1
    IsPowerPillMusicPlaying = False
    IsSirenMusicPlaying = False
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
        if MusicSystem.IsSirenMusicPlaying == False:
            mixer.music.load(f'Music/siren_{siren_variant}.wav')
            mixer.music.play(-1)
            MusicSystem.IsSirenMusicPlaying = True
            MusicSystem.IsPowerPillMusicPlaying = False

    @staticmethod
    def playPowerPillMusic():

        if MusicSystem.IsPowerPillMusicPlaying == False:
            mixer.music.load(f'Music/power_pill.wav')
            mixer.music.play(-1)
            MusicSystem.IsSirenMusicPlaying = False
            MusicSystem.IsPowerPillMusicPlaying = True


    @staticmethod
    def playPacmanDeathSound():
        MusicSystem.IsSirenMusicPlaying = False
        MusicSystem.IsPowerPillMusicPlaying = False
        death_sound = mixer.Sound('Music/pacman_death.wav')
        death_sound.play()

    @staticmethod
    def stopPlayingMusic():
        MusicSystem.IsSirenMusicPlaying = False
        MusicSystem.IsPowerPillMusicPlaying = False
        mixer.music.stop()
        