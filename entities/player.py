import pygame
import os

class Player:
    def __init__(self, image: pygame.Surface, position: tuple[int, int]):
        self.image = image
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.imagem, self.rect)

    @classmethod
    def create(cls, assets_dir, screen_width: int, screen_height: int):
        path = os.path.join(assets_dir, "player_ship.png")
        image = pygame.image.load(path).convert_alpha()
        position = (screen_width // 2, screen_height // 2)
        return cls(image, position)
