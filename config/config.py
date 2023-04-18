from types import SimpleNamespace
import pygame


class Config:
    def __init__(self):
        self.map = SimpleNamespace(
            # Window
            default_name="default",
            map_lines=20,
            map_columns=20,
            screen_width=1920,
            screen_height=1080,
            nb_roads=20,
            total_lines=71,
            total_columns=61
        )
        self.folder = SimpleNamespace(
            # Folder
            maps="maps/",
            temp="temp/",
            decor="decor/",
            decor_animated="decor_animated/",
            payloads="payloads/",
        )
        self.file = SimpleNamespace(
            # File
            temp_mask="shape_mask.png",
            temp_capture="shape_capture.png",
        )
        self.action = SimpleNamespace(
            # Action button unicode
            pause=pygame.K_F1,
            draw_decor=pygame.K_F2,
            time_speed_up=pygame.K_KP_PLUS,
            time_speed_down=pygame.K_KP_MINUS,
        )
        self.prompt = "3d render, isometric %s, octane render, by greg rutkowski"
        self.prompt_denoising_strength_animation = 0.2
        self.prompt_denoising_strength = 1




