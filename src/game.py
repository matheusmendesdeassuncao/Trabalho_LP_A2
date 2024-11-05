import pygame
import os
from classes import Obstacle, Player 

# Inicializa o Pygame
pygame.init()

# Define as cores utilizadas no jogo
BLACK = (0, 0, 0)      # Cor para obstáculos
WHITE = (255, 255, 255) # Cor de fundo
RED = (255, 0, 0)      # Cor para o ponto de vitória de Alexandre de Morais
BLUE = (0, 0, 255)     # Cor para o ponto de vitória de Peixonalta
GREEN = (0, 255, 0)    # Cor para o obstáculo 'T'
CIAN = (0, 255, 255)   # Cor para o obstáculo 'U'
YELLOW = (255, 255, 0) # Cor para o obstáculo 'V'

# Configuração da tela
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A fuga de Alexandre de Morais e Peixonalta de Bangu")

def load_image(image_path, file_name, width, height):
    """
    Função para carregar uma imagem, redimensioná-la e retornar a imagem.

    Parâmetros:
        image_path (str): Caminho da pasta onde a imagem está localizada.
        file_name (str): Nome do arquivo da imagem.
        width (int): Largura desejada para a imagem.
        height (int): Altura desejada para a imagem.

    Retorna:
        pygame.Surface: A imagem carregada e redimensionada, ou None se não encontrada.
    """
    full_path = os.path.join(image_path, file_name)
    if os.path.exists(full_path):
        image = pygame.image.load(full_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    else:
        print(f"Arquivo não encontrado: {full_path}")
        return None

# Caminho relativo para as imagens dos personagens
current_path = os.path.dirname(__file__)
image_path = os.path.abspath(os.path.join(current_path, '..', 'assets'))

# Carrega as imagens dos personagens
alexandre_de_morais_img = load_image(image_path, 'alexandre_de_morais.png', 64, 64)
peixonalta_img = load_image(image_path, 'peixonalta.png', 64, 64)

# Verifica se as imagens foram carregadas corretamente
if alexandre_de_morais_img is None or peixonalta_img is None:
    print("Erro: Imagem não encontrada.")
    pygame.quit()
    exit()

# Inicialização dos personagens
alexandre_de_morais = Player(100, 600, alexandre_de_morais_img, 64, 64)
peixonalta = Player(200, 600, peixonalta_img, 64, 64)

def load_level():
    """
    Função que define o layout do nível do jogo.

    Retorna:
        list: Uma lista de strings representando o mapa do jogo.
    """
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
    """
    Função para desenhar o nível na tela com base no layout definido.

    Parâmetros:
        screen (pygame.Surface): A superfície onde o jogo será desenhado.
        level (list): O mapa do nível a ser desenhado.

    Retorna:
        list: Uma lista de obstáculos do nível.
    """
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
    """
    Função para verificar se os personagens alcançaram seus respectivos pontos de vitória.

    Parâmetros:
        alexandre_de_morais (Player): O jogador 'Alexandre de Morais'.
        peixonalta (Player): O jogador 'Peixonalta'.
        level (list): O mapa do nível do jogo.

    Retorna:
        bool: True se ambos os jogadores chegaram aos seus pontos de vitória, caso contrário, False.
    """
    alexandre_de_morais_victory = level[alexandre_de_morais.rect.y // 32][alexandre_de_morais.rect.x // 32] == "F"
    peixonalta_victory = level[peixonalta.rect.y // 32][peixonalta.rect.x // 32] == "E"
    return alexandre_de_morais_victory and peixonalta_victory

# Loop principal do jogo
running = True
clock = pygame.time.Clock()
level = load_level()

while running:
    # Eventos do Pygame (ex: fechar a janela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controles do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        alexandre_de_morais.move(-1, obstacles)  # Movimento para a esquerda
    if keys[pygame.K_d]:
        alexandre_de_morais.move(1, obstacles)   # Movimento para a direita
    if keys[pygame.K_w]:
        alexandre_de_morais.jump()               # Pulo de Alexandre de Morais
    if keys[pygame.K_LEFT]:
        peixonalta.move(-1, obstacles)           # Movimento para a esquerda
    if keys[pygame.K_RIGHT]:
        peixonalta.move(1, obstacles)            # Movimento para a direita
    if keys[pygame.K_UP]:
        peixonalta.jump()                        # Pulo de Peixonalta

    # Atualiza a tela
    screen.fill(WHITE)
    obstacles = draw_level(screen, level)
    alexandre_de_morais.update(obstacles)
    peixonalta.update(obstacles)
    alexandre_de_morais.draw(screen)
    peixonalta.draw(screen)

    # Verifica vitória ou morte
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

    # Atualiza a tela a cada frame
    pygame.display.flip()
    clock.tick(60)
