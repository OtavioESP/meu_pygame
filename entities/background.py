import pygame
import os

class Background:
    def __init__(self, image: pygame.Surface):
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (0,0))

    @classmethod
    def create_background(cls, assets_dir):
        path = os.path.join(assets_dir,"˜background.png")
        image = pygame.image.load(path).convert()
        return cls(image)
