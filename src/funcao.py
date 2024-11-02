import pygame
import os

# Inicializa o Pygame
pygame.init()

# Define as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Configuração da tela
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("As Aventuras de Helora e Gabrela")  # Nome do jogo

# Função para carregar e redimensionar imagem
def load_image(image_path, file_name, width, height):
    full_path = os.path.join(image_path, file_name)
    if os.path.exists(full_path):
        image = pygame.image.load(full_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    else:
        print(f"Arquivo não encontrado: {full_path}")
        return None

# Atualiza o caminho para a pasta 'assets'
current_path = os.path.dirname(__file__)  # Local do arquivo
image_path = os.path.abspath(os.path.join(current_path, '..', 'assets'))  # Caminho para a pasta 'assets'
louriskelly_img = load_image(image_path, 'fireboy.png', 64, 64)  # Imagem do LourisKelly
gabikkk_img = load_image(image_path, 'watergirl.png', 64, 64)  # Imagem da Gabikkkk

if louriskelly_img is None or gabikkk_img is None:
    print("Erro: Imagem não encontrada.")
    pygame.quit()
    exit()

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)  # Define a posição e o tamanho do obstáculo

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, BLACK, self.rect)  # Desenha o obstáculo em preto

class Player:
    def __init__(self, x: int, y: int, image, width: int = 64, height: int = 64):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.vel_y = 0
        self.gravity = 0.5
        self.is_jumping = False
        self.is_alive = True  # Estado do jogador
        self.speed = 5  # Velocidade do movimento

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -10
            self.is_jumping = True

    def apply_gravity(self):
        if self.is_alive:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y

            # Colisão com o chão
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.is_jumping = False
                self.vel_y = 0

    def on_collision(self, other):
        if not self.rect.colliderect(other.rect):
            return

        if isinstance(other, Obstacle):
            if self.vel_y > 0:  # Colisão descendo
                self.rect.bottom = other.rect.top  # Ajusta o personagem para ficar sobre o chão
                self.is_jumping = False  # Permite pular novamente ao tocar o chão
                self.vel_y = 0  # Zera a velocidade vertical
            elif self.vel_y < 0:  # Colisão subindo
                self.rect.top = other.rect.bottom  # Ajusta a posição do personagem
                self.vel_y = 0  # Zera a velocidade vertical
            elif self.rect.right > other.rect.left and self.rect.left < other.rect.left:  # Colisão pela esquerda
                self.rect.right = other.rect.left
            elif self.rect.left < other.rect.right and self.rect.right > other.rect.right:  # Colisão pela direita
                self.rect.left = other.rect.right

    def move(self, dx):
        self.rect.x += dx

        # Restringe o movimento dentro da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self, obstacles):
        if self.is_alive:
            self.apply_gravity()
            # Verifica colisão com obstáculos
            for obstacle in obstacles:
                self.on_collision(obstacle)

    def draw(self, screen: pygame.Surface):
        if self.is_alive:  # Desenha o jogador somente se estiver vivo
            screen.blit(self.image, self.rect.topleft)

# Posições iniciais ajustadas
louriskelly = Player(100, 600, louriskelly_img, 64, 64)  # Posição inicial do LourisKelly (dentro da tela)
gabikkk = Player(200, 600, gabikkk_img, 64, 64)  # Posição inicial da Gabikkkk (dentro da tela)

# Função para carregar nível
def load_level():
    level = [
        "##################################################",
        "#                                                #",
        "#    F            T             T                #",
        "#    # # #                                 E     #",
        "#        # ##            #########   #############",
        "#           #                      # #           #",
        "#           #                     #  #           #",
        "#           ##########   #   #####   #           #",
        "#                      # #           #           #",
        "#        #            #  #           #           #",
        "#        #            #  #########   #           #",
        "#        #            #              #           #",
        "#        #            ##  ########## #           #",
        "#        #            #              #           #",
        "#        #            #   #######    #           #",
        "#        #   #        #              #           #",
        "#        #   #        ############  ##           #",
        "#        #   #        #              #           #",
        "#        #   ##########              #           #",
        "#           #                #########           #",
        "#                           #        #           #",
        "#                        # #   #     #           #",
        "#                  #   # #     #     #           #",
        "##################################################"
    ]
    return level

# Função para desenhar o nível
def draw_level(screen, level):
    obstacles = []  # Lista de obstáculos
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == "#":
                pygame.draw.rect(screen, BLACK, (x * 32, y * 32, 32, 32))  # Desenha a parede em preto
                obstacles.append(Obstacle(x * 32, y * 32))  # Adiciona à lista de obstáculos
            elif char == "F":
                pygame.draw.rect(screen, RED, (x * 32, y * 32, 32, 32))  # Área de vitória do LourisKelly
            elif char == "E":
                pygame.draw.rect(screen, BLUE, (x * 32, y * 32, 32, 32))  # Área de vitória do Gabikkkk
            elif char == "T":
                pygame.draw.rect(screen, GREEN, (x * 32, y * 32, 32, 32))  # Ponto de interesse
    return obstacles  # Retorna a lista de obstáculos

# Função para verificar vitória
def check_victory(louriskelly, gabikkk, level):
    fireboy_victory = False
    if 0 <= louriskelly.rect.y // 32 < len(level) and 0 <= louriskelly.rect.x // 32 < len(level[0]):
        fireboy_victory = level[louriskelly.rect.y // 32][louriskelly.rect.x // 32] == "F"
    
    watergirl_victory = False
    if 0 <= gabikkk.rect.y // 32 < len(level) and 0 <= gabikkk.rect.x // 32 < len(level[0]):
        watergirl_victory = level[gabikkk.rect.y // 32][gabikkk.rect.x // 32] == "E"
    
    return fireboy_victory and watergirl_victory

# Loop principal
running = True
clock = pygame.time.Clock()

level = load_level()  # Carrega o nível apenas uma vez antes do loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controle do personagem LourisKelly com W, A, S, D
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        louriskelly.move(-louriskelly.speed)
    if keys[pygame.K_d]:
        louriskelly.move(louriskelly.speed)
    if keys[pygame.K_w]:  # Usado para pular LourisKelly
        louriskelly.jump()

    # Controle do personagem Gabikkkk com setas
    if keys[pygame.K_LEFT]:
        gabikkk.move(-gabikkk.speed)
    if keys[pygame.K_RIGHT]:
        gabikkk.move(gabikkk.speed)
    if keys[pygame.K_UP]:  # Usado para pular Gabikkkk
        gabikkk.jump()

    # Limpa a tela
    screen.fill(WHITE)

    # Desenha o nível e atualiza obstáculos
    obstacles = draw_level(screen, level)  # Gera e desenha obstáculos
    louriskelly.update(obstacles)  # Atualiza LourisKelly
    gabikkk.update(obstacles)  # Atualiza Gabikkkk
    louriskelly.draw(screen)  # Desenha LourisKelly
    gabikkk.draw(screen)  # Desenha Gabikkkk

    # Verifica vitória
    if check_victory(louriskelly, gabikkk, level):
        print("Vitória!")
        running = False

    pygame.display.flip()
    clock.tick(60)  # Limita a 60 quadros por segundo

pygame.quit()
