import pygame

class Input:
    def __init__(self):
        self.keys = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.keys["up"] = True
            elif event.key == pygame.K_DOWN:
                self.keys["down"] = True
            elif event.key == pygame.K_LEFT:
                self.keys["left"] = True
            elif event.key == pygame.K_RIGHT:
                self.keys["right"] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.keys["up"] = False
            elif event.key == pygame.K_DOWN:
                self.keys["down"] = False
            elif event.key == pygame.K_LEFT:
                self.keys["left"] = False
            elif event.key == pygame.K_RIGHT:
                self.keys["right"] = False
