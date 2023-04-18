import pygame
from PIL import Image

class Decor(pygame.sprite.DirtySprite):
    type = "decor"
    order = 2

    def __init__(self, x, y, sprite):
        super().__init__()
        self.x = x
        self.y = y
        self.w = sprite.get_width()
        self.h = sprite.get_height()
        self.sprite = sprite

    # Draws the road and decoration on the screen
    def draw(self, screen, camera_x, camera_y, time):
        screen.blit(self.sprite, (self.x + camera_x, self.y + camera_y))


class DecorIa(pygame.sprite.DirtySprite):
    type = "decorIa"
    order = 3

    def __init__(self, id, x, y, image, animated=False):
        super().__init__()
        self.sprite = None
        self.id = id
        self.x = x
        self.y = y
        self.animated = animated
        if self.animated:
            self.order = 4
            self.w = image[0].width
            self.h = image[0].height
        else:
            self.w = image.width
            self.h = image.height
        self.set_image(image)

    def set_image(self, image):
        if self.animated:
            self.sprite = []
            for i in range(len(image)):
                # blend current sprite with next sprite
                idx = (i + 1) % len(image)
                for j in range(1, 4):
                    im2 = Image.blend(image[i], image[idx], j / 4)
                    self.sprite.append(pygame.image.fromstring(im2.tobytes(), image[i].size, image[i].mode).convert_alpha())
        else:
            self.sprite = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()

    # Draws the decoration on the screen
    def draw(self, screen, camera_x, camera_y, time):
        if self.animated:
            screen.blit(self.sprite[int(time % len(self.sprite))], (self.x + camera_x, self.y + camera_y))
        else:
            screen.blit(self.sprite, (self.x + camera_x, self.y + camera_y))
