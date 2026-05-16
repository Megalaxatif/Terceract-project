import pygame
from object import Game_object


class BrokenPipe(Game_object):
    def __init__(
        self,
        game_context,
        object_name,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        default_collision: pygame.Rect,
        default_wall: str,
        collision_index: int,
        movable: bool,
        displayed: bool,
        interactible: bool,
    ):
        super().__init__(
            game_context,
            object_name,
            image_path,
            rect,
            collisions,
            default_collision,
            default_wall,
            collision_index,
            movable,
            displayed
        )
        self.interactible = interactible           #fonctionne comme un closet mais avec 2 options
        self.unclogged = False
        self.open = not (self.name == "broken_pipe")
        self.background = "gray_bg" in self.name
        self.taken = False

    def initialize(self):
        self.menu_reference = self.game_context.get_reference("open_broken_pipe")
        self.bg_reference = self.game_context.get_reference("gray_bg_broken_pipe")
        self.pipe_reference = self.game_context.get_reference("broken_pipe")

    def swap_display(self):
        self.menu_reference.displayed = not self.menu_reference.displayed
        self.bg_reference.displayed = not self.bg_reference.displayed

    def handle_click_selection(self, event):
        if self.open and not self.pipe_reference.taken: #faire attention aux 3 objets qui sont broken pipe (obj, bg et menu), menu continue de s'ouvrir meme quand taken a cause de ca je pense
            if self.menu_reference.collision_rects[2].collidepoint(event.pos): #collision_rects[0] c le menu en entier
                self.pipe_reference.unclogged = True
                if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "broken_pipe", "unclogged", True)
                print("pipe unclogged")

            elif self.menu_reference.collision_rects[1].collidepoint(event.pos) and not self.pipe_reference.unclogged:
                print("still clogged")

            elif self.menu_reference.collision_rects[1].collidepoint(event.pos) and self.pipe_reference.unclogged:
                self.pipe_reference.taken = True
                if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "broken_pipe", "taken", True)
                    self.game_context.network_manager.send_package("variable", "broken_pipe", "movable", True) 
                self.pipe_reference.interactible = False
                self.pipe_reference.movable = True
                print("you took the pipe")  
            else :
                self.swap_display()
        elif not self.pipe_reference.unclogged or not self.pipe_reference.taken or self.background:
            print("swap here")
            self.swap_display()