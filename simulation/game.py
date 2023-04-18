import pygame
from simulation.graphics import Graphics
from simulation.input import Input
from config.config import Config


class Game:
    def __init__(self):
        self.config = Config()
        self.running = True
        self.clock = pygame.time.Clock()
        self.graphics = Graphics()
        self.input = Input()
        self.time = 360
        self.pause = False
        self.time_speed = 0.2
        self.camera_x = -40
        self.camera_y = 40
        self.draw_shape = False
        self.draw_decor = True
        self.input_box_active = False

    # Load the map and roads into the graphics object
    def load_map(self):
        self.graphics.load_map()

    # Handle user input events, such as keyboard and mouse actions
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Process input for input box
                for obj in self.graphics.objects_list_dynamic:
                    if obj.type == "inputBox":
                        obj.handle_event(event)
                # Toggle pause state
                if event.key == self.config.action.pause:
                    self.pause = not self.pause
                # Toggle drawing decorations
                if event.key == self.config.action.draw_decor:
                    self.draw_decor = not self.draw_decor
                # Increase time speed
                elif event.key == self.config.action.time_speed_up:
                    self.time_speed += 0.01
                # Decrease time speed
                elif event.key == self.config.action.time_speed_down:
                    self.time_speed -= 0.01
                # Enable drawing shape
                elif event.key == pygame.K_ESCAPE:
                    self.graphics.display_menu = not self.graphics.display_menu
                    self.graphics.dropdown_active = False
                    self.graphics.input_box_active = False
                elif event.key == pygame.K_LSHIFT:
                    self.draw_shape = True
                    self.graphics.begin_shape()
                elif event.key == pygame.K_LCTRL:
                    self.draw_shape = True
                    self.graphics.begin_shape(True)

            elif event.type == pygame.KEYUP:
                # Disable drawing shape
                if event.key == pygame.K_LSHIFT:
                    self.draw_shape = False
                    self.graphics.save_shape(self.camera_x, self.camera_y)
                elif event.key == pygame.K_LCTRL:
                    self.draw_shape = False
                    self.graphics.save_shape(self.camera_x, self.camera_y, True)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Add shape point on mouse click
                if self.draw_shape:
                    if not self.graphics.display_menu:
                        self.graphics.add_shape_point(event)
                elif self.graphics.new_map_button.is_clicked():
                    self.graphics.input_box.setText("")
                    self.graphics.input_box_active = True
                elif self.graphics.load_map_button.is_clicked():
                    self.graphics.dropdown_active = True
            self.input.handle_event(event)

        if self.graphics.input_box_active:
            self.graphics.input_events(events)
        if self.graphics.dropdown_active:
            self.graphics.input_events(events)
        pygame.event.clear()

    # Update the game state, including camera position and objects
    def update(self):
        # Update camera position based on input
        camera_speed = 10
        if self.input.keys["left"]:
            self.camera_x += camera_speed
        if self.input.keys["right"]:
            self.camera_x -= camera_speed
        if self.input.keys["up"]:
            self.camera_y += camera_speed
        if self.input.keys["down"]:
            self.camera_y -= camera_speed

        # Limit camera movement
        if self.camera_x < -60:
            self.camera_x = -60
        if self.camera_x > 2430:
            self.camera_x = 2430
        if self.camera_y < -1250:
            self.camera_y = -1250
        if self.camera_y > 40:
            self.camera_y = 40

        # Update game time
        if not self.pause:
            self.time += self.time_speed
        self.time = self.time % (60 * 24)

        # Update window title with camera coordinates
        pygame.display.set_caption(self.graphics.map_name)

        # Update dynamic objects
        for obj in self.graphics.objects_list_dynamic:
            if obj.type == "inputBox":
                obj.update()
                if obj.decor is not None:
                    # Update or add the decor object
                    decor_ia = [x for x in self.graphics.objects_list_static if x.type == "decorIa"
                                and x.id == obj.decor.id]
                    if len(decor_ia) == 0:
                        self.graphics.objects_list_static.append(obj.decor)
                        self.graphics.objects_list_static = sorted(self.graphics.objects_list_static,
                                                                   key=lambda k: k.order)
                    else:
                        decor_ia[0] = obj.decor
                    self.graphics.shape.draw_shape = False
            elif obj.type in ["vehicule"]:
                obj.update(self.time)

    def draw(self):
        self.graphics.draw(self.camera_x, self.camera_y, self.time, self.time_speed, self.draw_decor)
        if not self.pause:

            pygame.display.update()
            self.clock.tick(60)
