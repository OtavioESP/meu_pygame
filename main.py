import pygame
import os
import sys

from entities.player import Player
from entities.background import Background

pygame.init()
WIDTH, HEIGHT = 800, 600
RED_BAR_HEIGHT = 30
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Clean Architecture")

# Load entities
try:
    background = Background.create_background(ASSETS_DIR)
    player_ship = Player.create(ASSETS_DIR, WIDTH, HEIGHT)
except pygame.error as e:
    print(f"[Error] Asset loading failed: {e}")
    pygame.quit()
    sys.exit()

clock = pygame.time.Clock()

running = True
while running:
    click.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    background.draw(screen)
    player_ship.draw(screen)

    # Draw red bar at the bottom
    pygame.draw.rect(screen, (255, 0, 0), (0, HEIGHT - RED_BAR_HEIGHT, WIDTH, RED_BAR_HEIGHT))

    pygame.display.flip()

# --- Cleanup ---
pygame.quit()
sys.exit()
