import pygame
import random
from dataclasses import dataclass
from typing import List

# Initialize Pygame
pygame.init()

# Configuration
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

@dataclass
class Letter:
    content: str
    category: str
    x: int
    y: int
    dragged: bool = False

class GameState:
    WELCOME = "welcome"
    PLAYING = "playing"
    GAME_OVER = "game_over"

class SantaLetterSorter:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Santa's Letter Sorter")
        self.clock = pygame.time.Clock()

        # Load assets
        self.font = pygame.font.Font("assets/fonts/MountainsofChristmas-Regular.ttf", 24)
        self.title_font = pygame.font.Font("assets/fonts/MountainsofChristmas-Regular.ttf", 32)
        self.big_font = pygame.font.Font("assets/fonts/MountainsofChristmas-Regular.ttf", 48)
        self.background = pygame.image.load("assets/background3.png").convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background_y_position = 0
        self.background_speed = 0
        
        # Sound effects
        self.success_sound = pygame.mixer.Sound("assets/sounds/coin.mp3")
        self.error_sound = pygame.mixer.Sound("assets/sounds/error.mp3")
        pygame.mixer.music.load("assets/sounds/background.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets/sounds/song2.mp3")
        self.game_over_sound.set_volume(0.7)  # Ajuster le volume si nécessaire
        
        # Game state
        self.state = GameState.WELCOME
        self.letters = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.time_left = 45
        self.selected_letter = None
        self.is_game_over_music_playing = False

        # Categories with letters content
        self.letter_templates = {
            "toys": [
                "Dear Santa, I would love to have a toy car set.",
                "Could you bring me a building block set this Christmas?",
                "I dream of playing with a remote-controlled helicopter.",
                "A stuffed teddy bear would make me so happy!",
                "I wish for a toy kitchen to play chef with my friends.",
                "Santa, I would love a puzzle game to solve.",
                "A magical light-up wand would make my Christmas magical.",
                "Could you send me a set of action figures?",
                "I would like a toy spaceship for my adventures.",
                "Please bring me a colorful spinning top to play with."
            ],
            "books": [
                "Dear Santa, I would love a book of fairy tales to read before bed.",
                "Could you bring me a mystery novel to solve thrilling puzzles?",
                "I wish for a coloring book with my favorite animals.",
                "A book of magical spells and potions would be amazing!",
                "Santa, I would love to have a comic book collection.",
                "I dream of reading about space adventures in a sci-fi book.",
                "Please bring me an encyclopedia about dinosaurs.",
                "I would love a poetry book filled with beautiful verses.",
                "A book of recipes for kids would be perfect for my kitchen.",
                "I wish for a graphic novel full of superheroes and villains."
            ],
            "sports": [
                "Dear Santa, I dream of having a shiny new basketball.",
                "Could you bring me a pair of running shoes for my races?",
                "I wish for a cricket bat to play with my friends.",
                "Santa, I would love a yoga mat for practicing stretches.",
                "A set of golf clubs would make my holidays extra fun!",
                "Please bring me a badminton racket and shuttlecock.",
                "I dream of having protective gear for skateboarding.",
                "A set of colorful hula hoops would be so exciting!",
                "I wish for a water bottle and a sports bag for training.",
                "Could you send me a volleyball and a net for beach games?"
            ]
        }

        # Create bins
        self.bins = {
            "toys": pygame.Rect(100, WINDOW_HEIGHT - 100, 200, 80),
            "books": pygame.Rect(400, WINDOW_HEIGHT - 100, 200, 80),
            "sports": pygame.Rect(700, WINDOW_HEIGHT - 100, 200, 80)
        }

        # Start playing welcome music
        pygame.mixer.music.play(-1)

    def load_high_score(self):
        try:
            with open("data/highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data/highscore.txt", "w") as f:
                f.write(str(self.high_score))

    def spawn_letter(self):
        """Create a new letter with random category and content"""
        if len(self.letters) < 4:
            category = random.choice(list(self.letter_templates.keys()))
            content = random.choice(self.letter_templates[category])
            x = random.randint(50, WINDOW_WIDTH - 250)
            y = random.randint(50, 400)
            self.letters.append(Letter(content, category, x, y))

    def start_game(self):
        self.state = GameState.PLAYING
        self.score = 0
        self.time_left = 45
        self.letters = []
        self.spawn_letter()
        pygame.mixer.music.stop()
        self.is_game_over_music_playing = False
        self.game_over_sound.stop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.WELCOME:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.WELCOME
                        pygame.mixer.music.play(-1)
                        self.game_over_sound.stop()
                        self.is_game_over_music_playing = False
            
            if self.state == GameState.PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for letter in self.letters:
                        letter_rect = pygame.Rect(letter.x, letter.y, 200, 100)
                        if letter_rect.collidepoint(mouse_pos):
                            letter.dragged = True
                            self.selected_letter = letter
                            break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.selected_letter:
                        mouse_pos = pygame.mouse.get_pos()
                        for category, bin_rect in self.bins.items():
                            if bin_rect.collidepoint(mouse_pos):
                                if self.selected_letter.category == category:
                                    self.score += 10
                                    self.success_sound.play()
                                else:
                                    self.score = self.score - 5 
                                    self.error_sound.play()
                                self.letters.remove(self.selected_letter)
                                self.spawn_letter()
                        self.selected_letter.dragged = False
                        self.selected_letter = None

                elif event.type == pygame.MOUSEMOTION:
                    if self.selected_letter:
                        self.selected_letter.x, self.selected_letter.y = event.pos[0] - 100, event.pos[1] - 50

        return True

    def update(self):
        if self.state == GameState.PLAYING:
            self.time_left -= 1/FPS
            if self.time_left <= 0:
                self.state = GameState.GAME_OVER
                self.save_high_score()
                if not self.is_game_over_music_playing:
                    self.game_over_sound.play(-1)  # -1 pour jouer en boucle
                    self.is_game_over_music_playing = True
            
            if len(self.letters) < 4:
                self.spawn_letter()
 
        self.background_y_position += self.background_speed
        if self.background_y_position >= WINDOW_HEIGHT:
            self.background_y_position = 0

    def draw_welcome_screen(self):
        self.screen.blit(self.background, (0, 0))
        title = self.big_font.render("Santa's Letter Sorter", True, BLACK)
        subtitle = self.title_font.render("Press SPACE to start", True, BLACK)
        high_score_text = self.title_font.render(f"High Score: {self.high_score}", True, BLACK)
        
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH//2, 2*WINDOW_HEIGHT//3))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        self.screen.blit(high_score_text, high_score_rect)

    def draw_game_screen(self):
        self.screen.blit(self.background, (0, self.background_y_position - WINDOW_HEIGHT))
        self.screen.blit(self.background, (0, self.background_y_position))

        score_text = self.big_font.render(f"Score: {self.score}", True, BLACK)
        time_text = self.big_font.render(f"Time: {int(self.time_left)}s", True, BLACK)
        self.screen.blit(score_text, (120, 50))
        self.screen.blit(time_text, (WINDOW_WIDTH - 300, 50))

        for category, rect in self.bins.items():
            pygame.draw.rect(self.screen, BLUE, rect)
            text = self.font.render(category.upper(), True, WHITE)
            self.screen.blit(text, (rect.x + 10, rect.y + 30))

        for letter in self.letters:
            pygame.draw.rect(self.screen, WHITE, (letter.x, letter.y, 200, 100))
            pygame.draw.rect(self.screen, GOLD, (letter.x, letter.y, 200, 100), 2)

            # Improved text wrapping algorithm
            words = letter.content.split()
            lines = []
            current_line = []
            current_width = 0
            
            for word in words:
                word_surface = self.font.render(word + " ", True, BLACK)
                word_width = word_surface.get_width()
                
                if current_width + word_width <= 180:  # Leave some margin
                    current_line.append(word)
                    current_width += word_width
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_width = word_width
            
            if current_line:
                lines.append(' '.join(current_line))

            # Display only first three lines with proper spacing
            for i, line in enumerate(lines[:3]):
                text = self.font.render(line, True, BLACK)
                text_rect = text.get_rect()
                text_rect.left = letter.x + 10
                text_rect.top = letter.y + 10 + (i * 30)
                self.screen.blit(text, text_rect)

    def draw_game_over_screen(self):
        self.screen.blit(self.background, (0, 0))
        game_over = self.big_font.render("Game Over!", True, RED)
        final_score = self.title_font.render(f"Final Score: {self.score}", True, BLACK)
        high_score_text = self.title_font.render(f"High Score: {self.high_score}", True, BLACK)
        continue_text = self.title_font.render("Press SPACE to continue", True, BLACK)
        
        self.screen.blit(game_over, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 100))
        self.screen.blit(final_score, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2))
        self.screen.blit(high_score_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 50))
        self.screen.blit(continue_text, (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT//2 + 100))

    def draw(self):
        if self.state == GameState.WELCOME:
            self.draw_welcome_screen()
        elif self.state == GameState.PLAYING:
            self.draw_game_screen()
        else:  # GAME_OVER
            self.draw_game_over_screen()
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = SantaLetterSorter()
    game.run()
