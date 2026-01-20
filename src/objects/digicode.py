import pygame
from object import Object

class Digicode(Object):
    def __init__(self, game_context, image_path, rect, secret_code="1234"):
        super().__init__(game_context, "digicode", image_path, rect, [])
        self.pos = rect[0], rect[1]
        self.x, self.y = self.pos
        self.delta = 1

        # Digicode
        self.secret_code = secret_code
        self.entered_code = ""
        self.message = ""
        self.displayed = True # True = image visible, False = digicode ouvert
        self.dragging = False

        # Police et couleurs
        self.font = pygame.font.SysFont(None, 40)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.DARK = (50, 50, 50)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)

        # Boutons du digicode
        self.buttons = ["1","2","3","4","5","6","7","8","9","C","0","OK"]
        self.button_rects = []
        
        self.close_rect = pygame.Rect(self.x + 220*self.delta, self.y + 10*self.delta, 40*self.delta, 40*self.delta)

    def create_buttons(self, pos):
        x0, y0 = pos[0] + 30, pos[1] + 120
        w, h = 70, 50
        gap = 10
        self.button_rects.clear()
        for i, text in enumerate(self.buttons):
            x = x0 + (i % 3) * (w + gap)
            y = y0 + (i // 3) * (h + gap)
            self.button_rects.append((pygame.Rect(x*self.delta, y*self.delta, w*self.delta, h*self.delta), text))

    def draw(self):
        if self.displayed:
            self.screen.blit(self.image, self.rect)
            return
        self.delta = self.game_context.current_wall.delta
        self.x, self.y = self.pos[0]*self.delta, self.pos[1]*self.delta
        # Digicode ouvert
        pygame.draw.rect(self.screen, (200,200,0), (self.rect.x, self.rect.y, 300 *self.delta, 400*self.delta))

        # Bouton fermer
        pygame.draw.rect(self.screen, self.RED, self.close_rect)
        x_label = self.font.render("X", True, self.WHITE)
        self.screen.blit(x_label, x_label.get_rect(center=self.close_rect.center))

        # Code
        code_surface = self.font.render(self.entered_code, True, self.DARK)
        self.screen.blit(code_surface, (self.rect.x + 30*self.delta, self.rect.y + 40*self.delta))

        # Message
        if self.message:
            color = self.GREEN if self.message == "OK !" else self.RED
            msg_surface = self.font.render(self.message, True, color)
            self.screen.blit(msg_surface, (self.rect.x + 30*self.delta, self.rect.y + 80*self.delta))

        # Boutons
        self.create_buttons(self.pos)
        self.close_rect = pygame.Rect(self.x + 220*self.delta, self.y + 10*self.delta, 40*self.delta, 40*self.delta)
        for rect, text in self.button_rects:
            pygame.draw.rect(self.screen, self.GRAY, rect)
            label = self.font.render(text, True, self.DARK)
            self.screen.blit(label, label.get_rect(center=rect.center))

    def handle_event(self, event):
        if not event or event.type != pygame.MOUSEBUTTONDOWN:
            return

        # clic sur image
        if self.displayed:
            if self.rect.collidepoint(event.pos):
                self.displayed = False
                print("Komputer opened")
            return

        # bouton fermer
        if self.close_rect.collidepoint(event.pos):
            self.displayed = True
            self.entered_code = ""
            self.message = ""
            print("Komputer closed")
            return

        # Boutons
        for rect, text in self.button_rects:
            if rect.collidepoint(event.pos):
                if text == "C":
                    self.entered_code = ""
                    self.message = ""
                elif text == "OK":
                    self.message = "OK !" if self.entered_code == self.secret_code else "Erreur"
                    self.entered_code = ""
                else:
                    if len(self.entered_code) < 6:
                        self.entered_code += text
