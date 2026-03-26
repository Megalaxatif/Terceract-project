import pygame  # Le module Pygame
from pygame.locals import *
import pygame.freetype  # Pour afficher du texte
import time

pygame.freetype.init()  # Initialisation des polices
pygame.mixer.init(frequency=44100, size=-16, channels=2)  # Initialisation du son

dialogue_sound = pygame.mixer.Sound("../data/sounds/dialogue.wav")
dialogue_sound.set_volume(0.7)

class Dialogue:
    def __init__(self, game_context):
        self.liste_dialogues = [
                                "WHAT WAS THIS NOISE ? WHERE AM I ?! THIS DOOR IS STUCK AND IT SEEMS TO BE THE ONLY EXIT..",
                                "SHIT! THAT HURT, AND IT DIDN'T EVEN WORK",
                                "WHY CAN'T I JUST GO BACK..?",
                                "WHAT'S THIS.. A PIECE OF VASE ? WHY IS IT BROKEN..",
                                "SOMETHING SOUNDS HOLLOW",
                                "AS GOOD AS NEW! IT'S LIKE IT WAS NEVER BROKEN..",
                                "...",
                                "I HEARD SOMETHING CLICK",
                                "IS THAT.. ?",
                                "ONE OFF, ONE MORE TO GO",
                                "THERE WAS A KEY BEHIND THE WALL !",
                                "SHIT, THAT HURT! I THINK I'M BLEEDING.. THIS WHOLE THING IS SO ANNOYING! AT LEAST THIS DOOR IS OPEN"
                                ]

        self.game_context = game_context
        self.complete = True
        self.c = 0  # compteur taille texte (afficher str par str)
        self.current_time = time.time()
        self.text_surface = None
        self.text_rect = None
        self.max_width = self.game_context.screen.get_width() * 0.5  # ajustement de la largeur maximale de la boîte de dialogue
        self.current_dialogue = 0
        self.height = self.game_context.screen.get_height()
        self.width = self.game_context.screen.get_width()
        self.end_time = None
        self.delay_after = 3
        self.visible = True
        self.box_height = None
        self.box_width = None
        self.box_rect = None


        # === Gestion des Polices ===
        self.font_path = '../data/nintendo-nes-font.otf' # Chargement police Nintendo NES
        self.font_size1 = int(13 * self.game_context.delta_w)

        # Chargement des polices avec différentes tailles
        self.small_font = pygame.font.Font(self.font_path, self.font_size1)

    def get_lines(self, text):
        """ Découpe le texte en lignes qui s'adaptent à la boîte """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if '\n' in word:  # Si le mot contient un saut de ligne
                parts = word.split('\n')
                for i, part in enumerate(parts):
                    test_line = current_line + part + " "
                    text_width, _ = self.small_font.size(test_line)

                    if text_width > self.max_width:
                        lines.append(current_line)
                        current_line = part + " "
                    else:
                        current_line = test_line

                    # Ajouter la ligne courante si on rencontre un '\n'
                    if i < len(parts) - 1:
                        lines.append(current_line.strip())
                        current_line = ""

            else:
                test_line = current_line + word + " "
                text_width, _ = self.small_font.size(test_line)

                if text_width > self.max_width:
                    lines.append(current_line)
                    current_line = word + " "
                else:
                    current_line = test_line

        # Ajouter la dernière ligne si elle n'est pas vide
        if current_line:
            lines.append(current_line)

        return lines

    def display(self):
        if not self.visible:
            return

        self.font_size1 = int(13 * self.game_context.delta_w)

        # Chargement des polices avec différentes tailles
        self.small_font = pygame.font.Font(self.font_path, self.font_size1)

        self.max_width = self.game_context.width * 0.5  # ajustement de la largeur maximale de la boîte de dialogue
        self.height = self.game_context.height
        self.width = self.game_context.width

        if self.complete:
            self.c = 0
            self.complete = False

        if not self.complete:
            # Définir quel texte afficher (jusqu'au compteur c)
            dialogue = self.liste_dialogues[self.current_dialogue][:self.c]
            lines = self.get_lines(dialogue)

            # Calculer la hauteur totale des lignes pour centrer verticalement
            total_height = len(lines) * self.small_font.get_height()
            y_offset = (self.height - total_height) // 2

            espace_entre_lignes = 5*self.game_context.delta_h  # espace entre les lignes

            # Dessiner d'abord le rectangle autour de la boîte de dialogue
            self.box_height = total_height + 20*self.game_context.delta_h
            self.box_width = self.max_width + 20*self.game_context.delta_w
            self.box_rect = pygame.Rect((self.width - self.box_width) // 2, y_offset + 150*self.game_context.delta_h, self.box_width, self.box_height + len(lines)*espace_entre_lignes)
        pygame.draw.rect(self.game_context.screen, (50, 50, 50), self.box_rect)  # On dessine d'abord la boîte

        # Afficher ensuite chaque ligne de texte avec l'espace supplémentaire
        for i, line in enumerate(lines):
            self.text_surface = self.small_font.render(line, True, (255,255,255))
            self.text_rect = self.text_surface.get_rect(midtop=(self.width / 2,
                                                               y_offset + i * (self.small_font.get_height() + espace_entre_lignes)
                                                               + 160*self.game_context.delta_h))
            self.game_context.screen.blit(self.text_surface, self.text_rect)

        # Gérer l'affichage progressif du texte
        if self.current_time + 0.05 < time.time():

            if self.c < len(self.liste_dialogues[self.current_dialogue]):
                self.c += 1
                dialogue_sound.play()

            self.current_time = time.time()

    def handle_event(self, event):
        if not self.visible:
            return
        # TODO: I got this error at a random start : AttributeError: 'NoneType' object has no attribute 'collidepoint'
        #                                                         -----------
        if event.type == pygame.MOUSEBUTTONDOWN and self.box_rect.collidepoint((pygame.mouse.get_pos())):
            if self.c >= len(self.liste_dialogues[self.current_dialogue]):
                self.visible = False
                self.complete = True