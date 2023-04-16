import pygame


class Shape(pygame.sprite.DirtySprite):
    type = "shape"
    x = 0
    y = 0
    sprite = ""
    order = 9
    shape_points = []
    draw_shape = True

    # Initialize Shape object
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.shape_points = []

    # Add a point to the shape when the user clicks on the screen
    def add_point(self, event):
        self.shape_points.append(event.pos)
        print(self.shape_points)

    # Draw the shape on the screen
    def draw(self, screen, camera_x, camera_y):
        if len(self.shape_points) > 2 and self.draw_shape:
            w, h = screen.get_size()
            # Create a mask surface with the size of the screen
            mask = pygame.Surface((w, h))
            # Set the color key to make the mask transparent
            mask.set_colorkey((0, 0, 0))
            # Set the alpha value of the mask
            mask.set_alpha(50)
            # Fill the mask with black color
            mask.fill((0, 0, 0))
            # Draw the polygon on the mask using the shape points
            pygame.draw.polygon(mask, (255, 0, 0), self.shape_points)
            # Draw the mask on the screen
            screen.blit(mask, (0, 0))
