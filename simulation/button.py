import pygame


# Création d'une classe pour les boutons
class Button:
    type = "button_menu"
    order = 9

    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.visible = True

    def draw(self, screen, camera_x, camera_y, time):
        if self.visible:
            mouse = pygame.mouse.get_pos()
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
                pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

            font = pygame.font.Font(None, 20)
            text = font.render(self.text, True, self.text_color)
            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text, text_rect)

    def is_clicked(self):
        if self.visible:
            mouse = pygame.mouse.get_pos()
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
                return pygame.mouse.get_pressed()[0]
        return False