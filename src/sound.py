import pygame


class SoundManager:
    def __init__(self, game_context):
        self.game_context = game_context
        self.sounds = {
            "locked_door": pygame.mixer.Sound(
                f"{self.game_context.root_dir}/assets/sounds/locked_door.ogg"
            ),
        }

    def play_sound(self, name):
        self.sounds[name].play()
