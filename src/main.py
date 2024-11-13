import pygame
from button import Button 

def main():
    pygame.init()

    #cria a tela
    screen = pygame.display.set_mode((800, 600)) 
    pygame.display.set_caption('A Fuga') 

    clock = pygame.time.Clock()

    #criacao de botao de sair
    quit_button = Button(300, 250, 200, 50, text="Quit", color=(255, 255, 255), text_color=(0, 0, 0))

    while True:
        screen.fill((0, 0, 255)) 

        #verifica os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 

            #termina a execução se o botão for clicado
            if quit_button.is_clicked(event):
                pygame.quit()
                return
        
        #desenha o botao
        quit_button.draw(screen) 

        pygame.display.update()
        clock.tick(60) 

if __name__ == "__main__":
    main()
