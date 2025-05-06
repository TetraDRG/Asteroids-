import pygame
import random
import math  # Import the math module
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.vertices = self.generate_polygon()

    def generate_polygon(self):
        # Generate a random polygon with a variable number of vertices
        num_vertices = random.randint(5, 10)  # Number of vertices
        angle_step = 360 / num_vertices
        vertices = []
        for i in range(num_vertices):
            angle = random.uniform(i * angle_step, (i + 1) * angle_step)
            distance = random.uniform(self.radius * 0.7, self.radius)
            vertex = pygame.Vector2(
                self.position.x + distance * math.cos(math.radians(angle)),  # Use math.cos
                self.position.y + distance * math.sin(math.radians(angle))   # Use math.sin
            )
            vertices.append(vertex)
        return vertices

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.vertices, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        # Update the vertices based on the new position
        self.vertices = [
            vertex + self.velocity * dt for vertex in self.vertices
        ]

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # randomize the angle of the split
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_a.velocity = a * 1.2
        asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_b.velocity = b * 1.2

        # Increment score for each smaller asteroid created
        from score import Score  # Avoid circular imports
        Score().increment()
        Score().increment()

    @classmethod
    def random_spawn(cls):
        # Randomly choose an edge of the screen
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x = random.uniform(0, SCREEN_WIDTH)
            y = -ASTEROID_MAX_RADIUS
        elif edge == "bottom":
            x = random.uniform(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
        elif edge == "left":
            x = -ASTEROID_MAX_RADIUS
            y = random.uniform(0, SCREEN_HEIGHT)
        elif edge == "right":
            x = SCREEN_WIDTH + ASTEROID_MAX_RADIUS
            y = random.uniform(0, SCREEN_HEIGHT)

        # Random velocity
        velocity_x = random.uniform(-100, 100)
        velocity_y = random.uniform(-100, 100)

        # Random radius
        radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)

        # Create and return the asteroid
        asteroid = cls(x, y, radius)
        asteroid.velocity = pygame.Vector2(velocity_x, velocity_y)
        return asteroid
