import pygame
class Wall:
    def __init__(self, game_context, background_layer_path : str | None, interactable_layers_path : list[str] | None ):
        #explanation:
        #background_layer_path is a path to a static image that cannot move
        #interactable_layers is a list of the path to the entities to be displayed on the wall
        self.game_context = game_context
        self.background = pygame.image.load(background_layer_path) if background_layer_path is not None else pygame.Surface(self.game_context.screen.get_size())
        if background_layer_path is None: self.background.fill((255, 0, 0))
        self.entities = pygame.sprite.Group
        #TODO: we need to find the coordinates and dimensions of each object on the images in interactable_layers (by using masks most likely)
        # and put them in entities

        # first we load the raw images with their path in interactable_layers_path
        # then find the bounding rect of the sprite and its image
        # then create an object associated to the name of the image and give the bouding rect and the image as argument
        # then add the object to entities


    #TODO: reuse the code of cyberfrog to make a function that moves an object centered on 
    #the mouse position and that check collisions with the screen border and the other objects in entities
    def move_object(self):
        pass

    def update(self):
        #print("update error : function not implemented for subclass of Wall")
        self.game_context.screen.blit(self.background, (0,0))
        #pass