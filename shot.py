import pygame
from constants import *
from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def is_off_screen(self, screen_width, screen_height):
        return (
            self.position.x < 0 or self.position.x > screen_width or
            self.position.y < 0 or self.position.y > screen_height
        )
