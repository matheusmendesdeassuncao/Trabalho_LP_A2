import pygame
from classes import Player, Door, Policial, InimigoPeixonalta, InimigoCareca, Chave
from utils import *

# Inicializa o Pygame
pygame.init()

pygame.display.set_caption("A fuga de careca e Peixonalta de Bangu")

door_opening_width = 0

# Carrega as imagens dos personagens e dos inimigos e das chaves
careca_img = load_image(IMAGE_PATH, 'players/careca_final.png', 64, 64)
peixonalta_img = load_image(IMAGE_PATH, 'players/peixonauta_final.png', 48, 32)
inimigo_img = load_image(IMAGE_PATH, 'enemies/idle_policial.png', 196, 70)
inimigo_peixonalta_img = load_image(IMAGE_PATH, 'enemies/gato.png', 256, 64)
inimigo_careca_img = load_image(IMAGE_PATH, 'enemies/cobra.png', 424, 37)

porta_careca_img = load_image(IMAGE_PATH, 'doors/porta_careca_opening.png', 396, 57)
porta_peixonauta_img = load_image(IMAGE_PATH, 'doors/porta_peixonauta_opening.png', 572, 32)

chave_sprites = []
for i in range(1, 9):
    chave_img = load_image(IMAGE_PATH, f'keys/key-{i}.png.png', 19, 37)  # Substitua pelo caminho correto
    chave_sprites.append(chave_img)

porta_careca = Door(160, 70, porta_careca_img, 64, 64, 11)
porta_peixonauta = Door(1260, 70, porta_peixonauta_img, 64, 64, 11)

# Verifica se as imagens foram carregadas corretamente
if careca_img is None or peixonalta_img is None:
    print("Erro: Imagem não encontrada.")
    pygame.quit()
    exit()

# Inicialização dos personagens
careca = Player(100, 600, careca_img, 64, 64)
peixonalta = Player(200, 600, peixonalta_img, 64, 64)

# Inicializa os inimigos
inimigos = [
    InimigoCareca(800, 630, inimigo_careca_img, 64, 64),  # Inimigo que persegue apenas Careca
    InimigoPeixonalta(1700, 500, inimigo_peixonalta_img, 64, 64),  # Inimigo que persegue apenas Peixonalta
    Policial(1000, 250, inimigo_img, 64, 64)  # Inimigo genérico que persegue ambos os personagens
]

# Loop principal do jogo
running = True
clock = pygame.time.Clock()

# Criar instâncias das chaves e definir suas posições no mapa
chave1 = Chave(295, 340, chave_sprites)  # Posição 1 da chave
chave2 = Chave(1125, 370, chave_sprites)  # Posição 2 da chave

# Adicionar as chaves ao jogo (presumindo que você tenha uma lista ou grupo de objetos 'chaves')
chaves = pygame.sprite.Group()  # Usando um grupo para gerenciar as chaves
chaves.add(chave1, chave2)  # Adicionando as chaves ao grupo

font = pygame.font.SysFont(None, 55)

def victory():
    text = font.render("END", True, GREEN)
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

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

    SCREEN.blit(fundo_img, (0, 0)) # Desenha a tela de fundo

    porta_careca.draw(SCREEN)
    porta_peixonauta.draw(SCREEN)

    obstacles = draw_level(SCREEN, LEVEL)  # Desenha o nível e obtém os obstáculos
    careca.update(obstacles)  # Atualiza o estado do Careca
    peixonalta.update(obstacles)  # Atualiza o estado do Peixonalta
    careca.draw(SCREEN)  # Desenha o Careca na tela
    peixonalta.draw(SCREEN)  # Desenha o Peixonalta na tela

    # Atualiza as chaves
    for chave in chaves:
        chave.colisao(careca)  # Verifica se o Careca pegou a chave
        chave.colisao(peixonalta)  # Verifica se o Peixonalta pegou a chave
        porta_careca.interact(careca, chave)
        porta_peixonauta.interact(peixonalta, chave)

    porta_careca.animate()
    porta_peixonauta.animate()
    
    # Desenha as chaves no mapa
    chaves.draw(SCREEN)  # Desenha cada chave no mapa
    chaves.update()

    if porta_careca.check_victory(careca) and careca.pegou_chave:
        if porta_peixonauta.check_victory(peixonalta) and peixonalta.pegou_chave:
            victory()  # Exibe a mensagem de fim de jogo
            pygame.display.flip()  # Atualiza a tela
            pygame.time.wait(2000)  # Espera 2 segundos para fechar o jogo
            running = False

    # Verifica se algum jogador morreu
    if careca.check_death(LEVEL, "careca"):  # Se o Careca morreu
        print("Careca morreu! kkkkkkkkkk")
        running = False  # Encerra o jogo
    if peixonalta.check_death(LEVEL, "peixonalta"):  # Se o Peixonalta morreu
        print("Peixonalta morreu! kkkkkkkkkk")
        running = False  # Encerra o jogo

    # Atualiza e desenha inimigos
    for inimigo in inimigos:
        inimigo.update(careca, peixonalta, obstacles)  # Atualiza o inimigo
        inimigo.draw(SCREEN)  # Desenha o inimigo na tela

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
