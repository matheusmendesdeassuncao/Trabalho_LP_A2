import pygame
from utils import *

class Button:
    def __init__(self, x, y, width, height, text='', font_size=30, color=(255,215,0), text_color=(0,0,0), selected_color=(238,173,45)):
        """
        Inicializa um novo botão com as propriedades especificadas.

        Args:
            x (int): A posição horizontal do botão.
            y (int): A posição vertical do botão.
            width (int): A largura do botão.
            height (int): A altura do botão.
            text (str, opcional): O texto exibido no botão. O valor padrão é uma string vazia.
            font_size (int, opcional): O tamanho da fonte do texto. O valor padrão é 30.
            color (tuple, opcional): A cor de fundo do botão, no formato RGB. O valor padrão é (255, 215, 0).
            text_color (tuple, opcional): A cor do texto, no formato RGB. O valor padrão é (0, 0, 0).
            selected_color (tuple, opcional): A cor do botão quando selecionado, no formato RGB. O valor padrão é (238, 173, 45).
        """
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color 
        self.selected_color = selected_color
        self.text = text
        self.text_color= text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_selected = False

    def draw(self, screen):
        """
        Desenha o botão na tela, alterando sua cor se estiver selecionado.

        Args:
            screen (pygame.Surface): A superfície onde o botão será desenhado.
        """
        #altera a cor do botao enquanto ele esta selecionado
        self.is_selected = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.is_selected: 
            pygame.draw.rect(screen, self.selected_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        #cria as caracteristicas do texto
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
    
    #verifica se o botao foi clicado
    def is_clicked(self, event):
        """
        Verifica se o botão foi clicado.

        Args:
            event (pygame.event.Event): O evento capturado pelo Pygame, geralmente um evento de clique do mouse.

        Returns:
            bool: Retorna True se o botão foi clicado, caso contrário, retorna False.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return False
    
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
        pygame.mixer.music.load("./assets/songs/menu_music.mp3")
        pygame.mixer.music.play(-1)

    #para a musica atual e inicia a musica de jogo
    def play_music_game(self):
        """
        Reproduz a música de fundo durante o jogo.
        """
        pygame.mixer.music.stop() 
        pygame.mixer.music.load("./assets/songs/game_music.mp3")
        pygame.mixer.music.play(-1)

class Display:
    def __init__(self, screen):
        """
        Inicializa os atributos principais do jogo e configura as telas iniciais.

        Args:
            screen (pygame.Surface): A superfície principal onde os elementos do jogo serão renderizados.
        """
        self.screen = screen
        self.active_screen = "menu"
        self.music = Music()

        self.init_menu()
        self.init_credits()

    def init_menu(self):
        """
        Inicializa os elementos do menu principal.
        """
        #carrega a imagem e ajusta o tamanho

        self.menu_background = load_image(IMAGE_PATH, 'background/background_menu.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        #pygame.image.load("../assets/background/background_menu.png")
        self.menu_background = pygame.transform.scale(self.menu_background, (self.screen.get_width(), self.screen.get_height()))
        
        #inicializa os botões do menu
        self.menu_buttons = {
            "play": Button(300, 250, 200, 50, text="Play"),
            "credits": Button(300, 350, 200, 50, text="Credits"),
            "quit": Button(300, 450, 200, 50, text="Quit")
        }

        self.music.play_music_menu()

    #inicializa elementos da tela credits
    def init_credits(self):
        """
        Inicializa os elementos da tela de creditos.
        """
        #carrega a imagem e ajusta o tamanho
        self.credits_background = load_image(IMAGE_PATH, 'background/background_menu.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        #pygame.image.load("../assets/background/background_credits.png")
        self.credits_background = pygame.transform.scale(self.credits_background, (self.screen.get_width(), self.screen.get_height()))
        
        #inicializa os botões de credits
        self.credits_buttons = {
            "back": Button(30, 530, 200, 50, text="Back")
        }

    #desenha a tela menu
    def menu_screen(self):
        """
        Renderiza a tela do menu principal.
        """
        self.screen.blit(self.menu_background, (0, 0))
        for button in self.menu_buttons.values():
            button.draw(self.screen)
    
    #desenha a tela credits
    def credits_screen(self):
        """
        Renderiza a tela de creditos.
        """
        self.screen.blit(self.credits_background, (0, 0))

        #inicialize a fonte
        font_large = pygame.font.Font(None, 100)  #título
        font_medium = pygame.font.Font(None, 40)  #nomes

        #renderiza os textos
        title = font_large.render("CREDITS", True, (0, 0, 0))
        names = [
            font_medium.render("GABRIELA BARBOSA", True, (0, 0, 0)),
            font_medium.render("HELORA KELLY", True, (0, 0, 0)),
            font_medium.render("MATHEUS MENDES", True, (0, 0, 0))
        ]

        #defina as posições
        title_rect = title.get_rect(center=(400, 325))
        name_rects = [
            names[0].get_rect(center=(400, 400)),
            names[1].get_rect(center=(400, 450)),
            names[2].get_rect(center=(400, 500))
        ]

        #renderiza os textos na tela
        self.screen.blit(title, title_rect)
        for name, rect in zip(names, name_rects):
            self.screen.blit(name, rect)

        #desenha os botões   
        for button in self.credits_buttons.values():
            button.draw(self.screen)

    #verifica os eventos
    def handle_events(self, event):
        """
        Gerencia os eventos com base na tela ativa.

        Args:
            event: O evento capturado pelo Pygame, como cliques ou teclas pressionadas.
        """
        #verifica os eventos no menu
        if self.active_screen == "menu":
            if self.menu_buttons["play"].is_clicked(event):
                self.active_screen = "game"
                self.music.play_music_game() 
            elif self.menu_buttons["credits"].is_clicked(event):
                self.active_screen = "credits"
                self.music.play_music_game()
            elif self.menu_buttons["quit"].is_clicked(event):
                pygame.quit()
                quit()
        #verifica os eventos em credits
        elif self.active_screen == "credits":
            if self.credits_buttons["back"].is_clicked(event):
                self.active_screen = "menu"
                self.music.play_music_menu()

    #atualiza a tela
    def update_screen(self):
        """
        Atualiza a tela com base na tela ativa.
        """
        if self.active_screen == "menu":
            self.menu_screen()
        elif self.active_screen == "credits":
            self.credits_screen()