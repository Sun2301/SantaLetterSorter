import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SNOW_PARTICLE_COUNT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Resource Manager
class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, name, path):
        self.images[name] = pygame.image.load(path)

    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)

    def get_image(self, name):
        return self.images.get(name, None)

    def get_sound(self, name):
        return self.sounds.get(name, None)

# SnowParticle
class SnowParticle:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.wind_speed = random.uniform(-0.5, 0.5)

    def fall(self):
        self.y += self.speed
        self.x += self.wind_speed
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-20, -1)
            self.x = random.randint(0, SCREEN_WIDTH)
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

# Menu System
class MenuSystem:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def display_text(self, text, position, color=WHITE):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def main_menu(self):
        self.screen.fill(BLACK)
        self.display_text("Christmas AI Postmaster", (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))
        self.display_text("Press ENTER to start", (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 50))
        pygame.display.flip()

# Main Game Class
class ChristmasAIPostmaster:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Christmas AI Postmaster")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snow_particles = [SnowParticle(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(1, 4), random.uniform(1, 3)) for _ in range(SNOW_PARTICLE_COUNT)]
        self.menu = MenuSystem(self.screen)
        self.in_game = False

    def run(self):
        while self.running:
            self.handle_events()
            if not self.in_game:
                self.menu.main_menu()
            else:
                self.update()
                self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not self.in_game:
                    self.in_game = True

    def update(self):
        for particle in self.snow_particles:
            particle.fall()

    def draw(self):
        self.screen.fill(BLACK)
        for particle in self.snow_particles:
            particle.draw(self.screen)
        pygame.display.flip()

# Main execution
if __name__ == "__main__":
    game = ChristmasAIPostmaster()
    game.run()
    pygame.quit()
