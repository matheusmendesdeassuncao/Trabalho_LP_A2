import pygame
from button import Button 
from display import Display

def main():
    pygame.init()

    #cria a tela
    screen = pygame.display.set_mode((800, 600)) 
    pygame.display.set_caption('A Fuga') 
    display = Display(screen)

    clock = pygame.time.Clock()

    while True:
    
        #verifica os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            display.handle_events(event)

        #atualiza a tela
        display.update_screen()
        pygame.display.update()
        clock.tick(60) 

if __name__ == "__main__":
    main()
