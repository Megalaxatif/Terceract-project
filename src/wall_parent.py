import pygame
class Wall:
    def __init__(self, game_context, background_layer_path : str | None, interactable_layers : list[pygame.Surface] | None ):
        #explanation:
        #background_layer_path is a path to a static image that cannot move
        #interactable_layers is a list of all the object layers
        #TODO: we need to find the coordinates and dimensions of each object on the images in interactable_layers (by using masks most likely)
        # and put them in entities
        self.game_context = game_context
        self.background = pygame.image.load(background_layer_path) if background_layer_path is not None else pygame.Surface(self.game_context.screen.get_size())
        if background_layer_path is None: self.background.fill((255, 0, 0))
        self.entities = None # TODO: change this
        
    #TODO: reuse the code of cyberfrog to make a function that moves an object centered on 
    #the mouse position and that check collisions with the screen border and the other object in entities
    def move_object(self):
        pass

    def update(self):
        #print("update error : function not implemented for subclass of Wall")
        self.game_context.screen.blit(self.background, (0,0))