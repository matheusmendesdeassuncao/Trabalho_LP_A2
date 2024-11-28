import pygame

class Music: 
    def __init__(self):
        pygame.mixer.init()

    def play_music(self):
        pygame.mixer.music.load("../assets/music.mp3")
        pygame.mixer.music.play(-1)  # -1 para repetir a música indefinidamente
