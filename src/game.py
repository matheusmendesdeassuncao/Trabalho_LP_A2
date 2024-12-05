import pygame
from classes import Player, Door, Policial, InimigoPeixonalta, InimigoCareca, Chave
from utils import *
from menu import Display

def run_game():
    # Inicializa o Pygame
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
    display = Display(SCREEN)

    pygame.display.set_caption("A fuga de careca e Peixonalta de Bangu")

    # Loop principal do jogo
    running = True
    clock = pygame.time.Clock()

    # Carrega as imagens dos personagens e dos inimigos e das chaves
    careca_img = load_image(IMAGE_PATH, 'players/prision_careca.png', 187.5, 65)
    peixonalta_img = load_image(IMAGE_PATH, 'players/prision_peixonauta.png', 300, 40)
    inimigo_img = load_image(IMAGE_PATH, 'enemies/policial.png', 1452, 60)
    inimigo_peixonalta_img = load_image(IMAGE_PATH, 'enemies/gato.png', 256, 64)
    inimigo_careca_img = load_image(IMAGE_PATH, 'enemies/cobra.png', 424, 37)

    porta_careca_img = load_image(IMAGE_PATH, 'doors/porta_careca_opening.png', 396, 57)
    porta_peixonauta_img = load_image(IMAGE_PATH, 'doors/porta_peixonauta_opening.png', 572, 32)

    chave_sprites = []
    for i in range(1, 9):
        chave_img = load_image(IMAGE_PATH, f'keys/key-{i}.png.png', 19, 37)  # Substitua pelo caminho correto
        chave_sprites.append(chave_img)

    # Verifica se as imagens foram carregadas corretamente
    if careca_img is None or peixonalta_img is None:
        print("Erro: Imagem não encontrada.")
        pygame.quit()
        exit()

    atual_index = 0

    def load_level(num):
        global inimigos, porta_careca, porta_peixonauta, chaves, careca, peixonalta

        if num == 1:
            # Inicializa as portas
            porta_careca = Door(160, 135, porta_careca_img, 64, 64, 11)
            porta_peixonauta = Door(225, 135, porta_peixonauta_img, 64, 64, 11)

            careca = Player(100, 700, careca_img, 31.25, 65)
            peixonalta = Player(200, 700, peixonalta_img, 50, 40)

            # Inicializa os inimigos
            inimigos = [
                InimigoCareca(350, 667, inimigo_careca_img, 53, 37),  # Inimigo que persegue apenas Careca
                InimigoCareca(900, 762, inimigo_careca_img, 53, 37),
                InimigoPeixonalta(350, 736, inimigo_peixonalta_img, 64, 44),  # Inimigo que persegue apenas Peixonalta
                InimigoPeixonalta(900, 640, inimigo_peixonalta_img, 64, 44),
                Policial(80, 250, inimigo_img, 44, 60)
            ]

            # Criar instâncias das chaves e definir suas posições no mapa
            chave1 = Chave(760, 70, chave_sprites)
            chave2 = Chave(810, 70, chave_sprites)
            chaves = pygame.sprite.Group(chave1, chave2)

        if num == 2:
            # Inicializa as portas
            porta_careca = Door(500, 232, porta_careca_img, 64, 64, 11)
            porta_peixonauta = Door(900, 230, porta_peixonauta_img, 64, 64, 11)

            careca = Player(100, 100, careca_img, 31.25, 65)
            peixonalta = Player(200, 100, peixonalta_img, 50, 40)

            # Inicializa os inimigos (modifique conforme a estrutura do seu nível)
            inimigos = [
                InimigoCareca(600, 90, inimigo_careca_img, 53, 37),  # Inimigo que persegue apenas Careca
                InimigoCareca(900, 634, inimigo_careca_img, 53, 37),
                InimigoPeixonalta(220, 580, inimigo_peixonalta_img, 64, 44),  # Inimigo que persegue apenas Peixonalta
                InimigoPeixonalta(600, 735, inimigo_peixonalta_img, 64, 44),
                Policial(1350, 720, inimigo_img, 44, 60)
            ]

            # Inicializa as chaves (substitua conforme o layout do nível)
            chave1 = Chave(370, 720, chave_sprites)
            chave2 = Chave(806, 700, chave_sprites)
            chaves = pygame.sprite.Group(chave1, chave2)
        
    font = pygame.font.SysFont(None, 55)

    def victory():
        text = font.render("END", True, GREEN)
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    num = 1
    load_level(num)

    while running:  # Loop principal do jogo
        # Eventos do Pygame (ex: fechar a janela)
        for event in pygame.event.get():  # Verifica todos os eventos do Pygame
            if event.type == pygame.QUIT:  # Se o evento for o de fechar a janela
                pygame.quit()
                #running = False  # Interrompe o loop, fechando o jogo
            display.handle_events(event)

        SCREEN.blit(fundo_img, (0, 0)) # Desenha a tela de fundo

        obstacles = draw_level(SCREEN, levels[atual_index]) # Desenha o nível e obtém os obstáculos

        porta_careca.draw(SCREEN)
        porta_peixonauta.draw(SCREEN)

        careca.update(obstacles)  # Atualiza o estado do Careca
        peixonalta.update(obstacles)  # Atualiza o estado do Peixonalta
        careca.draw(SCREEN)  # Desenha o Careca na tela
        peixonalta.draw(SCREEN)  # Desenha o Peixonalta na tela

        # Controles do jogador
        keys = pygame.key.get_pressed()  # Obtém o estado atual das teclas pressionadas
        if keys[pygame.K_a]:  # Se a tecla 'a' for pressionada
            careca.move(-1, obstacles, "left")  # Move o Careca para a esquerda
        if keys[pygame.K_d]:  # Se a tecla 'd' for pressionada
            careca.move(1, obstacles, "rigth")   # Move o Careca para a direita
        if keys[pygame.K_w]:  # Se a tecla 'w' for pressionada
            careca.jump()  # Faz o Careca pular
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            careca.move(0, obstacles, "idle")

        if keys[pygame.K_LEFT]:  # Se a tecla de seta para a esquerda for pressionada
            peixonalta.move(-1, obstacles, "left")  # Move o Peixonalta para a esquerda
        if keys[pygame.K_RIGHT]:  # Se a tecla de seta para a direita for pressionada
            peixonalta.move(1, obstacles, "rigth")   # Move o Peixonalta para a direita
        if keys[pygame.K_UP]:  # Se a tecla de seta para cima for pressionada
            peixonalta.jump()  # Faz o Peixonalta pular
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            peixonalta.move(0, obstacles, "idle")

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
                atual_index += 1
                if atual_index < len(levels):  # Verifica se há mais níveis
                    num += 1
                    load_level(num)
                else:
                    victory()  # Exibe a mensagem de fim de jogo
                    pygame.display.flip()  # Atualiza a tela
                    pygame.time.wait(2000)  # Espera 2 segundos para fechar o jogo
                    running = False

        # Verifica se algum jogador morreu
        if careca.check_death(levels[atual_index], "careca"):  # Se o Careca morreu
            print("Careca morreu! kkkkkkkkkk")
            running = False  # Encerra o jogo
        if peixonalta.check_death(levels[atual_index], "peixonalta"):  # Se o Peixonalta morreu
            print("Peixonalta morreu! kkkkkkkkkk")
            running = False  # Encerra o jogo

        # Atualiza e desenha inimigos
        for inimigo in inimigos:
            if type(inimigo) == Policial:
                inimigo.update(careca, peixonalta, obstacles)  # Atualiza o inimigo
            else:
                inimigo.update()
            
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
        display.update_screen()
        pygame.display.flip()  # Atualiza a tela com as novas informações
        pygame.display.update()
        clock.tick(60)  # Controla a taxa de quadros por segundo (FPS), limitando a 60 FPS
    
    pygame.quit()