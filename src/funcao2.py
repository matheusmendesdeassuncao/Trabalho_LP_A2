import pygame
import os
# Inicializa o Pygame
pygame.init()
# Define as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Configuração da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fireboy & Watergirl")
# Função para carregar imagem
def load_image(image_path, file_name):
    full_path = os.path.join(image_path, file_name)
    if os.path.exists(full_path):
        return pygame.image.load(full_path).convert_alpha()
    else:
        print(f"Arquivo não encontrado: {full_path}")
        return None
# Atualiza o caminho para a pasta 'assets'
current_path = os.path.dirname(__file__)  # Local do arquivo
image_path = os.path.abspath(os.path.join(current_path, '..', 'assets'))  # Caminho para a pasta 'assets'
fireboy_img = load_image(image_path, 'helora.png')
watergirl_img = load_image(image_path, 'gabi.png')
if fireboy_img is None or watergirl_img is None:
    print("Erro: Imagem não encontrada.")
    pygame.quit()
    exit()
# Função para carregar e redimensionar imagem
def load_image(image_path, file_name, width, height):
    full_path = os.path.join(image_path, file_name)
    if os.path.exists(full_path):
        image = pygame.image.load(full_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    else:
        print(f"Arquivo não encontrado: {full_path}")
        return None
# Carrega e redimensiona as imagens dos personagens
fireboy_img = load_image(image_path, 'helora.png', 32, 32)
watergirl_img = load_image(image_path, 'gabi.png', 32, 32)
# Posições iniciais
fireboy_x, fireboy_y = 100, 100
watergirl_x, watergirl_y = 200, 100
# Função para carregar nível
def load_level():
    level = [
        "########################",
        "#   #       #     E    #",
        "#   #       #          #",
        "#   #######            #",
        "#           #####      #",
        "#  F ######            #",
        "#                      #",
        "########################"
    ]
    return level
# Função para desenhar o nível
def draw_level(screen, level):
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == "#":
                pygame.draw.rect(screen, BLACK, (x*32, y*32, 32, 32))
            elif char == "F":
                pygame.draw.rect(screen, RED, (x*32, y*32, 32, 32))
            elif char == "E":
                pygame.draw.rect(screen, BLUE, (x*32, y*32, 32, 32))
# Função para verificar colisão
def check_collision(x, y, level):
    grid_x = x // 32
    grid_y = y // 32
    if level[grid_y][grid_x] == "#":
        return True
    return False
# Função para verificar vitória
def check_victory(fireboy_x, fireboy_y, watergirl_x, watergirl_y, level):
    fireboy_victory = level[fireboy_y//32][fireboy_x//32] == "F"
    watergirl_victory = level[watergirl_y//32][watergirl_x//32] == "E"
    return fireboy_victory and watergirl_victory
# Loop do jogo
running = True
clock = pygame.time.Clock()
level = load_level()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Lógica do jogo
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if not check_collision(fireboy_x - 5, fireboy_y, level):
            fireboy_x -= 5
    if keys[pygame.K_d]:
        if not check_collision(fireboy_x + 5, fireboy_y, level):
            fireboy_x += 5
    if keys[pygame.K_w]:
        if not check_collision(fireboy_x, fireboy_y - 5, level):
            fireboy_y -= 5
    if keys[pygame.K_s]:
        if not check_collision(fireboy_x, fireboy_y + 5, level):
            fireboy_y += 5
    
    if keys[pygame.K_LEFT]:
        if not check_collision(watergirl_x - 5, watergirl_y, level):
            watergirl_x -= 5
    if keys[pygame.K_RIGHT]:
        if not check_collision(watergirl_x + 5, watergirl_y, level):
            watergirl_x += 5
    if keys[pygame.K_UP]:
        if not check_collision(watergirl_x, watergirl_y - 5, level):
            watergirl_y -= 5
    if keys[pygame.K_DOWN]:
        if not check_collision(watergirl_x, watergirl_y + 5, level):
            watergirl_y += 5
    
    # Verifica vitória
    if check_victory(fireboy_x, fireboy_y, watergirl_x, watergirl_y, level):
        print("Você venceu!")
        running = False
    
    # Atualização da tela
    screen.fill(WHITE)
    draw_level(screen, level)
    screen.blit(fireboy_img, (fireboy_x, fireboy_y))
    screen.blit(watergirl_img, (watergirl_x, watergirl_y))
    pygame.display.flip()
    
    clock.tick(60)
pygame.quit()