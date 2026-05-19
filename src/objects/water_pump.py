import pygame
from object import Game_object

class WaterPump(Game_object):
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
            movable=False,
            displayed=True,
        )

        self.disabled = True #a remettre a true a la fin
        self.water_count = 0 #remplir la pump
        self.leaking = True #boucher trous
        self.pipe_fixed = False #remettre morceau manquant

    def initialize(self):
        self.wallet_reference = self.game_context.get_reference("wallet")

    def water_increase(self, i):
        self.water_count += int(i)

    #def update(self, event):
        #print(f"water count : {self.water_count}, leaking : {self.leaking}, pipe fixed : {self.pipe_fixed}")
        #if not self.leaking and self.water_count >= 4 and self.pipe_fixed: #faudra remettre 4 a la fin
            #self.disabled = False
            #print("pump not disabled anymore")

    def handle_click_selection(self, event):
        if not self.leaking and self.water_count >= 3 and self.pipe_fixed: #and self.rect.collidepoint(event.pos) and self.game_context.current_room_id == 3 and self.game_context.current_wall_id == 0:
            self.wallet_reference.displayed = True
            self.game_context.dialogues.start_dialogue(20) #wallet appears
        elif self.leaking:
            self.game_context.dialogues.start_dialogue(17) #pump is leaking
        elif self.water_count < 3:
            self.game_context.dialogues.start_dialogue(16) #pump not full
        elif not self.pipe_fixed:
            self.game_context.dialogues.start_dialogue(18) #pipe not fixed