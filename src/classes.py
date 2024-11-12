import pygame
import random
from math import sqrt

# Classe que representa um obstáculo no jogo
class Obstacle:
    def __init__(self, x, y):
        """
        Inicializa um novo obstáculo na posição (x, y).

        Args:
            x (int): A posição horizontal do obstáculo.
            y (int): A posição vertical do obstáculo.
        """
        # Define a área do obstáculo como um retângulo com largura e altura de 32 pixels
        self.rect = pygame.Rect(x, y, 32, 32)

    def draw(self, screen: pygame.Surface):
        """
        Desenha o obstáculo na tela.

        Args:
            screen (pygame.Surface): A superfície onde o obstáculo será desenhado.
        """
        pygame.draw.rect(screen, (0, 0, 0), self.rect)  # Desenha o obstáculo em preto


# Classe que representa um jogador no jogo
class Player:
    def __init__(self, x: int, y: int, image, width: int = 64, height: int = 64):
        """
        Inicializa um novo jogador na posição (x, y) com a imagem fornecida.

        Args:
            x (int): A posição horizontal inicial do jogador.
            y (int): A posição vertical inicial do jogador.
            image: A imagem do jogador a ser exibida na tela.
            width (int, opcional): Largura do jogador. Padrão é 64.
            height (int, opcional): Altura do jogador. Padrão é 64.
        """
        self.rect = pygame.Rect(x, y, width, height)  # A área do jogador (retângulo)
        self.image = image  # A imagem do jogador
        self.vel_y = 0  # Velocidade vertical (para pular e gravidade)
        self.gravity = 0.5  # A intensidade da gravidade
        self.is_jumping = False  # Indica se o jogador está pulando
        self.is_alive = True  # Indica se o jogador está vivo
        self.speed = 5  # Velocidade do jogador
        self.direction = pygame.Vector2(0, 0)  # Direção de movimento (horizontal e vertical)

    def jump(self):
        """
        Faz o jogador pular, se ele não estiver já no ar.
        """
        if not self.is_jumping:
            self.vel_y = -15  # Define a velocidade de salto para cima
            self.is_jumping = True  # Marca que o jogador está pulando

    def apply_gravity(self):
        """
        Aplica a gravidade ao jogador, fazendo-o cair.
        """
        self.vel_y += self.gravity  # Aumenta a velocidade vertical com a gravidade
        self.rect.y += self.vel_y  # Atualiza a posição vertical do jogador

    def horizontal_movement_collision(self, obstacles):
        """
        Verifica e resolve colisões horizontais do jogador com obstáculos.

        Args:
            obstacles (list): Lista de obstáculos com os quais o jogador pode colidir.
        """
        self.rect.x += self.direction.x * self.speed  # Atualiza a posição horizontal do jogador
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):  # Verifica colisão com cada obstáculo
                if self.direction.x < 0:
                    self.rect.left = obstacle.rect.right  # Resolve colisão à esquerda
                elif self.direction.x > 0:
                    self.rect.right = obstacle.rect.left  # Resolve colisão à direita

    def vertical_movement_collision(self, obstacles):
        """
        Verifica e resolve colisões verticais do jogador com obstáculos.

        Args:
            obstacles (list): Lista de obstáculos com os quais o jogador pode colidir.
        """
        self.apply_gravity()  # Aplica a gravidade ao jogador
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):  # Verifica colisão com cada obstáculo
                if self.vel_y > 0:
                    self.rect.bottom = obstacle.rect.top  # Resolve colisão com o chão
                    self.is_jumping = False  # O jogador não está mais pulando
                    self.vel_y = 0  # Zera a velocidade vertical
                elif self.vel_y < 0:
                    self.rect.top = obstacle.rect.bottom  # Resolve colisão com o teto
                    self.vel_y = 0  # Zera a velocidade vertical

    def move(self, dx, obstacles):
        """
        Move o jogador horizontalmente e verifica colisões.

        Args:
            dx (int): A direção do movimento (positivo para direita, negativo para esquerda).
            obstacles (list): Lista de obstáculos com os quais o jogador pode colidir.
        """
        self.direction.x = dx  # Define a direção horizontal do movimento
        self.horizontal_movement_collision(obstacles)  # Verifica e resolve colisões horizontais

    def update(self, obstacles):
        """
        Atualiza o estado do jogador, verificando colisões verticais e aplicando gravidade.

        Args:
            obstacles (list): Lista de obstáculos com os quais o jogador pode colidir.
        """
        if self.is_alive:
            self.vertical_movement_collision(obstacles)  # Verifica e resolve colisões verticais

    def draw(self, screen: pygame.Surface):
        """
        Desenha o jogador na tela.

        Args:
            screen (pygame.Surface): A superfície onde o jogador será desenhado.
        """
        if self.is_alive:
            screen.blit(self.image, self.rect.topleft)  # Desenha a imagem do jogador

    def check_death(self, level, player_name):
        """
        Verifica se o jogador morreu, dependendo da posição na tela e do tipo de obstáculo.

        Args:
            level (list): O mapa do nível, representado por uma lista de strings.
            player_name (str): O nome do jogador (usado para verificar obstáculos específicos).

        Returns:
            bool: Retorna True se o jogador morreu, False caso contrário.
        """
        if 0 <= self.rect.y // 32 < len(level) and 0 <= self.rect.x // 32 < len(level[0]):
            tile = level[self.rect.y // 32][self.rect.x // 32]  # Pega o tipo de tile no nível
            if tile == "T":
                return True  # "T" mata ambos os personagens
            elif tile == "U" and player_name == "alexandre_de_morais":
                return True  # "U" mata apenas Alexandre de Morais
            elif tile == "V" and player_name == "peixonalta":
                return True  # "V" mata apenas Peixonalta
        return False  # Retorna False se o jogador não morreu


import pygame
import math

import pygame
import math

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, image, width, height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.velocidade_y = 0
        self.aceleracao_gravidade = 0.5
        self.salto = -10
        self.no_chao = False
        self.speed = 0
        self.pode_mover = False
        self.deteccao_distancia = 200  # Raio de detecção

    def move(self, obstacles):
        if self.pode_mover:
            self.rect.x += self.speed
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle.rect):
                    if self.speed > 0:
                        self.rect.right = obstacle.rect.left
                    elif self.speed < 0:
                        self.rect.left = obstacle.rect.right

    def gravidade(self, obstacles):
        if not self.no_chao:
            self.velocidade_y += self.aceleracao_gravidade
            self.rect.y += self.velocidade_y
            self.no_chao = False
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle.rect) and self.velocidade_y > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.velocidade_y = 0
                    self.no_chao = True

    def pular(self):
        if self.no_chao:
            self.velocidade_y = self.salto
            self.no_chao = False

    def update(self, careca, peixonalta, obstacles):
        distancia_careca = math.sqrt((self.rect.x - careca.rect.x) ** 2 + (self.rect.y - careca.rect.y) ** 2)
        distancia_peixonalta = math.sqrt((self.rect.x - peixonalta.rect.x) ** 2 + (self.rect.y - peixonalta.rect.y) ** 2)

        # Verifica se o inimigo deve perseguir o Careca ou o Peixonalta
        if distancia_careca <= self.deteccao_distancia:
            self.pode_mover = True
            if self.rect.x < careca.rect.x:
                self.speed = 2
            elif self.rect.x > careca.rect.x:
                self.speed = -2
        elif distancia_peixonalta <= self.deteccao_distancia:
            self.pode_mover = True
            if self.rect.x < peixonalta.rect.x:
                self.speed = 2
            elif self.rect.x > peixonalta.rect.x:
                self.speed = -2
        else:
            self.pode_mover = False

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect) and self.no_chao:
                self.pular()

        self.gravidade(obstacles)
        self.move(obstacles)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def verificar_morte(self, careca, peixonalta):
        """Verifica se o inimigo matou o personagem correto"""
        # Inimigo exclusivo do Careca
        if isinstance(self, InimigoCareca):
            if self.rect.colliderect(careca.rect):
                careca.morrer()  # O Careca morre
        # Inimigo exclusivo do Peixonalta
        elif isinstance(self, InimigoPeixonalta):
            if self.rect.colliderect(peixonalta.rect):
                peixonalta.morrer()  # O Peixonalta morre

# Subclasse do Inimigo que persegue o Careca
class InimigoCareca(Inimigo):
    def __init__(self, x, y, image, width, height):
        super().__init__(x, y, image, width, height)

    def update(self, careca, peixonalta, obstacles):
        super().update(careca, peixonalta, obstacles)

    def verificar_morte(self, careca):
        if self.rect.colliderect(careca.rect):
            careca.morrer()  # Mata o Careca quando colide

# Subclasse do Inimigo que persegue o Peixonalta
class InimigoPeixonalta(Inimigo):
    def __init__(self, x, y, image, width, height):
        super().__init__(x, y, image, width, height)

    def update(self, careca, peixonalta, obstacles):
        super().update(careca, peixonalta, obstacles)

    def verificar_morte(self, peixonalta):
        if self.rect.colliderect(peixonalta.rect):
            peixonalta.morrer()  # Mata o Peixonalta quando colide



