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
CIAN = (0, 255, 255)
YELLOW = (255, 255, 0)

# Configuração da tela
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A fuga de Alexandre de Morais e Peixonalta de Bangu")

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
alexandre_de_morais_img = load_image(image_path, 'alexandre_de_morais.png', 64, 64)
peixonalta_img = load_image(image_path, 'peixonalta.png', 64, 64)

if alexandre_de_morais_img is None or peixonalta_img is None:
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

    def check_death(self, level, player_name):
        if 0 <= self.rect.y // 32 < len(level) and 0 <= self.rect.x // 32 < len(level[0]):
            tile = level[self.rect.y // 32][self.rect.x // 32]
            if tile == "T":
                return True  # T mata ambos os personagens
            elif tile == "U" and player_name == "alexandre_de_morais":
                return True  # U mata apenas Alexandre de Morais
            elif tile == "V" and player_name == "peixonalta":
                return True  # V mata apenas Peixonalta
        return False



# Inicialização dos personagens
alexandre_de_morais = Player(100, 600, alexandre_de_morais_img, 64, 64)
peixonalta = Player(200, 600, peixonalta_img, 64, 64)

def load_level():
    level = [
        "##################################################",
        "#     F                  U           E           #",
        "#                                                #",
        "#           #  #               #                 #",
        "#   ####       ######                 #####      #",
        "#        ######                      #     #     #",
        "#    #       V                       # U         #",
        "#           #     ########           #           #",
        "#           #    ##      ##        # #           #",
        "#   ###         ##        ##    ####             #",
        "#    T          #          #        ###          #",
        "#         #     #          #       #   #         #",
        "#        ###    #    #######       # T #         #",
        "#               ######             ###           #",
        "#             ##        #######     #            #",
        "#     ####    #          #         #   #####     #",
        "#     #       #       #######          #         #",
        "#     ####### #         #             ###   #    #",
        "#     #       #         #         ##          ## #",
        "#   ####       ###  #########     #             ##",
        "#   #          #       #          #   ##  ###    #",
        "#   ####   ##  #       ###    #   # V        ##  #",
        "#   #      #       ##      ##      ##     ##     #",
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
            elif char == "U":
                pygame.draw.rect(screen, CIAN, (x * 32, y * 32, 32, 32))
            elif char == "T":
                pygame.draw.rect(screen, GREEN, (x * 32, y * 32, 32, 32))
            elif char == "V":
                pygame.draw.rect(screen, YELLOW, (x * 32, y * 32, 32, 32))
    return obstacles

def check_victory(alexandre_de_morais, peixonalta, level):
    alexandre_de_morais_victory = level[alexandre_de_morais.rect.y // 32][alexandre_de_morais.rect.x // 32] == "F"
    peixonalta_victory = level[peixonalta.rect.y // 32][peixonalta.rect.x // 32] == "E"
    return alexandre_de_morais_victory and peixonalta_victory


running = True
clock = pygame.time.Clock()
level = load_level()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        alexandre_de_morais.move(-1)
    if keys[pygame.K_d]:
        alexandre_de_morais.move(1)
    if keys[pygame.K_w]:
        alexandre_de_morais.jump()
    if keys[pygame.K_LEFT]:
        peixonalta.move(-1)
    if keys[pygame.K_RIGHT]:
        peixonalta.move(1)
    if keys[pygame.K_UP]:
        peixonalta.jump()

    screen.fill(WHITE)
    obstacles = draw_level(screen, level)
    alexandre_de_morais.update(obstacles)
    peixonalta.update(obstacles)
    alexandre_de_morais.draw(screen)
    peixonalta.draw(screen)

    if check_victory(alexandre_de_morais, peixonalta, level):
        print("Vitória!")
        running = False
    else:
        if alexandre_de_morais.check_death(level, "alexandre_de_morais"):
            print("Alexandre de Morais morreu! kkkkkkkkkk")
            running = False
        if peixonalta.check_death(level, "peixonalta"):
            print("Peixonalta morreu! kkkkkkkkkk")
            running = False

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
