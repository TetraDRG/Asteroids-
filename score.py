import pygame

class Score:
    def __init__(self, font_size=30):
        self.score = 0
        self.lives = 3  # Initialize lives
        self.font = pygame.font.Font(None, font_size)

    def increment(self, points=100):  # Default points changed to 100
        self.score += points
        if self.score >= 1000:  # Increment lives when score reaches 1000
            self.score -= 1000
            self.increment_life()

    def decrement_life(self):
        self.lives -= 1

    def increment_life(self):
        self.lives += 1

    def draw(self, screen, x, y):
        score_surface = self.font.render(f"Score: {self.score}", True, "white")
        lives_surface = self.font.render(f"Lives: {self.lives}", True, "white")
        screen.blit(score_surface, (x, y))
        screen.blit(lives_surface, (x, y + 30))  # Draw lives below the score
