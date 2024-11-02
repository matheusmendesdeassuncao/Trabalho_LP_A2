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
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fireboy & Watergirl")

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
fireboy_img = load_image(image_path, 'fireboy.png', 64, 64)
watergirl_img = load_image(image_path, 'watergirl.png', 64, 64)

if fireboy_img is None or watergirl_img is None:
    print("Erro: Imagem não encontrada.")
    pygame.quit()
    exit()

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Define a posição e o tamanho do obstáculo

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, BLUE, self.rect)  # Desenha o obstáculo

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
        if self.rect.colliderect(other.rect):
            # Se está caindo
            if self.vel_y > 0:  
                self.rect.bottom = other.rect.top  # Ajusta para cima do obstáculo
                self.is_jumping = False
                self.vel_y = 0
            elif self.vel_y < 0:  # Se está subindo
                self.rect.top = other.rect.bottom  # Ajusta para baixo do obstáculo

            # Restringe a movimentação horizontal se colidir nas laterais
            if self.rect.right > other.rect.left and self.rect.left < other.rect.left:
                self.rect.right = other.rect.left  # Colisão à esquerda
            elif self.rect.left < other.rect.right and self.rect.right > other.rect.right:
                self.rect.left = other.rect.right  # Colisão à direita

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

# Posições iniciais
fireboy = Player(100, 700, fireboy_img, 64, 64)  # Posição inicial do Fireboy
watergirl = Player(200, 700, watergirl_img, 64, 64)  # Posição inicial da Watergirl

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
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == "#":
                pygame.draw.rect(screen, BLACK, (x * 32, y * 32, 32, 32))
            elif char == "F":
                pygame.draw.rect(screen, RED, (x * 32, y * 32, 32, 32))
            elif char == "E":
                pygame.draw.rect(screen, BLUE, (x * 32, y * 32, 32, 32))
            elif char == "T":
                pygame.draw.rect(screen, GREEN, (x * 32, y * 32, 32, 32))

# Função para verificar vitória
def check_victory(fireboy, watergirl, level):
    fireboy_victory = False
    if 0 <= fireboy.rect.y // 32 < len(level) and 0 <= fireboy.rect.x // 32 < len(level[0]):
        fireboy_victory = level[fireboy.rect.y // 32][fireboy.rect.x // 32] == "F"
    
    watergirl_victory = False
    if 0 <= watergirl.rect.y // 32 < len(level) and 0 <= watergirl.rect.x // 32 < len(level[0]):
        watergirl_victory = level[watergirl.rect.y // 32][watergirl.rect.x // 32] == "E"
    
    return fireboy_victory and watergirl_victory

# Lista de obstáculos (apenas um, perto do canto superior direito)
obstacles = [Obstacle(1150, 50)]  # Obstáculo azul na parte superior direita

# Loop principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Verifica eventos apenas para Watergirl
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Pula somente se estiver vivo
                watergirl.jump()

    # Controle do personagem Fireboy com W, A, S, D
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        fireboy.move(-fireboy.speed)
    if keys[pygame.K_d]:
        fireboy.move(fireboy.speed)
    if keys[pygame.K_w]:  # Usado para pular Fireboy
        fireboy.jump()

    # Controle do personagem Watergirl com setas
    if keys[pygame.K_LEFT]:
        watergirl.move(-watergirl.speed)
    if keys[pygame.K_RIGHT]:
        watergirl.move(watergirl.speed)

    # Atualiza o estado dos jogadores
    fireboy.update(obstacles)
    watergirl.update(obstacles)

    # Verifica vitória
    if check_victory(fireboy, watergirl, load_level()):
        print("Vitória!")
        running = False

    # Desenha tudo
    screen.fill(WHITE)
    draw_level(screen, load_level())
    for obstacle in obstacles:
        obstacle.draw(screen)  # Desenha obstáculos
    fireboy.draw(screen)
    watergirl.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # Limita a 60 quadros por segundo

pygame.quit()
