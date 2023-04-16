import pygame


class Text:
    sprites = []
    font_title = None
    font_sub = None

    def __init__(self, sprites):
        self.sprites = sprites
        self.font_title = pygame.font.Font("assets/fonts/RetroGaming.ttf", 8)
        self.font_sub = pygame.font.Font("assets/fonts/RetroGaming.ttf", 10)

    # Renders the title and subtitle text with a background and border
    def title(self, text, sub_text, screen, x, y, camera_x, camera_y, offset_x=0, offset_y=0):
        text = self.font_title.render(text, True, (0, 0, 0))
        if sub_text != "":
            sub_text = self.font_sub.render(sub_text, True, (0, 0, 0))
            height = text.get_height() + sub_text.get_height() + 6 + 6
            width = max(text.get_width(), sub_text.get_width()) + 12
        else:
            height = text.get_height() + 6 + 6
            width = text.get_width() + 12

        temp_surface = pygame.Surface((width, height))
        temp_surface.fill((255, 255, 255, 225))

        temp_surface.blit(text, ((width - text.get_width()) // 2, 6))
        if sub_text != "":
            temp_surface.blit(sub_text, ((width - sub_text.get_width()) // 2, text.get_height() + 6))
        pygame.draw.rect(temp_surface, (224, 186, 123), pygame.Rect(0, 0, width, height), 2,
                         border_bottom_right_radius=5, border_bottom_left_radius=5,
                         border_top_right_radius=5, border_top_left_radius=5)

        screen.blit(temp_surface,
                    (x + camera_x + offset_x + self.sprites.tile_width // 2 - (temp_surface.get_width()) // 2,
                     y + camera_y + offset_y - 50))

    # Renders the subtitle text
    def subtitle(self, text, screen, x, y, camera_x, camera_y, offset_x=0, offset_y=0):
        text = self.font_sub.render(text, True, (0, 0, 0))
        w = text.get_width()
        screen.blit(text, (x + camera_x + offset_x + self.sprites.tile_width // 2 - w // 2, y + camera_y + offset_y))
