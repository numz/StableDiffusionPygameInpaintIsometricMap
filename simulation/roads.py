import pygame


class Road(pygame.sprite.DirtySprite):
    type = "road"
    order = 1

    def __init__(self, x, y, sprite, deco):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite = sprite
        self.deco = deco

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.sprite, (self.x + camera_x, self.y + camera_y))
        screen.blit(self.deco, (self.x + camera_x, self.y + camera_y))
