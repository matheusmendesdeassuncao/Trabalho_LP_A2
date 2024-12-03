import pygame

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