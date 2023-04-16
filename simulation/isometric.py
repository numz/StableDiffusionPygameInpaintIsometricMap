import pygame
import os


class SpritesIsometric:
    # change font color
    road_type = {}
    sprites = {}
    decor = {}
    road_decor_cross = {}
    road_decor_threeway_right = {}
    icons = {}
    bus = {}
    car = {}
    tile_width = 128
    move_x_x = 63
    move_x_y = 63
    move_y_x = 36
    move_y_y = 36
    start_x = 20
    start_y = 20

    def __init__(self):
        self.background = pygame.image.load("assets/Textures/parchmentBasic.png").convert()
        self.background = pygame.transform.scale(self.background, (5120, 5120))

        # Chargement des sprites
        straight_down = pygame.image.load("assets/roads/road_02.png").convert_alpha()
        straight_right = pygame.image.load("assets/roads/road_01.png").convert_alpha()

        corner_up = pygame.image.load("assets/roads/road_14.png").convert_alpha()
        corner_right = pygame.image.load("assets/roads/road_15.png").convert_alpha()
        corner_left = pygame.image.load("assets/roads/road_12.png").convert_alpha()
        corner_down = pygame.image.load("assets/roads/road_13.png").convert_alpha()

        cross = pygame.image.load("assets/roads/road_03.png").convert_alpha()

        # rotate straight

        three_way_up = pygame.image.load("assets/roads/road_07.png").convert_alpha()
        three_way_right = pygame.image.load("assets/roads/road_06.png").convert_alpha()
        three_way_left = pygame.image.load("assets/roads/road_04.png").convert_alpha()
        three_way_down = pygame.image.load("assets/roads/road_05.png").convert_alpha()

        self.road_type = {
            "0": straight_down,
            "1": straight_right,
            "2": corner_right,
            "3": corner_left,
            "4": corner_down,
            "5": corner_up,
            "6": cross,
            "7": three_way_up,
            "8": three_way_right,
            "9": three_way_left,
            "10": three_way_down
        }

        # create empty image transparent 64x64

        nothing = pygame.Surface((128, 128), pygame.SRCALPHA)
        nothing.fill((0, 0, 0, 0))

        road = pygame.image.load("assets/roads/road_57.png").convert_alpha()

        self.sprites = {"0": nothing,
                        "1": road,
                        }
        # create self.decor dict with file in folder decor
        k = 0
        with os.scandir("assets/decor_road/cross/") as entries:
            for entry in entries:
                if os.path.isfile(entry):
                    # print(entry.name)
                    self.road_decor_cross[str(k)] = pygame.image.load(
                        "assets/decor_road/cross/" + entry.name).convert_alpha()
                    k += 1

        k = 0
        with os.scandir("assets/decor_road/threeway/right") as entries:
            for entry in entries:
                if os.path.isfile(entry):
                    # print(entry.name)
                    self.road_decor_threeway_right[str(k)] = pygame.image.load(
                        "assets/decor_road/threeway/right/" + entry.name).convert_alpha()
                    k += 1

        # create self.decor dict with file in folder decor
        k = 0
        with os.scandir("assets/decors") as entries:
            for entry in entries:
                if os.path.isfile(entry):
                    # print(entry.name)
                    self.decor[str(k)] = pygame.image.load("assets/decors/" + entry.name).convert_alpha()
                    k += 1

        bus_right = pygame.image.load("assets/bus/iso_right.png").convert_alpha()
        bus_left = pygame.image.load("assets/bus/iso_left.png").convert_alpha()
        bus_up = pygame.image.load("assets/bus/iso_up.png").convert_alpha()
        bus_down = pygame.image.load("assets/bus/iso_down.png").convert_alpha()
        self.bus = {
            "right": bus_right,
            "left": bus_left,
            "up": bus_up,
            "down": bus_down
        }

        car_left = pygame.image.load("assets/car/iso_left.png").convert_alpha()
        car_right = pygame.image.load("assets/car/iso_right.png").convert_alpha()
        car_up = pygame.image.load("assets/car/iso_up.png").convert_alpha()
        car_down = pygame.image.load("assets/car/iso_down.png").convert_alpha()
        self.car = {
            "right": car_right,
            "left": car_left,
            "up": car_up,
            "down": car_down,
        }