import pygame

class Popup(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], colour: str | tuple[int, int, int], text: str = '', icon: pygame.Surface | None = None, groups: list[pygame.sprite.Group] = []):
        super().__init__(*groups)


    def update(self):
        pass
            
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False