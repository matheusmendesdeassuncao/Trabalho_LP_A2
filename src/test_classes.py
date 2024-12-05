import unittest
from unittest.mock import Mock
import pygame
from classes import animar, carregar_sprites, Obstacle, Door, Player, Policial, Inimigo, InimigoCareca, Chave

class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_animar(self):
        frames = [Mock(), Mock(), Mock()]
        index, fps, frame_time = 0, 10, 0

        for i in range(15):
            frame, index, frame_time = animar(frames, index, fps, frame_time)
            self.assertEqual(frame, frames[i % len(frames)])
            if i < fps:
                self.assertEqual(frame_time, i + 1)
            else:
                self.assertEqual(frame_time, 0)

    def test_carregar_sprites(self):
        image = Mock()
        image.get_width.return_value = 300
        image.get_height.return_value = 100
        num_frames, frame_width, frame_height = 5, 60, 100

        frames = carregar_sprites(image, num_frames, frame_width, frame_height)
        self.assertEqual(len(frames), num_frames)
        for i in range(num_frames):
            x = i * frame_width
            image.subsurface.assert_any_call((x, 0, frame_width, frame_height))

    def test_obstacle(self):
        x, y = 100, 150
        obstacle = Obstacle(x, y)
        self.assertEqual(obstacle.rect.topleft, (x, y))
        self.assertEqual(obstacle.rect.size, (32, 32))

    def test_door_init(self):
        x, y, width, height, max_frames = 100, 200, 64, 128, 10
        image = Mock()
        image.get_width.return_value = 640
        image.get_height.return_value = 128

        door = Door(x, y, image, width, height, max_frames)
        self.assertEqual(door.rect.topleft, (x, y))
        self.assertEqual(len(door.door_frames), max_frames)
        for i in range(max_frames):
            frame_width = image.get_width() // max_frames
            image.subsurface.assert_any_call(i * frame_width, 0, frame_width, image.get_height())

    def test_door_interact(self):
        x, y, width, height, max_frames = 100, 200, 64, 128, 10
        image = Mock()
        player = Mock()
        player.pegou_chave = True

        door = Door(x, y, image, width, height, max_frames)
        door.interact(player, True)
        self.assertTrue(door.opening)

    def test_door_check_victory(self):
        x, y, width, height, max_frames = 100, 200, 64, 128, 10
        image = Mock()
        player = Mock()
        player.rect.centerx = x + width // 2
        player.rect.centery = y + height // 2

        door = Door(x, y, image, width, height, max_frames)
        self.assertTrue(door.check_victory(player))

class TestPlayer(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.image = Mock()
        self.obstacles = [Mock()]
        self.player = Player(100, 100, self.image, 64, 64)

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.player.rect.topleft, (100, 100))
        self.assertEqual(self.player.rect.size, (64, 78))
        self.assertFalse(self.player.is_jumping)
        self.assertTrue(self.player.is_alive)
        self.assertEqual(self.player.direction, pygame.Vector2(0, 0))
        self.assertFalse(self.player.pegou_chave)

    def test_jump(self):
        self.player.jump()
        self.assertTrue(self.player.is_jumping)
        self.assertEqual(self.player.vel_y, -12)

    def test_apply_gravity(self):
        initial_y = self.player.rect.y
        self.player.apply_gravity()
        self.assertEqual(self.player.vel_y, 0.5)
        self.assertEqual(self.player.rect.y, initial_y + 0.5)

    def test_move(self):
        initial_x = self.player.rect.x
        self.player.move(1, self.obstacles, "rigth")
        self.assertEqual(self.player.rect.x, initial_x + self.player.speed)

    def test_update(self):
        initial_y = self.player.rect.y
        self.player.update(self.obstacles)
        self.assertGreater(self.player.rect.y, initial_y)  # Deve ter aplicado a gravidade

    def test_draw(self):
        self.player.draw(self.screen)
        self.assertTrue(self.player.is_alive)

    def test_check_death(self):
        level = [
            "########################",
            "#                      #",
            "#           T          #",
            "#                      #",
            "########################"
        ]
        self.player.rect.topleft = (64, 64)  # Posição na linha do obstáculo 'T'
        self.assertTrue(self.player.check_death(level, "peixonalta"))

        self.player.rect.topleft = (32, 32)  # Posição fora do obstáculo
        self.assertFalse(self.player.check_death(level, "peixonalta"))

class TestInimigo(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.image = Mock()
        self.obstacles = [Mock()]
        self.careca = Mock()
        self.peixonalta = Mock()
        self.inimigo = Inimigo(100, 100, self.image, 64, 64)

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.inimigo.rect.topleft, (100, 100))
        self.assertEqual(self.inimigo.rect.size, (64, 64))
        self.assertFalse(self.inimigo.no_chao)

    def test_move(self):
        initial_x = self.inimigo.rect.x
        self.inimigo.pode_mover = True
        self.inimigo.speed = 5
        self.inimigo.move(self.obstacles)
        self.assertEqual(self.inimigo.rect.x, initial_x + 5)

    def test_gravidade(self):
        initial_y = self.inimigo.rect.y
        self.inimigo.gravidade(self.obstacles)
        self.assertGreater(self.inimigo.rect.y, initial_y)

    def test_pular(self):
        self.inimigo.no_chao = True
        self.inimigo.pular()
        self.assertEqual(self.inimigo.velocidade_y, self.inimigo.salto)

    def test_verificar_morte(self):
        self.inimigo.rect.colliderect.return_value = True
        self.inimigo.verificar_morte(self.careca, self.peixonalta)
        self.careca.morrer.assert_called_once()

class TestPolicial(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.image = Mock()
        self.obstacles = [Mock()]
        self.careca = Mock()
        self.peixonalta = Mock()
        self.policial = Policial(100, 100, self.image, 44, 60)

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.policial.rect.topleft, (100, 100))
        self.assertEqual(self.policial.rect.size, (44, 60))
        self.assertEqual(self.policial.estado, 'idle')

    def test_update(self):
        self.careca.rect.x = 150
        self.careca.rect.y = 100
        self.policial.update(self.careca, self.peixonalta, self.obstacles)
        self.assertEqual(self.policial.estado, 'running')

    def test_verificar_morte(self):
        self.policial.rect.colliderect.return_value = True
        self.policial.verificar_morte(self.careca, self.peixonalta)
        self.careca.morrer.assert_called_once()

class TestInimigoCareca(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.image = Mock()
        self.inimigo_careca = InimigoCareca(100, 100, self.image, 53, 37)

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.inimigo_careca.rect.topleft, (100, 100))
        self.assertEqual(self.inimigo_careca.rect.size, (53, 37))
        self.assertEqual(self.inimigo_careca.direction, 1)

    def test_update(self):
        initial_x = self.inimigo_careca.rect.x
        self.inimigo_careca.update()
        self.assertNotEqual(self.inimigo_careca.rect.x, initial_x)

    def test_verificar_morte(self):
        self.inimigo_careca.rect.colliderect.return_value = True
        self.careca = Mock()
        self.inimigo_careca.verificar_morte(self.careca)
        self.careca.morrer.assert_called_once()

class TestChave(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.sprites = [Mock(), Mock(), Mock()]
        self.chave = Chave(100, 150, self.sprites)
        self.player = Mock()
        self.player.rect = pygame.Rect(100, 150, 64, 64)
        self.player.pegou_chave = False

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.chave.rect.topleft, (100, 150))
        self.assertEqual(self.chave.rect.size, self.sprites[0].get_rect().size)
        self.assertFalse(self.chave.pegada)

    def test_update(self):
        initial_frame = self.chave.atual
        self.chave.update()
        self.assertNotEqual(self.chave.atual, initial_frame)

    def test_colisao(self):
        self.chave.colisao(self.player)
        self.assertTrue(self.player.pegou_chave)
        self.assertFalse(self.chave.alive())

    def test_draw(self):
        self.chave.draw(self.screen)
        self.sprites[0].blit.assert_called_with(self.chave.image, self.chave.rect)

if __name__ == '__main__':
    unittest.main()