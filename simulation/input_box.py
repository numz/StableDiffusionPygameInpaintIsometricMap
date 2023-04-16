import pygame
import os
import json
import requests
import io
import base64
from PIL import Image
from simulation.decors import DecorIa
from config.config import Config


class InputBox(pygame.sprite.DirtySprite):

    type = "inputBox"
    id = 0
    map_name = None
    x = 0
    y = 0
    sprite = ""
    order = 8
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('black')
    font = None
    text = {}
    input_surface = None
    decor = None

    # Initialize InputBox with position, dimensions, images, and other necessary attributes
    def __init__(self, map_name, x, y, w, h, image, mask, text, objects_list):
        self.config = Config()
        pygame.sprite.DirtySprite.__init__(self)
        self.map_name = map_name
        self.rect = None
        self.decor = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.prompt = ""
        self.image = image
        self.mask = mask
        self.objects_list = objects_list
        self.title = self.text.font_sub.render("prompt: ", True, (0, 0, 0))
        self.prompt_input = self.text.font_sub.render(self.prompt, True, (0, 0, 0))
        width = self.title.get_width() + self.prompt_input.get_width() + 15
        height = self.title.get_height() + 6
        input_surface = pygame.Surface((width, height))
        input_surface.fill((255, 255, 255, 225))
        input_surface.blit(self.title, (6, 3))
        input_surface.blit(self.prompt_input, (self.title.get_width() + 3, 3))

        self.input_surface = input_surface
        self.rect = pygame.Rect(self.x, self.y, self.input_surface.get_width(),
                                self.input_surface.get_height())

        with open(self.config.folder.payloads+"payload.json", "r") as f:
            payloads = json.load(f)
        self.payload = payloads["payload"]
        self.url = payloads["url"]
        self.active = True

    # Create image using Stable diffusion
    def create_image(self):
        if self.id == 0:
            if len([x for x in self.objects_list if x.type == "decorIa"]) == 0:
                self.id = 1
            else:
                self.id = [x for x in self.objects_list if x.type == "decorIa"][-1].id + 1

        image = open(self.config.folder.temp+self.config.file.temp_capture, "rb").read()
        image_mask = open(self.config.folder.temp+self.config.file.temp_mask, "rb").read()
        self.payload["init_images"] = ["data:image/png;base64," + base64.b64encode(image).decode('UTF-8')]
        self.payload["mask"] = "data:image/png;base64," + base64.b64encode(image_mask).decode('UTF-8')
        self.payload["prompt"] = self.config.prompt.replace("%s", self.prompt)
        self.payload["width"] = self.w
        self.payload["height"] = self.h

        response = requests.post(url=f'{self.url}', json=self.payload)

        r = response.json()
        if not os.path.exists(self.config.folder.maps + self.map_name + self.config.folder.decor):
            os.makedirs(self.config.folder.maps + self.map_name + self.config.folder.decor)

        path = self.config.folder.maps + self.map_name + "/"+ self.config.folder.decor

        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
            self.mask = Image.open(self.config.folder.temp+self.config.file.temp_mask)
            image = image.convert('RGBA')
            self.mask = self.mask.convert('L')
            image.putalpha(self.mask)
            image_name = path + '/image_' + str(self.id) + '_' + str(self.x) + '_' + str(self.y) + '_' + str(
                self.w) + '_' + str(self.h) + '.png'
            image.save(image_name)

            if self.decor is None:
                self.decor = DecorIa(self.id, self.x, self.y, image)
            else:
                self.decor.set_image(image)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:

                    print(self.prompt)
                    self.create_image()

                elif event.key == pygame.K_BACKSPACE:
                    self.prompt = self.prompt[:-1]
                else:
                    if event.unicode.isalnum() or event.unicode == " " or event.unicode == "," or event.unicode == "." or event.unicode == "'":
                        self.prompt += event.unicode

    def update(self):
        self.prompt_input = self.text.font_sub.render(self.prompt, True, (0, 0, 0))
        width = self.title.get_width() + self.prompt_input.get_width() + 12
        height = self.title.get_height() + 6
        input_surface = pygame.Surface((width, height))
        input_surface.fill((255, 255, 255, 225))
        input_surface.blit(self.title, (6, 3))
        input_surface.blit(self.prompt_input, (self.title.get_width() + 3 + 6, 3))
        self.input_surface = input_surface
        self.rect.w = input_surface.get_width()

    def draw(self, screen, camera_x, camera_y):
        # Limit camera movement
        position_x = self.x + camera_x
        position_y = self.y - (self.title.get_height() + 6) + camera_y

        if position_x < 0:
            position_x = 10
        if position_y < 0:
            position_y = 10

        screen.blit(self.input_surface, (position_x, position_y))
        self.rect = pygame.Rect(position_x, position_y,
                                self.input_surface.get_width(), self.input_surface.get_height())
        pygame.draw.rect(screen, (224, 186, 123), self.rect, 2,
                         border_bottom_right_radius=5, border_bottom_left_radius=5,
                         border_top_right_radius=5, border_top_left_radius=5)