import pygame
import random
import math

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


# Classe que representa um Player no jogo
class Player:
    def __init__(self, x: int, y: int, image, width: int = 64, height: int = 64):
        """
        Inicializa um novo Player na posição (x, y) com a imagem fornecida.

        Args:
            x (int): A posição horizontal inicial do Player.
            y (int): A posição vertical inicial do Player.
            image: A imagem do Player a ser exibida na tela.
            width (int, opcional): Largura do Player. Padrão é 64.
            height (int, opcional): Altura do Player. Padrão é 64.
        """
        self.rect = pygame.Rect(x, y, width, height)  # A área do Player (retângulo)
        self.image = image  # A imagem do Player
        self.vel_y = 0  # Velocidade vertical (para pular e gravidade)
        self.gravity = 0.5  # A intensidade da gravidade
        self.is_jumping = False  # Indica se o Player está pulando
        self.is_alive = True  # Indica se o Player está vivo
        self.speed = 5  # Velocidade do Player
        self.direction = pygame.Vector2(0, 0)  # Direção de movimento (horizontal e vertical)
        self.pegou_chave = False  # Adicionando o atributo pegou_chave

    def pegar_chave(self):
        # Supondo que a chave seja um objeto ou algo que você possa checar se foi pego
        self.pegou_chave = True
        print(f"{self.nome} pegou a chave!")

    def jump(self):
        """
        Faz o Player pular, se ele não estiver já no ar.
        """
        if not self.is_jumping:
            self.vel_y = -15  # Define a velocidade de salto para cima
            self.is_jumping = True  # Marca que o Player está pulando

    def apply_gravity(self):
        """
        Aplica a gravidade ao Player, fazendo-o cair.
        """
        self.vel_y += self.gravity  # Aumenta a velocidade vertical com a gravidade
        self.rect.y += self.vel_y  # Atualiza a posição vertical do Player

    def horizontal_movement_collision(self, obstacles):
        """
        Verifica e resolve colisões horizontais do Player com obstáculos.

        Args:
            obstacles (list): Lista de obstáculos com os quais o Player pode colidir.
        """
        self.rect.x += self.direction.x * self.speed  # Atualiza a posição horizontal do Player
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):  # Verifica colisão com cada obstáculo
                if self.direction.x < 0:
                    self.rect.left = obstacle.rect.right  # Resolve colisão à esquerda
                elif self.direction.x > 0:
                    self.rect.right = obstacle.rect.left  # Resolve colisão à direita

    def vertical_movement_collision(self, obstacles):
        """
        Verifica e resolve colisões verticais do Player com obstáculos.

        Args:
            obstacles (list): Lista de obstáculos com os quais o Player pode colidir.
        """
        self.apply_gravity()  # Aplica a gravidade ao Player
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):  # Verifica colisão com cada obstáculo
                if self.vel_y > 0:
                    self.rect.bottom = obstacle.rect.top  # Resolve colisão com o chão
                    self.is_jumping = False  # O Player não está mais pulando
                    self.vel_y = 0  # Zera a velocidade vertical
                elif self.vel_y < 0:
                    self.rect.top = obstacle.rect.bottom  # Resolve colisão com o teto
                    self.vel_y = 0  # Zera a velocidade vertical

    def move(self, dx, obstacles):
        """
        Move o Player horizontalmente e verifica colisões.

        Args:
            dx (int): A direção do movimento (positivo para direita, negativo para esquerda).
            obstacles (list): Lista de obstáculos com os quais o Player pode colidir.
        """
        self.direction.x = dx  # Define a direção horizontal do movimento
        self.horizontal_movement_collision(obstacles)  # Verifica e resolve colisões horizontais

    def update(self, obstacles):
        """
        Atualiza o estado do Player, verificando colisões verticais e aplicando gravidade.

        Args:
            obstacles (list): Lista de obstáculos com os quais o Player pode colidir.
        """
        if self.is_alive:
            self.vertical_movement_collision(obstacles)  # Verifica e resolve colisões verticais

    def draw(self, screen: pygame.Surface):
        """
        Desenha o Player na tela.

        Args:
            screen (pygame.Surface): A superfície onde o Player será desenhado.
        """
        if self.is_alive:
            screen.blit(self.image, self.rect.topleft)  # Desenha a imagem do Player

    def check_death(self, level, player_name):
        """
        Verifica se o Player morreu, dependendo da posição na tela e do tipo de obstáculo.

        Args:
            level (list): O mapa do nível, representado por uma lista de strings.
            player_name (str): O nome do Player (usado para verificar obstáculos específicos).

        Returns:
            bool: Retorna True se o Player morreu, False caso contrário.
        """
        if 0 <= self.rect.y // 32 < len(level) and 0 <= self.rect.x // 32 < len(level[0]):
            tile = level[self.rect.y // 32][self.rect.x // 32]  # Pega o tipo de tile no nível
            if tile == "T":
                return True  # "T" mata ambos os personagens
            elif tile == "U" and player_name == "careca":
                return True  # "U" mata apenas Alexandre de Morais
            elif tile == "V" and player_name == "peixonalta":
                return True  # "V" mata apenas Peixonalta
        return False  # Retorna False se o Player não morreu

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, image, width, height):
        """
        Inicializa um novo inimigo com a posição (x, y), imagem, largura e altura fornecidos.

        Args:
            x (int): A posição horizontal inicial do Inimigo.
            y (int): A posição vertical inicial do Inimigo.
            image: A imagem do Inimigo a ser exibida na tela.
            width (int): A largura do Inimigo.
            height (int): A altura do Inimigo.
        """
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        #self.img_right = img_rigth

        self.imagens_cobra = []
        for i in range(4):
            img = self.image.subsurface((i*53,0), (53, 37))
            self.imagens_cobra.append(img)

        self.index_lista = 0
        self.image = self.imagens_cobra[self.index_lista]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.rect.center = (x, y)

        self.width = width
        self.height = height
        self.velocidade_y = 0
        self.aceleracao_gravidade = 0.5
        self.salto = -15
        self.no_chao = False
        self.speed = 0
        self.pode_mover = False
        self.deteccao_distancia = 250

    def move(self, obstacles):
        """
        Move o inimigo horizontalmente e verifica colisões com os obstáculos.

        Args:
            obstacles (list): Lista de obstáculos com os quais o Inimigo pode colidir.

        Returns:
            bool: Retorna True se houve colisão com um obstáculo, False caso contrário.
        """
        if self.pode_mover:
            self.rect.x += self.speed
            colidiu = False
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle.rect):
                    colidiu = True
                    if self.speed > 0:
                        self.rect.right = obstacle.rect.left
                    elif self.speed < 0:
                        self.rect.left = obstacle.rect.right
            return colidiu
        return False

    def gravidade(self, obstacles):
        """
        Aplica a gravidade ao Inimigo, fazendo-o cair e verificar colisões com o chão ou teto.

        Args:
            obstacles (list): Lista de obstáculos com os quais o Inimigo pode colidir.
        """
        if not self.no_chao:
            self.velocidade_y += self.aceleracao_gravidade
            self.rect.y += self.velocidade_y
            self.no_chao = False
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle.rect):
                    if self.velocidade_y > 0:
                        self.rect.bottom = obstacle.rect.top
                        self.velocidade_y = 0
                        self.no_chao = True
                    elif self.velocidade_y < 0:
                        self.rect.top = obstacle.rect.bottom
                        self.velocidade_y = 0

    def pular(self):
        """
        Faz o Inimigo pular, caso esteja no chão.
        """
        if self.no_chao:
            self.velocidade_y = self.salto
            self.no_chao = False

    def update(self, careca, peixonalta, obstacles):
        """
        Atualiza o estado do Inimigo, verificando as distâncias até os personagens, se deve se mover e aplicar gravidade.

        Args:
            careca (Player): O jogador chamado Careca.
            peixonalta (Player): O jogador chamado Peixonalta.
            obstacles (list): Lista de obstáculos com os quais o Inimigo pode colidir.
        """
        distancia_careca = math.sqrt((self.rect.x - careca.rect.x) ** 2 + (self.rect.y - careca.rect.y) ** 2)
        distancia_peixonalta = math.sqrt((self.rect.x - peixonalta.rect.x) ** 2 + (self.rect.y - peixonalta.rect.y) ** 2)

        if distancia_careca <= self.deteccao_distancia:
            alvo = careca
        elif distancia_peixonalta <= self.deteccao_distancia:
            alvo = peixonalta
        else:
            alvo = None
            self.pode_mover = False
            self.speed = 0

        if alvo:
            self.pode_mover = True
            if self.rect.x < alvo.rect.x:
                self.speed = 2
            elif self.rect.x > alvo.rect.x:
                self.speed = -2

            colidiu = self.move(obstacles)

            if colidiu and self.rect.y > alvo.rect.y:
                self.pular()

        self.gravidade(obstacles)

    def draw(self, screen):
        """
        Desenha o Inimigo na tela.

        Args:
            screen (pygame.Surface): A superfície onde o Inimigo será desenhado.
        """
        screen.blit(self.image, self.rect)

    def pegar_chave(self):
        """
        Marca que o Inimigo pegou a chave (caso o conceito de chave se aplique ao Inimigo).

        """
        self.pegou_chave = True

    def verificar_morte(self, careca, peixonalta):
        """
        Verifica se o Inimigo colidiu com o Careca ou o Peixonalta e mata o jogador correspondente.

        Args:
            careca (Player): O jogador Careca.
            peixonalta (Player): O jogador Peixonalta.
        """
        if isinstance(self, InimigoCareca) and self.rect.colliderect(careca.rect):
            careca.morrer()
        elif isinstance(self, InimigoPeixonalta) and self.rect.colliderect(peixonalta.rect):
            peixonalta.morrer()


class InimigoCareca(Inimigo):
    def __init__(self, x, y, img_left, width, height):
        """
        Inicializa um Inimigo especializado em perseguir o Careca.

        Args:
            x (int): A posição horizontal inicial do Inimigo.
            y (int): A posição vertical inicial do Inimigo.
            image: A imagem do Inimigo.
            width (int): A largura do Inimigo.
            height (int): A altura do Inimigo.
        """
        super().__init__(x, y, img_left, width, height)
        self.img_left = img_left

    def update(self, careca, peixonalta, obstacles):
        """
        Atualiza o comportamento do InimigoCareca, buscando o Careca.

        Args:
            careca (Player): O jogador Careca.
            peixonalta (Player): O jogador Peixonalta.
            obstacles (list): Lista de obstáculos com os quais o Inimigo pode colidir.
        """
        super().update(careca, peixonalta, obstacles)
        if self.index_lista > 3:
            self.index_lista = 0
        self.index_lista += 0.1
        self.image = self.imagens_cobra[int(self.index_lista)]

    def verificar_morte(self, careca):
        """
        Verifica se o InimigoCareca colidiu com o Careca, matando-o.

        Args:
            careca (Player): O jogador Careca.
        """
        if self.rect.colliderect(careca.rect):
            careca.morrer()


class InimigoPeixonalta(Inimigo):
    def __init__(self, x, y, img_left, width, height):
        """
        Inicializa um Inimigo especializado em perseguir o Peixonalta.

        Args:
            x (int): A posição horizontal inicial do Inimigo.
            y (int): A posição vertical inicial do Inimigo.
            image: A imagem do Inimigo.
            width (int): A largura do Inimigo.
            height (int): A altura do Inimigo.
        """
        super().__init__(x, y, img_left, width, height)

    def update(self, careca, peixonalta, obstacles):
        """
        Atualiza o comportamento do InimigoPeixonalta, buscando o Peixonalta.

        Args:
            careca (Player): O jogador Careca.
            peixonalta (Player): O jogador Peixonalta.
            obstacles (list): Lista de obstáculos com os quais o Inimigo pode colidir.
        """
        super().update(careca, peixonalta, obstacles)

    def verificar_morte(self, peixonalta):
        """
        Verifica se o InimigoPeixonalta colidiu com o Peixonalta, matando-o.

        Args:
            peixonalta (Player): O jogador Peixonalta.
        """
        if self.rect.colliderect(peixonalta.rect):
            peixonalta.morrer()


class Chave(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites):
        """
        Inicializa uma nova chave na posição (x, y) com a imagem fornecida.

        Args:
            x (int): A posição horizontal da chave.
            y (int): A posição vertical da chave.
            image: A imagem da chave a ser exibida na tela.
        """
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.atual = 0
        self.image = self.sprites[self.atual]
    
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pegada = False  # A chave não foi pegada inicialmente

    def update(self):
        self.atual += 0.1
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]

    def colisao(self, player):
        """
        Verifica se o Player colidiu com a chave e a pegou.

        Args:
            player (Player): O jogador que pode pegar a chave.
        """
        if self.rect.colliderect(player.rect) and not player.pegou_chave:
            player.pegou_chave = True  # Marca que o jogador pegou a chave
            self.kill()

    def draw(self, screen):
        """
        Desenha a chave na tela.

        Args:
            screen (pygame.Surface): A superfície onde a chave será desenhada.
        """
        screen.blit(self.image, self.rect)