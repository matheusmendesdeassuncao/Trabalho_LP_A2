import pygame
import math

def animar(frames, index, fps, frame_time):
    """
    Gerencia a animação dos sprites, atualizando o índice da imagem exibida.

    Parameters:
        frames (list): Uma lista de sprites para a animação.
        index (int): O índice atual do sprite sendo exibido.
        fps (int): O número de frames por segundo para a animação.

    Returns:
        image: Imagem no índice atual.
        int: O índice final 
    """
    frame_time += 1
    if frame_time >= fps:
        frame_time = 0
        index = (index + 1) % len(frames)
    return frames[index], index, frame_time

def carregar_sprites(image_util, num_frames, frame_width, frame_height, start_x = 0, start_y = 0):
    """
    Carrega uma spritesheet e divide em múltiplos sprites.

    Parameters:
        image_util: A imagem da spritesheet.
        num_frames (int): O número de sprites na spritesheet.
        frame_width (int): Largura de cada frame
        frame_height (int): Altura de cada frame
        start_x (int): Posição inicial da largura
        start_y (int): Posição inicial da altura

    Returns:
        list: Uma lista contendo os frames individuais
    """
    frames = []
    for i in range(num_frames):
        start_x_y = (i * frame_width + start_x, start_y)
        img = image_util.subsurface(start_x_y, (frame_width, frame_height))
        frames.append(img)
    return frames

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

class Door:
    def __init__(self, x, y, image, width, height, max_frames):
        """
        Inicializa a porta com a posição e sprites para animação.

        Parameters:
            x (int): A posição horizontal da porta.
            y (int): A posição vertical da porta.
            image: A spritesheet da porta a ser exibida na tela.
            width (int): Largura da porta.
            height (int): Altura da porta.
            max_frames (int): Quantidade de frames na imagem
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.max_frames = max_frames
        self.animation_frame = 0
        self.opening = False
        self.door_frames = []

        frame_width = image.get_width() // max_frames
        for i in range(max_frames):
            frame = image.subsurface(i*frame_width, 0, frame_width, image.get_height())
            self.door_frames.append(frame)
    
    def draw(self, screen):
        if self.opening:
            screen.blit(self.door_frames[self.animation_frame], (self.x, self.y))
        else:
            screen.blit(self.door_frames[0], (self.x, self.y))
    
    def animate(self):
        if self.opening and self.animation_frame < self.max_frames - 1:
            self.animation_frame += 1

    def interact(self, player, chave):
        if player.pegou_chave and not self.opening:
            self.opening = True

    def check_victory(self, player):
        """
        Verifica se o jogador alcançou a porta e possui a chave.

        Parameters:
            player (pygame.sprite.Sprite): O personagem principal do jogo.

        Returns:
            bool: Verdadeiro se o jogador alcançou a porta e possui a chave; caso contrário, Falso.
        """
        porta_centro_x = self.x + self.width // 2
        porta_centro_y = self.y + self.height // 2
        tolerancia = 20

        # Verifica se o jogador está dentro da área ao redor do centro da porta
        if (porta_centro_x - tolerancia <= player.rect.centerx <= porta_centro_x + tolerancia and
            porta_centro_y - tolerancia <= player.rect.centery <= porta_centro_y + tolerancia):
            return True
        return False

# Classe que representa um Player no jogo
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, width, height):
        """
        Inicializa um novo Player na posição (x, y) com a imagem fornecida.

        Args:
            x (int): A posição horizontal inicial do Player.
            y (int): A posição vertical inicial do Player.
            image: A imagem do Player a ser exibida na tela.
            width (int, opcional): Largura do Player. Padrão é 64.
            height (int, opcional): Altura do Player. Padrão é 64.
        """
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height
        self.vel_y = 0
        self.gravity = 0.5
        self.speed = 3
        self.is_jumping = False  # Indica se o Player está pulando
        self.is_alive = True  # Indica se o Player está vivo
        self.direction = pygame.Vector2(0, 0)  # Direção de movimento (horizontal e vertical)
        self.pegou_chave = False  # Adicionando o atributo pegou_chave

        self.idle = carregar_sprites(image, 2, width, height)
        
        self.run_rigth = carregar_sprites(image, 2, width, height, width*2)
        self.run_left = carregar_sprites(image, 2, width, height, width*4)
        
        self.jump_rigth = carregar_sprites(image, 1, width, height, width*2)
        self.jump_left = carregar_sprites(image, 1, width, height, width*4)

        self.index_lista = 0
        self.image = self.idle[self.index_lista]
        self.rect = self.image.get_rect()

        if height > 64:
            self.rect = pygame.Rect(x, y, width, height-1)
        else:
            self.rect = pygame.Rect(x, y, width, height+14)

        self.fps = 12
        self.frame_time = 0

        self.estado = 'idle'
        self.direcao = 'rigth'

    def pegar_chave(self):
        # Supondo que a chave seja um objeto ou algo que você possa checar se foi pego
        self.pegou_chave = True
        print(f"{self.nome} pegou a chave!")

    def jump(self):
        """
        Faz o Player pular, se ele não estiver já no ar.
        """
        if not self.is_jumping:
            self.estado = "jumping"
            self.vel_y = -12  # Define a velocidade de salto para cima
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

    def move(self, dx, obstacles, key):
        """
        Move o Player horizontalmente e verifica colisões.

        Args:
            dx (int): A direção do movimento (positivo para direita, negativo para esquerda).
            obstacles (list): Lista de obstáculos com os quais o Player pode colidir.
        """
        self.estado = "running"
        self.direction.x = dx  # Define a direção horizontal do movimento
        self.horizontal_movement_collision(obstacles)  # Verifica e resolve colisões horizontais
        if key == "rigth":
            self.direcao = "rigth"
        if key == "left":
            self.direcao = "left"
        if key == "idle":
            self.estado = "idle"

    def update(self, obstacles):
        """
        Atualiza o estado do Player, verificando colisões verticais e aplicando gravidade.

        Args:
            obstacles (list): Lista de obstáculos com os quais o Player pode colidir.
        """
        if self.is_alive:
            self.vertical_movement_collision(obstacles)  # Verifica e resolve colisões verticais

            frames = self.idle
            if self.estado == "idle":
                frames = self.idle
            elif self.estado == "running":
                if self.direcao == "rigth":
                    frames = self.run_rigth
                elif self.direcao == "left":
                    frames = self.run_left
            elif self.estado == "jumping":
                if self.direcao == "rigth":
                    frames = self.jump_rigth
                elif self.direcao == "left":
                    frames = self.jump_left
            
            if self.index_lista >= len(frames):
                self.index_lista = 0

            self.image, self.index_lista, self.frame_time = animar(frames, self.index_lista, self.fps, self.frame_time)
            
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
    def __init__(self, start_pos, y, image, width, height):
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
        self.rect = self.image.get_rect()
        self.rect.x = start_pos
        self.rect.y = y

        self.width = width
        self.height = height
        self.velocidade_y = 0
        self.aceleracao_gravidade = 0.5
        self.salto = -15
        self.no_chao = False
        self.speed = 0
        self.pode_mover = False
        self.deteccao_distancia = 200

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
        self.no_chao = False
        if not self.no_chao:
            self.velocidade_y += self.aceleracao_gravidade
            self.rect.y += self.velocidade_y
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle.rect):
                    if self.velocidade_y > 0:
                        self.rect.bottom = obstacle.rect.top
                        self.velocidade_y = 0
                        self.no_chao = True
                    elif self.velocidade_y < 0:
                        self.rect.top = obstacle.rect.bottom
                        self.velocidade_y = 0
                        self.no_chao = False

    def pular(self):
        """
        Faz o Inimigo pular, caso esteja no chão.
        """
        if self.no_chao:
            self.velocidade_y = self.salto
            self.no_chao = False
        
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

class Policial(Inimigo):
    def __init__(self, x, y, image, width, height):
        """
        Inicializa um Inimigo especializado em perseguir o Careca.

        Args:
            x (int): A posição horizontal inicial do Inimigo.
            y (int): A posição vertical inicial do Inimigo.
            image: A imagem do Inimigo.
            width (int): A largura do Inimigo.
            height (int): A altura do Inimigo.
        """
        super().__init__(x, y, image, width, height)
        
        self.idle = carregar_sprites(image, 7, 44, 60) 
        
        self.run_rigth = carregar_sprites(image, 7, 44, 60, 836)
        self.run_left = carregar_sprites(image, 7, 44, 60, 1144)

        self.index_lista = 0
        self.image = self.idle[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.fps = 7
        self.frame_time = 0

        self.estado = 'idle'
        self.direcao = 'rigth'

    def update(self, careca, peixonalta, obstacles):
        """
        Atualiza o comportamento do InimigoCareca, buscando o Careca.

        Args:
            careca (Player): O jogador Careca.
            peixonalta (Player): O jogador Peixonalta.
            obstacles (list): Lista de obstáculos com os quais o Inimigo pode colidir.
        """
        distancia_careca = math.sqrt((self.rect.x - careca.rect.x) ** 2 + (self.rect.y - careca.rect.y) ** 2)
        distancia_peixonalta = math.sqrt((self.rect.x - peixonalta.rect.x) ** 2 + (self.rect.y - peixonalta.rect.y) ** 2)

        if distancia_careca <= self.deteccao_distancia:
            alvo = careca
        elif distancia_peixonalta <= self.deteccao_distancia:
            alvo = peixonalta
        else:
            self.estado = "idle"
            alvo = None
            self.pode_mover = False
            self.speed = 0

        if alvo:
            self.estado = 'running'
            self.pode_mover = True
            if self.rect.x < alvo.rect.x:
                self.direcao = 'rigth'
                self.speed = 4
            else:
                self.direcao = 'left'
                self.speed = -4

            colidiu = self.move(obstacles)

            if colidiu and self.rect.y > alvo.rect.y:
                self.pular()

        self.gravidade(obstacles)

        if self.estado == "idle":
            frames = self.idle
        elif self.estado == "running":
            if self.direcao == "rigth":
                frames = self.run_rigth
            elif self.direcao == "left":
                frames = self.run_left
        
        self.image, self.index_lista, self.frame_time = animar(frames, self.index_lista, self.fps, self.frame_time)
        
    def verificar_morte(self, careca, peixonalta):
        super().verificar_morte(careca, peixonalta)

class InimigoCareca(Inimigo):
    def __init__(self, start_pos, y, image, width, height):
        """
        Inicializa um Inimigo especializado em perseguir o Careca.

        Args:
            x (int): A posição horizontal inicial do Inimigo.
            y (int): A posição vertical inicial do Inimigo.
            image: A imagem do Inimigo.
            width (int): A largura do Inimigo.
            height (int): A altura do Inimigo.
        """
        super().__init__(start_pos, y, image, width, height)
        self.y = y
        self.current_pos = start_pos
        self.end_pos = start_pos + 200
        self.start_pos = start_pos
        self.direction = 1

        self.left_frames = carregar_sprites(image, 4, 53, 37)
        self.rigth_frames = carregar_sprites(image, 4, 53, 37, 212)

        self.index_lista = 0
        self.fps = 7
        self.frame_time = 0

    def update(self):
        """
        Atualiza o comportamento do InimigoCareca, buscando o Careca.

        Args:
            careca (Player): O jogador Careca.
            peixonalta (Player): O jogador Peixonalta.
            obstacles (list): Lista de obstáculos com os quais o Inimigo pode colidir.
        """
        if self.direction == 1:
            if self.current_pos < self.end_pos:
                self.current_pos += 1
            else:
                self.direction = -1
        else:
            if self.current_pos > self.start_pos:
                self.current_pos -= 1
            else:
                self.direction = 1

        self.rect.x = self.current_pos
        self.rect = pygame.Rect(self.current_pos, self.y, self.width, self.height)

        frames = self.rigth_frames if self.direction == 1 else self.left_frames
        self.image, self.index_lista, self.frame_time = animar(frames, self.index_lista, self.fps, self.frame_time)
        
    def verificar_morte(self, careca):
        """
        Verifica se o InimigoCareca colidiu com o Careca, matando-o.

        Args:
            careca (Player): O jogador Careca.
        """
        if self.rect.colliderect(careca.rect):
            print(f"Colisão detectada! Inimigo: {self.rect}, Player: {careca.rect}")
            careca.morrer()

class InimigoPeixonalta(Inimigo):
    def __init__(self, start_pos, y, image, width, height):
        """
        Inicializa um Inimigo especializado em perseguir o Peixonalta.

        Args:
            x (int): A posição horizontal inicial do Inimigo.
            y (int): A posição vertical inicial do Inimigo.
            image: A imagem do Inimigo.
            width (int): A largura do Inimigo.
            height (int): A altura do Inimigo.
        """
        super().__init__(start_pos, y, image, width, height)
        self.current_pos = start_pos
        self.start_pos = start_pos
        self.end_pos = start_pos + 200
        self.direction = 1

        self.left_frames = carregar_sprites(image, 2, 64, 44, start_y = 20)
        self.rigth_frames = carregar_sprites(image, 2, 64, 44, 128, 20)

        self.index_lista = 0
        self.fps = 7
        self.frame_time = 0
        self.y = y + 20

    def update(self):
        """
        Atualiza o comportamento do InimigoPeixonalta, buscando o Peixonalta.

        Args:
            careca (Player): O jogador Careca.
            peixonalta (Player): O jogador Peixonalta.
            obstacles (list): Lista de obstáculos com os quais o Inimigo pode colidir.
        """
        if self.direction == 1:
            if self.current_pos < self.end_pos:
                self.current_pos += 1
            else:
                self.direction = -1
        else:
            if self.current_pos > self.start_pos:
                self.current_pos -= 1
            else:
                self.direction = 1

        self.rect = pygame.Rect(self.current_pos, self.y, self.width, self.height)

        frames = self.rigth_frames if self.direction == 1 else self.left_frames
        self.image, self.index_lista, self.frame_time = animar(frames, self.index_lista, self.fps, self.frame_time)

    def verificar_morte(self, peixonalta):
        """
        Verifica se o InimigoPeixonalta colidiu com o Peixonalta, matando-o.

        Args:
            peixonalta (Player): O jogador Peixonalta.
        """
        if self.rect.colliderect(peixonalta.rect):
            print(f"Colisão detectada! Inimigo: {self.rect}, Player: {peixonalta.rect}")
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
        