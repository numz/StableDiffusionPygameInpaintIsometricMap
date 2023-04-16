import numpy as np
import pygame


class Vehicule(pygame.sprite.DirtySprite):
    type = "vehicule"
    order = 4

    def __init__(self, sprites, road, id, text):
        super().__init__()
        self.sprite = None
        self.x = None
        self.y = None
        self.sprites = sprites
        self.text = text
        self.requisitions = 0

        if np.random.randint(20) > 10:
            self.sprite_orientation = self.sprites.bus
        else:
            self.sprite_orientation = self.sprites.car

        self.line = road["from"]["x"]
        self.col = road["from"]["y"]
        self.id = id
        self.visible = False
        self.leave = np.random.randint(60 * 24)
        self.arrival = self.leave + np.random.randint((60 * 24) - self.leave)
        self.depart = (road["from"]["x"], road["from"]["y"])
        self.arrivee = (road["to"]["x"], road["to"]["y"])

    # Updates the vehicle's visibility and position based on the current time
    def update(self, time):
        if self.leave < time < self.arrival:
            self.visible = True
        else:
            self.visible = False

        if self.visible:

            diff_line = self.arrivee[0] - self.depart[0]
            diff_col = self.arrivee[1] - self.depart[1]

            sign_x = 1 if diff_col > 0 else -1
            sign_y = 1 if diff_line > 0 else -1

            distance = abs(diff_line) + abs(diff_col)
            vitesse = distance / (self.arrival - self.leave + 0.000001)

            time_elapsed = time - self.leave
            horizontal_time = abs(diff_col) / (vitesse+0.000001)

            if time_elapsed <= horizontal_time:
                self.col = self.depart[1] + sign_x * time_elapsed * vitesse
                self.line = self.depart[0]
                if sign_x == 1:
                    self.sprite = self.sprite_orientation["right"]
                else:
                    self.sprite = self.sprite_orientation["left"]
            else:
                self.col = self.arrivee[1]
                self.line = self.depart[0] + sign_y * (time_elapsed - horizontal_time) * vitesse
                if sign_y == 1:
                    self.sprite = self.sprite_orientation["down"]
                else:
                    self.sprite = self.sprite_orientation["up"]

            self.x = self.sprites.start_x + self.col * self.sprites.move_x_x - self.line * self.sprites.move_x_y
            self.y = self.sprites.start_y + self.line * self.sprites.move_y_x + self.col * self.sprites.move_y_y

    # Draws the vehicle on the screen
    def draw(self, screen, camera_x, camera_y):
        if self.visible:
            screen.blit(self.sprite, (self.x + camera_x, self.y + camera_y))
            screen.blit(self.sprite, (self.x + camera_x, self.y + camera_y))
