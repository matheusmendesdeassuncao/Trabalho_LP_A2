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
pygame.display.set_caption("As Aventuras de Helora e Gabrela")

# Função para carregar e redimensionar imagem
def load_image(image_path, file_name, width, height):
    full_path = os.path.join(image_path, file_name)
    if os.path.exists(full_path):
        image = pygame.image.load(full_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    else:
        print(f"Arquivo não encontrado: {full_path}")
        return None

current_path = os.path.dirname(__file__)
image_path = os.path.abspath(os.path.join(current_path, '..', 'assets'))
louriskelly_img = load_image(image_path, 'helora.png', 64, 64)
gabikkk_img = load_image(image_path, 'gabi.png', 64, 64)

if louriskelly_img is None or gabikkk_img is None:
    print("Erro: Imagem não encontrada.")
    pygame.quit()
    exit()

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, BLACK, self.rect)

class Player:
    def __init__(self, x: int, y: int, image, width: int = 64, height: int = 64):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.vel_y = 0
        self.gravity = 0.5
        self.is_jumping = False
        self.is_alive = True
        self.speed = 5
        self.direction = pygame.Vector2(0, 0)

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -15
            self.is_jumping = True

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def horizontal_movement_collision(self, obstacles):
        self.rect.x += self.direction.x * self.speed
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.direction.x < 0:
                    self.rect.left = obstacle.rect.right
                elif self.direction.x > 0:
                    self.rect.right = obstacle.rect.left

    def vertical_movement_collision(self, obstacles):
        self.apply_gravity()
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel_y > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.is_jumping = False
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.vel_y = 0

    def move(self, dx):
        self.direction.x = dx
        self.horizontal_movement_collision(obstacles)

    def update(self, obstacles):
        if self.is_alive:
            self.vertical_movement_collision(obstacles)

    def draw(self, screen: pygame.Surface):
        if self.is_alive:
            screen.blit(self.image, self.rect.topleft)

    def check_death(self, level):
        if 0 <= self.rect.y // 32 < len(level) and 0 <= self.rect.x // 32 < len(level[0]):
            return level[self.rect.y // 32][self.rect.x // 32] == "T"
        return False

# Inicialização dos personagens
louriskelly = Player(100, 600, louriskelly_img, 64, 64)
gabikkk = Player(200, 600, gabikkk_img, 64, 64)

def load_level():
    level = [
        "##################################################",
        "#     F                                     E    #",
        "#                T             T                 #",
        "#    # # #                                       #",
        "#        # ##                        #############",
        "#           #                      # #           #",
        "#           #                     #  #           #",
        "#           ##########        ####   #           #",
        "#                      #             #           #",
        "#        #            #  #           #           #",
        "#        #            #              #           #",
        "#        #            #              #           #",
        "#        #            ##   ######### #           #",
        "#        #            #              #           #",
        "#        #            #              #           #",
        "#        #   #        #              #           #",
        "#        #   #        ###########   ##           #",
        "#        #   #        #              #           #",
        "#        #   ##########              #           #",
        "#           #                #########           #",
        "#                           #        #           #",
        "#                        # #   #     #           #",
        "#                        #     #     #           #",
        "##################################################"
    ]
    return level

def draw_level(screen, level):
    obstacles = []
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == "#":
                pygame.draw.rect(screen, BLACK, (x * 32, y * 32, 32, 32))
                obstacles.append(Obstacle(x * 32, y * 32))
            elif char == "F":
                pygame.draw.rect(screen, RED, (x * 32, y * 32, 32, 32))
            elif char == "E":
                pygame.draw.rect(screen, BLUE, (x * 32, y * 32, 32, 32))
            elif char == "T":
                pygame.draw.rect(screen, GREEN, (x * 32, y * 32, 32, 32))
    return obstacles

def check_victory(louriskelly, gabikkk, level):
    fireboy_victory = level[louriskelly.rect.y // 32][louriskelly.rect.x // 32] == "F"
    watergirl_victory = level[gabikkk.rect.y // 32][gabikkk.rect.x // 32] == "E"
    victory = fireboy_victory and watergirl_victory
    return fireboy_victory and watergirl_victory


running = True
clock = pygame.time.Clock()
level = load_level()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        louriskelly.move(-1)
    if keys[pygame.K_d]:
        louriskelly.move(1)
    if keys[pygame.K_w]:
        louriskelly.jump()
    if keys[pygame.K_LEFT]:
        gabikkk.move(-1)
    if keys[pygame.K_RIGHT]:
        gabikkk.move(1)
    if keys[pygame.K_UP]:
        gabikkk.jump()

    screen.fill(WHITE)
    obstacles = draw_level(screen, level)
    louriskelly.update(obstacles)
    gabikkk.update(obstacles)
    louriskelly.draw(screen)
    gabikkk.draw(screen)

    #victory, fireboy_victory, watergirl_victory = check_victory(louriskelly, gabikkk, level)
    if check_victory(louriskelly, gabikkk, level):
        print("Vitória!")
        running = False
    else:
        if louriskelly.check_death(level):
            print("LourisKelly morreu!")
            running = False
        if gabikkk.check_death(level):
            print("Gabikkkk morreu!")
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
