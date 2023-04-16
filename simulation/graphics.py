import numpy as np
import os
import json
from PIL import Image
import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
from simulation.text import Text
from simulation.isometric import SpritesIsometric
from simulation.roads import Road
from simulation.decors import Decor, DecorIa
from simulation.vehicule import Vehicule
from simulation.input_box import InputBox
from simulation.shape import Shape
from simulation.button import Button
from config.config import Config


class Graphics:
    def __init__(self):
        self.config = Config()
        self.roads = None
        self.map_matrix = np.zeros((self.config.map.map_lines, self.config.map.map_columns))
        self.objects_list_static = []
        self.objects_list_dynamic = []
        self.group = pygame.sprite.LayeredDirty()
        self.vehicules = []
        self.drawing = False
        self.shape = None
        self.map_name = self.config.map.default_name
        self.display_menu = True
        self.mask_shape_points = None
        self.screen_width = self.config.map.screen_width
        self.screen_height = self.config.map.screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.sprites = SpritesIsometric()
        self.text = Text(self.sprites)
        self.background = self.sprites.background
        self.new_map_button = Button((self.screen_width / 2) - 100, (self.screen_height / 2) - 60, 200, 50, "New Map",
                                     (50, 150, 200), (70, 170, 220), (0, 0, 0))
        self.load_map_button = Button((self.screen_width / 2) - 100, (self.screen_height / 2) + 60, 200, 50, "Load Map",
                                      (50, 150, 200), (70, 170, 220), (0, 0, 0))
        self.input_box_active = False
        self.input_box = TextBox(self.screen, (self.screen_width // 2) - 100, (self.screen_height // 2) - 200, 200, 40,
                                 fontSize=30, borderColour=(224, 186, 123), textColour=(0, 0, 0),
                                 onSubmit=self.new_map, radius=5, borderThickness=2)
        self.dropdown_active = False
        choices = []
        values = []
        for map_name in os.listdir(self.config.folder.maps):
            choices.append(map_name)
            values.append(map_name)

        self.dropdown = Dropdown(
            self.screen, (self.screen_width // 2) - 50, (self.screen_height // 2) - 25, 100, 50, name='Select map',
            choices=choices, borderRadius=3, colour=(50, 150, 200), values=values, direction='down',
            textHAlign='left',  textColour=(0, 0, 0), textHMargin=10, textVMargin=10,
        )

    def init_new_map(self):
        map_matrix = np.empty((self.config.map.map_lines, self.config.map.map_columns), dtype=object)

        # Generate random road plans
        # change random seed each time to get different results
        np.random.seed()

        roads = [{"from": {"x": np.random.randint(self.config.map.map_lines), "y": np.random.randint(self.config.map.map_columns)},
                  "to": {"x": np.random.randint(self.config.map.map_lines), "y": np.random.randint(self.config.map.map_columns)}}
                 for _ in range(self.config.map.nb_roads)]

        # Draw roads on map matrix
        for road in roads:
            diff_x = road['to']['x'] - road['from']['x']
            diff_y = road['to']['y'] - road['from']['y']
            sign_x = 1 if diff_x > 0 else -1
            sign_y = 1 if diff_y > 0 else -1
            yp = road['from']['y']
            xp = road['from']['x']

            for j in range(abs(diff_y)):
                yp += sign_y
                map_matrix[xp, yp] = [1] if map_matrix[xp, yp] is None else map_matrix[xp, yp] + [1]

            for i in range(abs(diff_x)):
                xp += sign_x
                map_matrix[xp, yp] = [1] if map_matrix[xp, yp] is None else map_matrix[xp, yp] + [1]

        # Clean up map matrix
        for i in range(len(map_matrix)):
            for j in range(len(map_matrix[i])):
                if map_matrix[i][j] is None or not map_matrix[i][j]:
                    map_matrix[i][j] = 0
                elif all(x == 1 for x in map_matrix[i][j]):
                    map_matrix[i][j] = 1

        self.map_matrix = map_matrix
        self.roads = roads

        #create dir from name
        if not os.path.exists(self.config.folder.maps+self.map_name):
            os.makedirs(self.config.folder.maps+self.map_name)
        #save as json file
        map = {"map_matrix": self.map_matrix.tolist(), "roads": self.roads}
        with open(self.config.folder.maps+self.map_name+"/"+self.map_name+'.json', 'w') as f:
            json.dump(map, f, indent=4)
        print(self.map_matrix)

    def capture(self, name, pos, size, camera_x, camera_y):  # (pygame Surface, String, tuple, tuple)
        for obj in self.objects_list_static:
            obj.draw(self.screen, camera_x, camera_y)
        for obj in self.objects_list_dynamic:
            if obj.type != "shape":
                obj.draw(self.screen, camera_x, camera_y)
        image = pygame.Surface(size)  # Create image surface
        image.blit(self.screen, (0, 0), (pos, size))  # Blit portion of the display to the image
        pygame.image.save(image, name)  # Save the image to the disk**

    def save_shape(self, camera_x, camera_y):
        self.drawing = False
        if len(self.shape.shape_points) >= 3:
            x = min(self.shape.shape_points, key=lambda x: x[0])[0]
            y = min(self.shape.shape_points, key=lambda x: x[1])[1]
            w = max(self.shape.shape_points, key=lambda x: x[0])[0] - x
            h = max(self.shape.shape_points, key=lambda x: x[1])[1] - y

            if w < 492:
                w = 492
            elif 748 > w > 492:
                w = 748

            if h < 492:
                h = 492
            elif 748 > h > 492:
                h = 748

            x, y, w, h = pygame.Rect(x, y, w, h).inflate(20, 20).topleft + pygame.Rect(x, y, w, h).inflate(20, 20).size
            self.mask_shape_points = [(p[0] - x, p[1] - y) for p in self.shape.shape_points]
            mask = pygame.Surface((w, h))
            mask.fill((0, 0, 0))
            pygame.draw.polygon(mask, (255, 255, 255), self.mask_shape_points)
            pygame.image.save(mask, self.config.folder.temp+self.config.file.temp_mask)
            self.capture(self.config.folder.temp+self.config.file.temp_capture, (x, y), (w, h), camera_x, camera_y)
            # convert image to str base64
            self.objects_list_dynamic.append(
                InputBox(self.map_name, x - camera_x, y - camera_y, w, h,
                         self.config.folder.temp+self.config.file.temp_capture,
                         self.config.folder.temp+self.config.file.temp_mask,
                         self.text, self.objects_list_static))
        else:
            self.objects_list_dynamic = [x for x in self.objects_list_dynamic if x.type != "shape"]

    def add_shape_point(self, event):
        self.shape.add_point(event)

    def begin_shape(self):
        self.objects_list_dynamic = [x for x in self.objects_list_dynamic if x.type != "shape" and x.type != "inputBox"]
        self.shape = Shape()
        self.objects_list_dynamic.append(self.shape)
        self.drawing = True

    def create_road(self, line, col, x, y):
        top = self.map_matrix[line - 1][col] if line - 1 >= 0 else 0
        left = self.map_matrix[line][col - 1] if col - 1 >= 0 else 0
        right = self.map_matrix[line][col + 1] if col + 1 < len(self.map_matrix[line]) else 0
        bottom = self.map_matrix[line + 1][col] if line + 1 < len(self.map_matrix) else 0

        deco = self.sprites.sprites["0"]
        if top == 0 and left == 0 and right == 0 and bottom != 0:
            sprite = self.sprites.road_type["0"]
        elif top == 0 and left == 0 and right != 0 and bottom == 0:
            sprite = self.sprites.road_type["1"]
        elif top == 0 and left == 0 and right != 0 and bottom != 0:
            sprite = self.sprites.road_type["3"]
        elif top == 0 and left != 0 and right == 0 and bottom == 0:
            sprite = self.sprites.road_type["1"]
        elif top == 0 and left != 0 and right == 0 and bottom != 0:
            sprite = self.sprites.road_type["4"]
        elif top == 0 and left != 0 and right != 0 and bottom == 0:
            sprite = self.sprites.road_type["1"]
        elif top == 0 and left != 0 and right != 0 and bottom != 0:
            sprite = self.sprites.road_type["9"]
        elif top != 0 and left == 0 and right == 0 and bottom == 0:
            sprite = self.sprites.road_type["0"]
        elif top != 0 and left == 0 and right == 0 and bottom != 0:
            sprite = self.sprites.road_type["0"]
        elif top != 0 and left == 0 and right != 0 and bottom == 0:
            sprite = self.sprites.road_type["5"]
        elif top != 0 and left == 0 and right != 0 and bottom != 0:
            sprite = self.sprites.road_type["7"]
            deco = self.sprites.road_decor_threeway_right[
                str(np.random.randint(0, len(self.sprites.road_decor_threeway_right.keys())))]
        elif top != 0 and left != 0 and right == 0 and bottom == 0:
            sprite = self.sprites.road_type["2"]
        elif top != 0 and left != 0 and right == 0 and bottom != 0:
            sprite = self.sprites.road_type["10"]
        elif top != 0 and left != 0 and right != 0 and bottom == 0:
            sprite = self.sprites.road_type["8"]
        elif top != 0 and left != 0 and right != 0 and bottom != 0:
            sprite = self.sprites.road_type["6"]
            deco = self.sprites.road_decor_cross[str(np.random.randint(0, len(self.sprites.road_decor_cross.keys())))]
        else:
            sprite = self.sprites.road_type["0"]

        self.objects_list_static.append(Road(x, y, sprite, deco))

    def input_events(self, events):
        pygame_widgets.update(events)
        if self.dropdown.getSelected() != self.map_name and self.dropdown_active:
            self.load_saved_map()

    def new_map(self):
        # Get text in the textbox
        if self.input_box.getText() != "":
            self.map_name = self.input_box.getText()
            self.init_new_map()
            self.objects_list_dynamic = []
            self.objects_list_static = []
            self.input_box.setText("")
            self.draw_map()
            self.input_box_active = False
            self.display_menu = False

    def load_saved_map(self):
        if self.dropdown.getSelected() is not None:
            self.objects_list_dynamic = []
            self.objects_list_static = []
            self.map_name = self.dropdown.getSelected()
            with open(self.config.folder.maps + self.map_name + "/" + self.map_name + ".json", "r") as f:
                map_data = json.load(f)
            self.map_matrix = np.array(map_data["map_matrix"])
            self.roads = map_data["roads"]
            self.draw_map()
            self.input_box_active = False
            self.display_menu = False

    def draw_map(self):
        for line in range(self.config.map.total_lines):
            for col in range(self.config.map.total_columns):
                if not (self.sprites.start_y + self.config.map.map_columns + 1 > col > self.sprites.start_y
                        and self.sprites.start_x + self.config.map.map_lines + 1 > line > self.sprites.start_x):
                    x = self.sprites.start_x + col * self.sprites.move_x_x - line * self.sprites.move_x_y
                    y = self.sprites.start_y - (42 * self.sprites.move_y_x) + line * self.sprites.move_y_x + col * self.sprites.move_y_y
                    sprite = self.sprites.sprites["1"]
                    deco = self.sprites.sprites["0"]
                    self.objects_list_static.append(Road(x, y, sprite, deco))
                    np.random.seed(line + col * 1000)
                    sprite = self.sprites.decor[str(np.random.randint(0, len(self.sprites.decor.keys())))]
                    self.objects_list_static.append(Decor(x, y, sprite))

        # list folder
        if self.map_name != "":
            path = self.config.folder.maps + self.map_name + "/" + self.config.folder.decor
            decors_ia = []
            if os.path.isdir(path):
                for file in os.scandir(path):
                    _, id_img, x, y, w, h = file.name.replace(".png", "").split("_")
                    image = Image.open(path + file.name)
                    decors_ia.append([int(id_img), int(x), int(y), int(w), int(h), image])
            decors_ia = sorted(decors_ia, key=lambda x: x[0])

            for id_decor, x, y, w, h, image in decors_ia:
                self.objects_list_static.append(DecorIa(id_decor, x, y, image))

        for line in range(len(self.map_matrix)):
            for col in range(len(self.map_matrix[0])):
                x = self.sprites.start_x + col * self.sprites.move_x_x - line * self.sprites.move_x_y
                y = self.sprites.start_y + line * self.sprites.move_y_x + col * self.sprites.move_y_y
                if line < len(self.map_matrix) and col < len(self.map_matrix[line]):
                    if self.map_matrix[line][col] != 0:
                        self.create_road(line, col, x, y)
                    else:
                        sprite = self.sprites.sprites["1"]
                        deco = self.sprites.sprites["0"]
                        self.objects_list_static.append(Road(x, y, sprite, deco))
                        np.random.seed(line + col * 1000)
                        sprite = self.sprites.decor[str(np.random.randint(0, len(self.sprites.decor.keys())))]
                        self.objects_list_static.append(Decor(x, y, sprite))
                col += 1
            line += 1

        k = 0
        for road in self.roads:
            self.objects_list_dynamic.append(Vehicule(self.sprites, road, k, self.text))
            k += 1

        self.objects_list_dynamic.append(self.new_map_button)
        self.objects_list_dynamic.append(self.load_map_button)

        self.objects_list_static = sorted(self.objects_list_static, key=lambda k: k.order)
        self.objects_list_dynamic = sorted(self.objects_list_dynamic, key=lambda k: k.order)

    def load_map(self):
        self.init_new_map()
        self.draw_map()

    def draw(self, camera_x, camera_y, time, time_speed, draw_decor):
        self.screen.blit(self.background, (-2430 + camera_x, -40 + camera_y))

        for obj in self.objects_list_static:
            if obj.type in ["decor", "decorIa"]:
                if draw_decor:
                    if (
                            -camera_x + self.screen_width > obj.x > -camera_x and -camera_y + self.screen_height > obj.y > -camera_y) or \
                            (
                                    -camera_x + self.screen_width > obj.x + obj.w > -camera_x and -camera_y + self.screen_height > obj.y > -camera_y) or \
                            (
                                    -camera_x + self.screen_width > obj.x > -camera_x and -camera_y + self.screen_height > obj.y + obj.h > -camera_y) or \
                            (
                                    -camera_x + self.screen_width > obj.x + obj.w > -camera_x and -camera_y + self.screen_height > obj.y + obj.h > -camera_y):
                        obj.draw(self.screen, camera_x, camera_y)
            else:
                obj.draw(self.screen, camera_x, camera_y)

        for obj in self.objects_list_dynamic:
            if self.display_menu and obj.type == "button_menu":
                obj.draw(self.screen, camera_x, camera_y)
                obj.visible = True
            elif not self.display_menu and obj.type == "button_menu":
                obj.visible = False
            elif not self.display_menu and obj.type != "button_menu":
                obj.draw(self.screen, camera_x, camera_y)

        if self.input_box_active:
            self.display_menu = False
            self.input_box.draw()
        if self.dropdown_active:
            self.display_menu = False
            self.dropdown.draw()
