import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int], colour: str | tuple[int, int, int], text: str = '', icon: pygame.Surface | None = None, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        if icon:
            self.image.blit(pygame.transform.scale(icon, size))
        else:
            self.image.fill(colour)
        
        self.font = pygame.font.SysFont('arial', 20)
        self.image.blit(self.font.render(text, False, 'black'))
            
        self.rect: pygame.Rect = self.image.get_rect()
        
        self.originalImage: pygame.Surface = self.image
        self.darkeningSurface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        self.darkeningSurface.fill((0, 0, 0, 120))
        
        self.active: bool = True
        self.pressed: bool = False

    def update(self):
        mousePos = pygame.mouse.get_pos()
        mouseStates = pygame.mouse.get_just_pressed()
        if not self.active:
            return None
            
        self.pressed = False
        if self.rect.collidepoint(mousePos) and mouseStates[0]:
            self.pressed = True
            
        self.image.blit(self.originalImage)
        if self.pressed:
            self.image.blit(self.darkeningSurface)
            
    def isPressed(self):
        return self.pressed
            
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False
            