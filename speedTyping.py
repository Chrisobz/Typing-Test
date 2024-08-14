import pygame
from pygame.locals import *
import sys
import time
import random

class Game:
   
    def __init__(self):
        # Initialize game window dimensions and variables
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False

        # Define colors
        self.HEAD_C = (255,213,102)
        self.TEXT_C = (240,240,240)
        self.RESULT_C = (255,70,70)
        
        # Initialize pygame and load images
        pygame.init()
        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

        # Set up the game window
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed Test')
        
    def draw_text(self, screen, msg, y, fsize, color, max_width=None):
        """
        Draw text on the screen with optional word wrapping.

        Args:
            screen: Pygame screen object to draw on.
            msg: The text message to display.
            y: The vertical position of the text.
            fsize: Font size of the text.
            color: Color of the text.
            max_width: Maximum width before wrapping the text.
        """
        font = pygame.font.Font(None, fsize)
        words = msg.split(' ')
        lines = []
        current_line = ""
        
        # Handle word wrapping
        for word in words:
            test_line = current_line + word + " "
            text_width, text_height = font.size(test_line)
            
            if max_width and text_width > max_width:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
        
        lines.append(current_line)
        
        # Render each line of text
        for i, line in enumerate(lines):
            text = font.render(line, True, color)
            text_rect = text.get_rect(center=(self.w/2, y + i * text_height))
            screen.blit(text, text_rect)
    
    def get_sentence(self):
        """Fetch a random sentence from the sentences file."""
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        """Calculate and display the typing test results."""
        if not self.end:
            self.total_time = time.time() - self.time_start
            if self.total_time > 0:  # Ensure no division by zero
                count = 0
                for i, c in enumerate(self.word):
                    try:
                        if self.input_text[i] == c:
                            count += 1
                    except:
                        pass
                # Calculate accuracy and WPM
                self.accuracy = count / len(self.word) * 100
                self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True
                
            self.results = 'Time:' + str(round(self.total_time, 2)) + " secs   Accuracy:" + str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # Display result image and reset button
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            screen.blit(self.time_img, (self.w/2-75, self.h-140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))
            
            pygame.display.update()

    def run(self):
        """Main game loop."""
        self.reset_game()
    
        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # Activate typing when user clicks on the text box
                    if x >= 50 and x <= 650 and y >= 250 and y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                    # Reset the game when reset button is clicked
                    if x >= 310 and x <= 510 and y >= 390 and self.end:
                        self.reset_game()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            # Show results when Enter key is pressed
                            self.show_results(self.screen)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)  
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            # Handle backspace for input text
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()
            clock.tick(60)

    def reset_game(self):
        """Reset the game state to start a new test."""
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)
        
        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.word = self.get_sentence()
        if not self.word:
            self.reset_game()

        # Set up the initial display with the sentence and input box
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.draw_text(self.screen, "Typing Speed Test", 80, 80, self.HEAD_C)  
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C, max_width=650)
        
        pygame.display.update()

# Run the game
Game().run()
