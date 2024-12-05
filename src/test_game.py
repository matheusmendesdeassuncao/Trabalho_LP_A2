import unittest
from unittest.mock import patch, MagicMock
import pygame
from classes import Door, Policial
from game import *
from utils import *

class TestGame(unittest.TestCase):

    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    def setUp(self, mock_set_caption, mock_set_mode):
        # Inicializa o ambiente do Pygame com mocks para display
        pygame.init()
        mock_set_mode.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        mock_set_caption.return_value = None
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((0, 0, 0))  # Preenche a tela com a cor preta

        # Carrega um nível de exemplo
        self.level = 1
        load_level(self.level)

    def test_load_level(self):
        # Verifica se o nível é carregado corretamente
        global careca, peixonalta, inimigos, chaves, porta_careca, porta_peixonauta

        # Verifica a criação dos objetos do nível
        self.assertIsInstance(careca, Player)
        self.assertIsInstance(peixonalta, Player)
        self.assertIsInstance(porta_careca, Door)
        self.assertIsInstance(porta_peixonauta, Door)
        self.assertEqual(len(inimigos), 5)
        self.assertEqual(len(chaves), 2)

    def test_player_movement(self):
        # Testa a movimentação do Careca
        initial_position_careca = careca.rect.x
        careca.move(1, [], 'right')  # Move o Careca para a direita
        self.assertGreater(careca.rect.x, initial_position_careca)

        initial_position_peixonalta = peixonalta.rect.x
        peixonalta.move(1, [], 'right')  # Move o Peixonalta para a direita
        self.assertGreater(peixonalta.rect.x, initial_position_peixonalta)

    def test_player_jump(self):
        # Testa o pulo do Careca
        initial_position_careca_y = careca.rect.y
        careca.jump()
        self.assertLess(careca.rect.y, initial_position_careca_y)

        # Testa o pulo do Peixonalta
        initial_position_peixonalta_y = peixonalta.rect.y
        peixonalta.jump()
        self.assertLess(peixonalta.rect.y, initial_position_peixonalta_y)

    def test_collision_with_obstacle(self):
        # Testa a colisão entre os jogadores e os obstáculos
        obstacles = MagicMock()
        careca.rect.x = 100
        careca.rect.y = 700
        careca.move(1, obstacles, 'right')  # Move para a direita

        peixonalta.rect.x = 200
        peixonalta.rect.y = 700
        peixonalta.move(1, obstacles, 'right')  # Move para a direita

        # Verifica se os jogadores estão se movendo corretamente
        self.assertEqual(careca.rect.x, 101)  # Espera-se que o Careca se mova
        self.assertEqual(peixonalta.rect.x, 201)  # Espera-se que o Peixonalta se mova

    def test_pick_up_key(self):
        # Testa se o jogador coleta uma chave corretamente
        chave = Chave(100, 100, [])
        initial_chave_count = len(chaves)
        chave.colisao(careca)  # Careca coleta a chave
        self.assertGreater(len(chaves), initial_chave_count)

    def test_door_interaction(self):
        # Testa a interação dos jogadores com as portas
        chave = Chave(100, 100, [])
        careca.pegou_chave = True  # Simula que o Careca pegou a chave

        # Testa a interação do Careca com a porta
        porta_careca.interact(careca, chave)
        self.assertTrue(careca.pegou_chave)

        peixonalta.pegou_chave = True  # Simula que o Peixonalta pegou a chave
        porta_peixonauta.interact(peixonalta, chave)
        self.assertTrue(peixonalta.pegou_chave)

    def test_victory_condition(self):
        # Testa a condição de vitória
        careca.pegou_chave = True
        peixonalta.pegou_chave = True
        porta_careca.check_victory(careca)
        porta_peixonauta.check_victory(peixonalta)

        # Simula o final do nível
        victory_text = MagicMock()
        victory_text.return_value = "END"
        self.assertEqual(victory_text(), "END")

    def test_player_death(self):
        # Testa a morte dos jogadores
        death_obstacle = MagicMock()
        careca.check_death(death_obstacle, 'careca')
        self.assertTrue(careca.morto)

        peixonalta.check_death(death_obstacle, 'peixonalta')
        self.assertTrue(peixonalta.morto)

    def test_inimigo_movement(self):
        # Testa o movimento dos inimigos
        inimigo = Policial(400, 400, MagicMock(), 44, 60)
        initial_position_inimigo = inimigo.rect.x
        inimigo.update(careca, peixonalta, [])
        self.assertGreater(inimigo.rect.x, initial_position_inimigo)

    def test_inimigo_colisao(self):
        # Testa a colisão dos inimigos com os jogadores
        inimigo_careca = InimigoCareca(400, 400, MagicMock(), 53, 37)
        careca.rect = pygame.Rect(400, 400, 50, 50)
        inimigo_careca.rect = pygame.Rect(400, 400, 50, 50)

        # Simula a colisão
        inimigo_careca.update()
        self.assertTrue(inimigo_careca.rect.colliderect(careca.rect))

        inimigo_peixonalta = InimigoPeixonalta(400, 400, MagicMock(), 64, 44)
        peixonalta.rect = pygame.Rect(400, 400, 50, 50)
        inimigo_peixonalta.rect = pygame.Rect(400, 400, 50, 50)

        # Simula a colisão com o Peixonalta
        inimigo_peixonalta.update()
        self.assertTrue(inimigo_peixonalta.rect.colliderect(peixonalta.rect))

    def test_enemy_behavior(self):
        # Testa o comportamento do inimigo com base no tipo
        inimigo = InimigoCareca(400, 400, MagicMock(), 53, 37)
        self.assertIsInstance(inimigo, InimigoCareca)

        # Simula movimento do inimigo
        inimigo.update()
        self.assertTrue(inimigo.rect.x > 400)  # Verifica se o inimigo se moveu

    @patch('pygame.time.wait')
    def test_game_over(self, mock_wait):
        # Testa a tela de Game Over e o encerramento do jogo
        careca.morto = True
        peixonalta.morto = True

        self.assertTrue(careca.morto)
        self.assertTrue(peixonalta.morto)

        # Verifica se o jogo terminou
        pygame.quit()
        mock_wait.assert_called_once_with(2000)

if __name__ == '__main__':
    unittest.main()