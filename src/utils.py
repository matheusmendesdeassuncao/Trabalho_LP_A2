import pygame
import os
from classes import Obstacle

pygame.init()

# Define as cores utilizadas no jogo
GREEN = (0, 255, 0)     # Cor para o obstáculo 'T'
CIAN = (0, 255, 255)    # Cor para o obstáculo 'U'
YELLOW = (255, 255, 0)  # Cor para o obstáculo 'V'

# Configuração da tela
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 750

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Caminho relativo para as imagens
CURRENT_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.abspath(os.path.join(CURRENT_PATH, '..', 'assets'))

door_opening_width = 0

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

# Define o layout do nível do jogo.
LEVEL = [
    "##################################################",
    "#                        U                       #",
    "#                                       E        #",
    "#          X    X                                #",
    "#  XXXXX       X#XXXX                 XXXXX      #",
    "#        XXXXXX                      X           #",
    "#            V                       # U         #",
    "#                 XXXXXXXX           #           #",
    "#           X    X########X         X            #",
    "#   XXX          ##########X                     #",
    "#    T          X###########        XXX          #",
    "#         X     ############           X         #",
    "#        X#X    ############         T #         #",
    "#               ############       X             #",
    "#                                  #             #",
    "#     XXXXX                        #   XXXXXXX   #",
    "#     #####   X                        #####     #",
    "#     #####X  #                       X#####     #",
    "#     ######  #                   XX          XX #",
    "#   XX######   XXX   XXXXXXX      ##            x#",
    "#   ########   #       ##             XX  XXX    #",
    "#   ########X                 X     V        XX  #",
    "#   #########     XXX      XXX#     X     XX     #",
    "##################################################"
]

fundo_img = load_image(IMAGE_PATH, 'playground/fundo.png', SCREEN_WIDTH, SCREEN_HEIGHT)
piso_img = load_image(IMAGE_PATH, 'playground/piso.png', 32, 32)
sub_piso_img = load_image(IMAGE_PATH, 'playground/sub_piso.png', 32, 32)

def draw_level(screen, level):
    """
    Função para desenhar o nível na tela com base no layout definido.

    Parâmetros:
        screen (pygame.Surface): A superfície onde o jogo será desenhado.
        level (list): O mapa do nível a ser desenhado.

    Retorna:
        list: Uma lista de obstáculos do nível.
    """
    obstacles = []  # Inicializa uma lista para armazenar os obstáculos no nível
    for y, row in enumerate(level):  # Itera sobre as linhas do mapa (level)
        for x, char in enumerate(row):  # Itera sobre os caracteres de cada linha
            if char == "#":  # Se o carectere for '#', desenha o piso interno
                screen.blit(sub_piso_img, (x * 32, y * 32))
                obstacles.append(Obstacle(x * 32, y * 32)) 
            elif char == "X": # Se o carectere for 'X', desenha o piso externo
                screen.blit(piso_img, (x * 32, y * 32)) 
                obstacles.append(Obstacle(x * 32, y * 32))
            elif char == "U":  # Se o caractere for 'U', desenha o obstáculo do tipo 'U'
                pygame.draw.rect(screen, CIAN, (x * 32, y * 32, 32, 32))  # Desenha o obstáculo 'U' em ciano
            elif char == "T":  # Se o caractere for 'T', desenha o obstáculo do tipo 'T'
                pygame.draw.rect(screen, GREEN, (x * 32, y * 32, 32, 32))  # Desenha o obstáculo 'T' em verde
            elif char == "V":  # Se o caractere for 'V', desenha o obstáculo do tipo 'V'
                pygame.draw.rect(screen, YELLOW, (x * 32, y * 32, 32, 32))  # Desenha o obstáculo 'V' em amarelo

    return obstacles  # Retorna a lista de obstáculos desenhados