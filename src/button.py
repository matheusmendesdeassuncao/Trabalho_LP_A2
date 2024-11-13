import pygame

class Button:
    def __init__(self, x, y, width, height, text='', font_size=30, color=(0,0,0), text_color=(255,255,255), selected_color=(255,192,203)):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color 
        self.selected_color = selected_color
        self.text = text
        self.text_color= text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_selected = False

    def draw(self, screen):

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
        if self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return False