import unittest
from unittest.mock import patch, Mock
import pygame
from menu import Button, Music, Display  

class TestButton(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.button = Button(100, 100, 200, 50, text='Test')

    def tearDown(self):
        pygame.quit()

    def test_button_draw(self):
        self.button.draw(self.screen)
        self.assertTrue(self.button.is_selected, "Button should detect mouse hover")

    def test_button_click(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(150, 125))
        self.assertTrue(self.button.is_clicked(event), "Button should detect mouse click")

    def test_button_no_click(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(50, 50))
        self.assertFalse(self.button.is_clicked(event), "Button should not detect mouse click outside")

class TestMusic(unittest.TestCase):

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    @patch('pygame.mixer.music.stop')
    def test_play_music_menu(self, mock_stop, mock_play, mock_load):
        music = Music()
        music.play_music_menu()
        mock_stop.assert_called_once()
        mock_load.assert_called_once_with("./assets/songs/menu_music.mp3")
        mock_play.assert_called_once_with(-1)

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    @patch('pygame.mixer.music.stop')
    def test_play_music_game(self, mock_stop, mock_play, mock_load):
        music = Music()
        music.play_music_game()
        mock_stop.assert_called_once()
        mock_load.assert_called_once_with("./assets/songs/game_music.mp3")
        mock_play.assert_called_once_with(-1)

class TestDisplay(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = Display(self.screen)

    def tearDown(self):
        pygame.quit()

    def test_init_menu(self):
        self.display.init_menu()
        self.assertIsNotNone(self.display.menu_background, "Menu background should be loaded")

    def test_menu_screen(self):
        self.display.active_screen = 'menu'
        self.display.menu_screen()
        # Aqui você deve verificar o conteúdo da tela, mas isso pode ser complexo de fazer com unittests

    def test_credits_screen(self):
        self.display.active_screen = 'credits'
        self.display.credits_screen()
        # Aqui você deve verificar o conteúdo da tela, mas isso pode ser complexo de fazer com unittests

    def test_handle_menu_events(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(350, 275))
        with patch.object(Music, 'play_music_game'):
            self.display.handle_events(event)
            self.assertEqual(self.display.active_screen, 'game', "Screen should switch to game on play button click")

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(350, 375))
        with patch.object(Music, 'play_music_game'):
            self.display.handle_events(event)
            self.assertEqual(self.display.active_screen, 'credits', "Screen should switch to credits on credits button click")

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(350, 475))
        with patch('pygame.quit'):
            with self.assertRaises(SystemExit):
                self.display.handle_events(event)

    def test_handle_credits_events(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(100, 555))
        with patch.object(Music, 'play_music_menu'):
            self.display.handle_events(event)
            self.assertEqual(self.display.active_screen, 'menu', "Screen should switch to menu on back button click in credits")

if __name__ == '_main_':
    unittest.main()