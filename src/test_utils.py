import unittest
from unittest.mock import patch, MagicMock
import pygame
import os
from utils import *

class TestGameFunctions(unittest.TestCase):

    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_load_image(self, mock_exists, mock_load):
        # Mock para simular a presença do arquivo de imagem
        mock_exists.return_value = True
        mock_load.return_value = MagicMock()

        # Testa se a função retorna a imagem carregada e redimensionada
        image = load_image(IMAGE_PATH, 'careca_final.png', 100, 100)
        self.assertIsNotNone(image)

        # Testa se a função retorna None para um caminho inexistente
        mock_exists.return_value = False
        image = load_image('dummy_path', 'dummy_image.png', 100, 100)
        self.assertIsNone(image)

    def test_draw_level(self):
        # Inicializa o Pygame e configura a tela
        pygame.init()
        screen = pygame.display.set_mode((1600, 900))

        # Testa a função draw_level com LEVEL1
        obstacles = draw_level(screen, LEVEL1)
        self.assertIsInstance(obstacles, list)
        self.assertTrue(all(isinstance(obstacle, Obstacle) for obstacle in obstacles))
        self.assertGreater(len(obstacles), 0)

        # Testa a função draw_level com LEVEL2
        obstacles = draw_level(screen, LEVEL2)
        self.assertIsInstance(obstacles, list)
        self.assertTrue(all(isinstance(obstacle, Obstacle) for obstacle in obstacles))
        self.assertGreater(len(obstacles), 0)

        pygame.quit()

if __name__ == '__main__':
    unittest.main()