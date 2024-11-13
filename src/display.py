import pygame
from button import Button

class Display:
    def __init__(self, screen):
        self.screen = screen
        self.active_screen = "menu"

        self.init_menu()
        self.init_credits()

    def init_menu(self):
        #carrega a imagem e ajusta o tamanho
        self.menu_background = pygame.image.load("../assets/background_menu.png")
        self.menu_background = pygame.transform.scale(self.menu_background, (self.screen.get_width(), self.screen.get_height()))
        
        #inicializa os botões do menu
        self.menu_buttons = {
            "play": Button(300, 250, 200, 50, text="Play"),
            "credits": Button(300, 350, 200, 50, text="Credits"),
            "quit": Button(300, 450, 200, 50, text="Quit")
        }

    #inicializa elementos da tela credits
    def init_credits(self):
        #carrega a imagem e ajusta o tamanho
        self.credits_background = pygame.image.load("../assets/background_credits.png")
        self.credits_background = pygame.transform.scale(self.credits_background, (self.screen.get_width(), self.screen.get_height()))
        
        #inicializa os botões de credits
        self.credits_buttons = {
            "back": Button(30, 530, 200, 50, text="Back")
        }

    #desenha a tela menu
    def menu_screen(self):
        self.screen.blit(self.menu_background, (0, 0))
        for button in self.menu_buttons.values():
            button.draw(self.screen)
    
    #desenha a tela credits
    def credits_screen(self):
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
        #verifica os eventos no menu
        if self.active_screen == "menu":
            if self.menu_buttons["play"].is_clicked(event):
                self.active_screen = "game"
            elif self.menu_buttons["credits"].is_clicked(event):
                self.active_screen = "credits"
            elif self.menu_buttons["quit"].is_clicked(event):
                pygame.quit()
                quit()
        #verifica os eventos em credits
        elif self.active_screen == "credits":
            if self.credits_buttons["back"].is_clicked(event):
                self.active_screen = "menu"

    #atualiza a tela
    def update_screen(self):
        if self.active_screen == "menu":
            self.menu_screen()
        elif self.active_screen == "credits":
            self.credits_screen()
