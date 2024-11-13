import pygame
from button import Button

class Display:
    def __init__(self, screen):
        self.screen = screen
        self.active_screen = "menu"

        self.init_menu()
        self.init_credits()

    #inicializa elementos da tela menu
    def init_menu(self):
        self.menu_background = (255,192,203)
        self.menu_buttons = {
            "play": Button(300, 250, 200, 50, text="Play"),
            "credits": Button(300, 350, 200, 50, text="Credits"),
            "quit": Button(300, 450, 200, 50, text="Quit")
        }

    #inicializa elementos da tela credits
    def init_credits(self):
        self.credits_background = (255,192,203)
        self.credits_buttons = {
            "back": Button(300, 250, 200, 50, text="Back")
        }

    #desenha a tela menu
    def menu_screen(self):
        self.screen.fill(self.menu_background)
        for button in self.menu_buttons.values():
            button.draw(self.screen)
    
    #desenha a tela credits
    def credits_screen(self):
        self.screen.fill(self.credits_background)
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
