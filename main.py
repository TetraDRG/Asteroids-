import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import Score


def display_game_over(screen, font):
    game_over_surface = font.render("Game Over", True, "red")
    reset_surface = font.render("Press R to Reset", True, "white")
    screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    screen.blit(reset_surface, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 10))


def reset_game(score, asteroids, shots, player, asteroid_field):
    score.lives = 3
    score.score = 0
    # Clear all asteroids from the screen
    for asteroid in asteroids:
        asteroid.kill()
    asteroids.empty()
    shots.empty()
    player.position = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Reset player position
    player.velocity = pygame.math.Vector2(0, 0)  # Reset player velocity
    player.angle = 0  # Reset player angle
    asteroid_field.spawn_asteroids()  # Immediately spawn new asteroids


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField(num_asteroids=5)  # Initialize asteroid field with fewer asteroids

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Initialize score
    score = Score()

    dt = 0

    font = pygame.font.Font(None, 50)  # Font for "Game Over" and reset message

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if score.lives <= 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game(score, asteroids, shots, player, asteroid_field)  # Reset the game

        if score.lives > 0:
            updatable.update(dt)  # Continue updating all objects

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    score.decrement_life()  # Decrement lives on collision
                    if score.lives <= 0:
                        break  # Exit collision handling if lives reach 0
                    asteroid.kill()  # Remove the asteroid after collision

                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()
                        score.increment()  # Increment score for every asteroid hit

            for shot in shots:
                if shot.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    shots.remove(shot)
                    score.increment()  # Increment score by default value (100)

            screen.fill("black")

            for obj in drawable:
                obj.draw(screen)

            # Draw the score
            score.draw(screen, 10, 10)
        else:
            screen.fill("black")
            display_game_over(screen, font)  # Display "Game Over" and reset message

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
