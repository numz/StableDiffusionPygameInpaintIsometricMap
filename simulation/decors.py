import pygame


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
    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.sprite, (self.x + camera_x, self.y + camera_y))


class DecorIa(pygame.sprite.DirtySprite):
    type = "decorIa"
    order = 3

    def __init__(self, id, x, y, image):
        super().__init__()
        self.sprite = None
        self.id = id
        self.x = x
        self.y = y
        self.w = image.width
        self.h = image.height
        self.set_image(image)

    def set_image(self, image):
        self.sprite = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()

    # Draws the decoration on the screen
    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.sprite, (self.x + camera_x, self.y + camera_y))