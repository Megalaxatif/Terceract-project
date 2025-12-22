import pygame
import xml.etree.ElementTree as ET

from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

# --- Chargement du XML ---
tree = ET.parse(f"{root_dir}/data/dialogues/dtest.xml")
root = tree.getroot()

pygame.font.init()
font_test = pygame.font.SysFont('Comic Sans MS', 30)
text_interact = font_test.render('Press E to interact', False, (255, 255, 255))

class Entities(pygame.sprite.Sprite):
    def __init__(self, initial_posx, initial_posy, sprite_img, id, displayed, mini_game_access):
        super().__init__()
        if sprite_img is not None:
            self.sprite = sprite_img
        else:
            self.sprite = pygame.Surface((40, 40))
            self.sprite.fill((0, 255, 0))

        self.rect = sprite_img.get_rect() if sprite_img is not None else pygame.Rect(400, 400, 40, 40)
        self.rect.x = initial_posx if initial_posx is not None else 0
        self.rect.y = initial_posy if initial_posy is not None else 0
        self.entities_id = id
        self.is_displayed = displayed
        self.radius = 100
        # TODO bien centrer le carree
        self.interact_area_rect = pygame.Rect(0, 0, self.rect.width + 2*self.radius, self.rect.height + 2*self.radius)
        self.interact_area_rect.center = self.rect.center
        self.interact_area = pygame.Surface(self.interact_area_rect.size)
        self.mini_game_origin = None
        self.mini_game_access = mini_game_access

    def npc_collision(self, player):
        return self.rect.colliderect(player)

    def npc_interact(self, player, screen, game, new):
        if self.interact_area_rect.colliderect(player):
            screen.blit(text_interact, (100,100))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.apply_node(root, game)
                #game.current_mini_game = new.name       

    def is_entity_displayed(self):
        return self.is_displayed

    def get_posX(self):
        return self.rect.x

    def get_posY(self):
        return self.rect.y

    
    # dialogues:

    def display_message(self, node):
        msg = node.find("message")
        if msg is not None:
            print("\nPNJ :", msg.text.strip())

    def apply_game_properties(self, node, game):
        props = node.find("game_properties")
        if props is not None:
            for prop in props:
                if prop.tag == "launch_mini_game":
                    game.current_mini_game = prop.text.strip()
                print(f"[GAME] {prop.tag} = {prop.text.strip()}")

    def apply_node(self, node, game):
        if node.tag == "conversation":
            start = node.find("start")
            print("PNJ :", start.text.strip())
            choices = node.findall("choice")
        else:
            self.display_message(node)
            self.apply_game_properties(node, game)
            choices = node.findall("choice")

        if not choices:
            print("\n[FIN DU DIALOGUE]")
            return

        while True:
            print()
            for i, choice in enumerate(choices, start=1):
                print(f"{i} - {choice.attrib['text']}")

            try:
                index = int(input("\n> ")) - 1
                if index < 0 or index >= len(choices):
                    raise ValueError
            except ValueError:
                print("Choix invalide.")
                continue
    
            self.apply_node(choices[index], game)
            return


