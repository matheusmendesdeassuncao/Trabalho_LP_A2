import pygame
import os
from classes import Obstacle, Player, Inimigo, InimigoPeixonalta, InimigoCareca, Chave

# Inicializa o Pygame
pygame.init()

# Define as cores utilizadas no jogo
# BLACK = (0, 0, 0)       # Cor para obstáculos
# WHITE = (255, 255, 255) # Cor de fundo
# RED = (255, 0, 0)       # Cor para o ponto de vitória de careca
# BLUE = (0, 0, 255)      # Cor para o ponto de vitória de Peixonalta
GREEN = (0, 255, 0)     # Cor para o obstáculo 'T'
CIAN = (0, 255, 255)    # Cor para o obstáculo 'U'
YELLOW = (255, 255, 0)  # Cor para o obstáculo 'V'

# Configuração da tela
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A fuga de careca e Peixonalta de Bangu")

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

# Carrega as imagens dos personagens e dos inimigos e das chaves
careca_img = load_image(image_path, 'players/careca_final.png', 64, 64)
peixonalta_img = load_image(image_path, 'players/peixonauta_final.png', 48, 32)
inimigo_img = load_image(image_path, 'enimies/inimigo.png', 424, 37)
inimigo_peixonalta_img = load_image(image_path, 'enimies/inimigo_peixonalta.png', 424, 37)
inimigo_careca_img = load_image(image_path, 'enimies/careca/cobra.png', 424, 37)

chave_sprites = []
for i in range(1, 9):
    chave_img = load_image(image_path, f'keys/key-{i}.png.png', 19, 37)  # Substitua pelo caminho correto
    chave_sprites.append(chave_img)

# Verifica se as imagens foram carregadas corretamente
if careca_img is None or peixonalta_img is None:
    print("Erro: Imagem não encontrada.")
    pygame.quit()
    exit()

fundo_img = load_image(image_path, 'playground/fundo.png', SCREEN_WIDTH, SCREEN_HEIGHT)
piso_img = load_image(image_path, 'playground/piso.png', 32, 32)
close_door_c = load_image(image_path, 'doors/porta_careca_close.png', 32, 64)
close_door_p = load_image(image_path, 'doors/porta_peixonauta_close.png', 32, 32)
sub_piso_img = load_image(image_path, 'playground/sub_piso.png', 32, 32)

# Inicialização dos personagens
careca = Player(100, 600, careca_img, 64, 64)
peixonalta = Player(200, 600, peixonalta_img, 64, 64)

# Inicializa os inimigos
inimigos = [
    Inimigo(1000, 250, inimigo_img, 64, 64),  # Inimigo genérico que persegue ambos os personagens
    InimigoPeixonalta(1400, 100, inimigo_peixonalta_img, 64, 64),  # Inimigo que persegue apenas Peixonalta
    InimigoCareca(800, 550, inimigo_careca_img, 64, 64)  # Inimigo que persegue apenas Careca
]
def load_level():
    """
    Função que define o layout do nível do jogo.

    Retorna:
        list: Uma lista de strings representando o mapa do jogo.
    """
    level = [
        "##################################################",
        "#                        U                       #",
        "#    F                                  E        #",
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
        "#   XX######   XXX   XXXXXXXX     ##            x#",
        "#   ########   #       ##             XX  XXX    #",
        "#   ########X                 X     V        XX  #",
        "#   #########     XXX      XXX#     X     XX     #",
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
    obstacles = []  # Inicializa uma lista para armazenar os obstáculos no nível
    for y, row in enumerate(level):  # Itera sobre as linhas do mapa (level)
        for x, char in enumerate(row):  # Itera sobre os caracteres de cada linha
            if char == "#":  # Verifica se o caractere é um obstáculo (representado por '#')
                #pygame.draw.rect(screen, BLACK, (x * 32, y * 32, 32, 32))  # Desenha o obstáculo na tela com a cor preta
                screen.blit(sub_piso_img, (x * 32, y * 32))
                obstacles.append(Obstacle(x * 32, y * 32))  # Adiciona o obstáculo à lista
            elif char == "X":
                screen.blit(piso_img, (x * 32, y * 32))
                obstacles.append(Obstacle(x * 32, y * 32))
            elif char == "F":  # Se o caractere for 'F', desenha o ponto de vitória para o Careca
                #pygame.draw.rect(screen, RED, (x * 32, y * 32, 32, 32))  # Desenha o ponto de vitória de Careca em vermelho
                screen.blit(close_door_c, (x * 32, y * 32))
            elif char == "E":  # Se o caractere for 'E', desenha o ponto de vitória para o Peixonalta
                #pygame.draw.rect(screen, BLUE, (x * 32, y * 32, 32, 32))  # Desenha o ponto de vitória de Peixonalta em azul
                screen.blit(close_door_p, (x * 32, y * 32))
            elif char == "U":  # Se o caractere for 'U', desenha o obstáculo do tipo 'U'
                pygame.draw.rect(screen, CIAN, (x * 32, y * 32, 32, 32))  # Desenha o obstáculo 'U' em ciano
            elif char == "T":  # Se o caractere for 'T', desenha o obstáculo do tipo 'T'
                pygame.draw.rect(screen, GREEN, (x * 32, y * 32, 32, 32))  # Desenha o obstáculo 'T' em verde
            elif char == "V":  # Se o caractere for 'V', desenha o obstáculo do tipo 'V'
                pygame.draw.rect(screen, YELLOW, (x * 32, y * 32, 32, 32))  # Desenha o obstáculo 'V' em amarelo

    return obstacles  # Retorna a lista de obstáculos desenhados

def check_victory(careca, peixonalta, level):
    """
    Função para verificar se os personagens alcançaram seus respectivos pontos de vitória.

    Parâmetros:
        careca (Player): O jogador 'careca'.
        peixonalta (Player): O jogador 'Peixonalta'.
        level (list): O mapa do nível do jogo.

    Retorna:
        bool: True se ambos os jogadores chegaram aos seus pontos de vitória, caso contrário, False.
    """
    careca_victory = level[careca.rect.y // 32][careca.rect.x // 32] == "F"
    peixonalta_victory = level[peixonalta.rect.y // 32][peixonalta.rect.x // 32] == "E"
    return careca_victory and peixonalta_victory

# Loop principal do jogo
running = True
clock = pygame.time.Clock()
level = load_level()

# Criar instâncias das chaves e definir suas posições no mapa
chave1 = Chave(295, 340, chave_sprites)  # Posição 1 da chave
chave2 = Chave(1125, 370, chave_sprites)  # Posição 2 da chave

# Adicionar as chaves ao jogo (presumindo que você tenha uma lista ou grupo de objetos 'chaves')
chaves = pygame.sprite.Group()  # Usando um grupo para gerenciar as chaves
chaves.add(chave1, chave2)  # Adicionando as chaves ao grupo

while running:  # Loop principal do jogo
    # Eventos do Pygame (ex: fechar a janela)
    for event in pygame.event.get():  # Verifica todos os eventos do Pygame
        if event.type == pygame.QUIT:  # Se o evento for o de fechar a janela
            running = False  # Interrompe o loop, fechando o jogo

    # Controles do jogador
    keys = pygame.key.get_pressed()  # Obtém o estado atual das teclas pressionadas
    if keys[pygame.K_a]:  # Se a tecla 'a' for pressionada
        careca.move(-1, obstacles)  # Move o Careca para a esquerda
    if keys[pygame.K_d]:  # Se a tecla 'd' for pressionada
        careca.move(1, obstacles)   # Move o Careca para a direita
    if keys[pygame.K_w]:  # Se a tecla 'w' for pressionada
        careca.jump()               # Faz o Careca pular
    if keys[pygame.K_LEFT]:  # Se a tecla de seta para a esquerda for pressionada
        peixonalta.move(-1, obstacles)  # Move o Peixonalta para a esquerda
    if keys[pygame.K_RIGHT]:  # Se a tecla de seta para a direita for pressionada
        peixonalta.move(1, obstacles)   # Move o Peixonalta para a direita
    if keys[pygame.K_UP]:  # Se a tecla de seta para cima for pressionada
        peixonalta.jump()             # Faz o Peixonalta pular

    # Atualiza a tela
    #screen.fill(fundo_img)  # Preenche a tela com a cor branca

    screen.blit(fundo_img, (0, 0))
    obstacles = draw_level(screen, level)  # Desenha o nível e obtém os obstáculos
    careca.update(obstacles)  # Atualiza o estado do Careca
    peixonalta.update(obstacles)  # Atualiza o estado do Peixonalta
    careca.draw(screen)  # Desenha o Careca na tela
    peixonalta.draw(screen)  # Desenha o Peixonalta na tela

    # Atualiza as chaves
    for chave in chaves:
        chave.colisao(careca)  # Verifica se o Careca pegou a chave
        chave.colisao(peixonalta)  # Verifica se o Peixonalta pegou a chave

    # Desenha as chaves no mapa
    #for chave in chaves:
    chaves.draw(screen)  # Desenha cada chave no mapa

    #for chave in chaves:
    chaves.update()

    # Verifica se ambos pegaram as chaves e se a vitória ocorreu
    if check_victory(careca, peixonalta, level) and peixonalta.pegou_chave and careca.pegou_chave:
        print("Vitória!")  # Mensagem de vitória
        running = False  # Encerra o jogo
    else:
        # Verifica se o Careca morreu
        if careca.check_death(level, "careca"):
            print("Careca morreu! kkkkkkkkkk")
            running = False  # Encerra o jogo

    # Verifica se algum jogador morreu
    if careca.check_death(level, "careca"):  # Se o Careca morreu
        print("Careca morreu! kkkkkkkkkk")
        running = False  # Encerra o jogo
    if peixonalta.check_death(level, "peixonalta"):  # Se o Peixonalta morreu
        print("Peixonalta morreu! kkkkkkkkkk")
        running = False  # Encerra o jogo

    # Atualiza e desenha inimigos
    for inimigo in inimigos:
        inimigo.update(careca, peixonalta, obstacles)  # Atualiza o inimigo
        inimigo.draw(screen)  # Desenha o inimigo na tela

        # Verifica colisão entre inimigos e personagens
        if isinstance(inimigo, InimigoCareca) and inimigo.rect.colliderect(careca.rect):  # Se o inimigo for InimigoCareca e colidir com o Careca
            print("Careca foi pego pela cobra")
            running = False  # Encerra o jogo
        elif isinstance(inimigo, InimigoPeixonalta) and inimigo.rect.colliderect(peixonalta.rect):  # Se o inimigo for InimigoPeixonalta e colidir com o Peixonalta
            print("Peixonalta foi pego pelo gato")
            running = False  # Encerra o jogo
        elif not isinstance(inimigo, (InimigoCareca, InimigoPeixonalta)):  # Para outros tipos de inimigos
            if inimigo.rect.colliderect(careca.rect):  # Se o inimigo colidir com o Careca
                print("Careca foi pego pelo guarda")
                running = False  # Encerra o jogo
            elif inimigo.rect.colliderect(peixonalta.rect):  # Se o inimigo colidir com o Peixonalta
                print("Peixonalta foi pego pelo guarda")
                running = False  # Encerra o jogo

    # Atualiza a tela a cada frame
    pygame.display.flip()  # Atualiza a tela com as novas informações
    clock.tick(60)  # Controla a taxa de quadros por segundo (FPS), limitando a 60 FPS
