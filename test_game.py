import unittest
from unittest.mock import patch
import time

# Import the Game class from your main game file
from speedTyping import Game  # Replace with your actual file name

class TestGame(unittest.TestCase):

    @patch('speedTyping.Game.get_sentence')  # Mock the sentence retrieval
    def test_typing_accuracy(self, mock_get_sentence):
        # Mock the sentence to be typed
        mock_get_sentence.return_value = "hello world"
        
        # Create an instance of the game
        game = Game()
        game.word = "hello world"  # Set the word to be typed
        game.input_text = "hello world"  # Simulate correct user input
        
        # Manually set start time to a known value
        game.time_start = time.time() - 30  # Assume the user took 30 seconds
        
        # Call the show_results to calculate accuracy and WPM
        game.show_results(game.screen)
        
        # Check if the accuracy is 100%
        self.assertEqual(game.accuracy, 100.0)
        
        # Check if the WPM is correctly calculated
        self.assertGreater(game.wpm, 0)  # WPM should be greater than 0

    @patch('speedTyping.Game.get_sentence')  # Mock the sentence retrieval
    def test_typing_inaccuracy(self, mock_get_sentence):
        # Mock the sentence to be typed
        mock_get_sentence.return_value = "hello world"
        
        # Create an instance of the game
        game = Game()
        game.word = "hello world"  # Set the word to be typed
        game.input_text = "hella wurld"  # Simulate incorrect user input
        
        # Manually set start time to a known value
        game.time_start = time.time() - 30  # Assume the user took 30 seconds
        
        # Call the show_results to calculate accuracy and WPM
        game.show_results(game.screen)
        
        # Check if the accuracy is less than 100%
        self.assertLess(game.accuracy, 100.0)
        
        # Check if the WPM is correctly calculated
        self.assertGreater(game.wpm, 0)  # WPM should be greater than 0

if __name__ == '__main__':
    unittest.main()
