import pygame

class Music:
    def __init__(self):
        """
        Inicializa os componentes do mixer do Pygame.
        """
        pygame.mixer.init()

    #para a musica atual e inicia a musica de menu
    def play_music_menu(self):
        """
        Reproduz a música de fundo do menu principal.
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.load("../assets/menu_music.mp3")
        pygame.mixer.music.play(-1)

    #para a musica atual e inicia a musica de jogo
    def play_music_game(self):
         """
        Reproduz a música de fundo durante o jogo.
        """
        pygame.mixer.music.stop() 
        pygame.mixer.music.load("../assets/game_music.mp3")
        pygame.mixer.music.play(-1)
