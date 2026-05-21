import pygame
import pygame.freetype
from pygame.locals import *

pygame.freetype.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)

dialogue_sound = pygame.mixer.Sound("../data/sounds/dialogue.wav")
dialogue_sound.set_volume(0.7)


class Dialogue:
    def __init__(self, game_context):
        self.game_context = game_context

        self.dialogues_list = [
            "WHAT WAS THIS NOISE ? WHERE AM I ?! THIS DOOR IS STUCK AND IT SEEMS TO BE THE ONLY EXIT..",
            "SHIT! THAT HURT, AND IT DIDN'T EVEN WORK", #useless
            "WHY CAN'T I JUST GO BACK..?", #useless
            "WHAT'S THIS.. A PIECE OF VASE ? WHY IS IT BROKEN..", #useless
            "SOMETHING SOUNDS HOLLOW..?", #(fait)  DEMANDER A NOAH
            "AS GOOD AS NEW! IT'S LIKE IT WAS NEVER BROKEN..", #index 5 (useless)
            "...", #(useless)
            "THAT'S LOCKED", #(fait)
            "THERE'S A KEYCARD !", #(fait)
            "IT'S OPEN !", #(fait)
            "THERE WAS A KEY BEHIND THE WALL !", #index 10 (fait)
            "SHIT, THAT HURT! I THINK I'M BLEEDING.. THIS WHOLE THING IS SO ANNOYING! AT LEAST THIS DOOR IS OPEN", #nul

            "I FOUND SOMETHING.. THIS IS DISGUSTING", #index 12 (fait)
            "I CAN'T REACH !", #(fait)
            "I FILLED THE BOTTLE", #(fait)
            "I EMPTIED THE BOTTLE IN THE PUMP", #(fait)
            "WATER IS MISSING", #(fait)
            "IT'S LEAKING EVERYWHERE", #(fait)
            "THE PIPE IS MISSING A PIECE", #(fait)
            "IT'S FULL", #(fait)
            "I HEARD SOMETHING DROP FAR AWAY, MAYBE IF I FOLLOW THE PIPES...", #index 20 (fait)
            "THE DOOR IS UNLOCKED", #(fait)
            "THE BOTTLE IS ALREADY FILLED", #(fait)
            "THE BOTTLE IS EMPTY", #(fait)
            "IT'S EMPTY.. I THINK I SAW A WATER BOTTLE IN THE FIRST ROOM", #(fait)

            "THERE WAS SOMETHING BEHIND THE WALL !", #index 25 (fait)
            "THE DOOR.. IS FINALLY OPEN" #(fait)
            ]

        self.visible = True
        self.complete = True
        self.current_dialogue = 0
        self.c = 0

        self.delay_per_char = 50      # ms
        self.delay_after = 3000       # ms
        self.last_char_time = 0

        self.font_path = "../data/nintendo-nes-font.otf"
        self.font_size = 0
        self.small_font = None

        self.max_width = 0
        self.box_rect = None
        self.lines = []

        self.update_layout(force=True)

    def update_layout(self, force=False):
        new_font_size = int(13 * self.game_context.delta_w)
        new_max_width = self.game_context.width * 0.5

        need_update = (
            force
            or new_font_size != self.font_size
            or new_max_width != self.max_width
        )

        if not need_update:
            return

        self.font_size = new_font_size
        self.small_font = pygame.font.Font(self.font_path, self.font_size)
        self.max_width = new_max_width

        self.rebuild_text()

    def rebuild_text(self):
        if not self.visible:
            self.lines = []
            self.box_rect = None
            return

        full_text = self.dialogues_list[self.current_dialogue]
        visible_text = full_text[:self.c]
        self.lines = self.get_lines(visible_text)

        screen_w = self.game_context.width
        screen_h = self.game_context.height
        line_h = self.small_font.get_height()
        line_spacing = int(5 * self.game_context.delta_h)

        total_height = len(self.lines) * line_h
        y_offset = (screen_h - total_height) // 2

        box_height = total_height + 20 * self.game_context.delta_h + len(self.lines) * line_spacing
        box_width = self.max_width + 20 * self.game_context.delta_w

        self.box_rect = pygame.Rect(
            (screen_w - box_width) // 2,
            y_offset + 150 * self.game_context.delta_h,
            box_width,
            box_height
        )

    def get_lines(self, text):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            if "\n" in word:
                parts = word.split("\n")
                for i, part in enumerate(parts):
                    test_line = current_line + part + " "
                    text_width, _ = self.small_font.size(test_line)

                    if text_width > self.max_width and current_line:
                        lines.append(current_line.rstrip())
                        current_line = part + " "
                    else:
                        current_line = test_line

                    if i < len(parts) - 1:
                        lines.append(current_line.rstrip())
                        current_line = ""
            else:
                test_line = current_line + word + " "
                text_width, _ = self.small_font.size(test_line)

                if text_width > self.max_width and current_line:
                    lines.append(current_line.rstrip())
                    current_line = word + " "
                else:
                    current_line = test_line

        if current_line:
            lines.append(current_line.rstrip())

        return lines

    def start_dialogue(self, index):
        if 0 <= index < len(self.dialogues_list):
            self.current_dialogue = index
            self.c = 0
            self.complete = False
            self.visible = True
            self.last_char_time = pygame.time.get_ticks()
            self.rebuild_text()

    def update(self):
        if not self.visible:
            return

        self.update_layout()

        if self.complete:
            self.complete = False
            self.c = 0
            self.last_char_time = pygame.time.get_ticks()
            self.rebuild_text()

        now = pygame.time.get_ticks()
        full_text = self.dialogues_list[self.current_dialogue]

        if self.c < len(full_text) and now - self.last_char_time >= self.delay_per_char:
            self.c += 1
            self.last_char_time = now
            self.rebuild_text()

            if full_text[self.c - 1] not in " \n":
                dialogue_sound.play()

    def display(self):
        if not self.visible or not self.box_rect:
            return

        screen = self.game_context.screen
        screen_w = self.game_context.width
        screen_h = self.game_context.height

        line_h = self.small_font.get_height()
        line_spacing = int(5 * self.game_context.delta_h)
        total_height = len(self.lines) * line_h
        y_offset = (screen_h - total_height) // 2

        pygame.draw.rect(screen, (50, 50, 50), self.box_rect)

        for i, line in enumerate(self.lines):
            text_surface = self.small_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                midtop=(
                    screen_w / 2,
                    y_offset + i * (line_h + line_spacing) + 160 * self.game_context.delta_h
                )
            )
            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if not self.visible or self.box_rect is None:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box_rect.collidepoint(event.pos):
                if self.c >= len(self.dialogues_list[self.current_dialogue]):
                    self.visible = False
                    self.complete = True