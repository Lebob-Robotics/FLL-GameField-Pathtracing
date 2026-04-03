import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], colour: str | tuple[int, int, int], text: str = '', icon: pygame.Surface | None = None, groups: list[pygame.sprite.Group] = []):
        super().__init__(*groups)
        self.image: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(self.image, colour, (0, 0, *size), border_radius = 5)
        if icon:
            image_buffer = size[0] // 10
            self.image.blit(pygame.transform.scale(icon, [dimension - image_buffer * 2 for dimension in size]), (image_buffer, image_buffer))
        
        self.font = pygame.font.SysFont('arial', 20)
        self.image.blit(self.font.render(text, False, 'black'))
            
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = position
        
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

            
    def is_pressed(self):
        return self.pressed
            
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False
            