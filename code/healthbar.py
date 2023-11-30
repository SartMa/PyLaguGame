import pygame

class Healthbar(pygame.sprite.Sprite):
    def __init__(self, typ, h_typ, pos):
        super().__init__()
        self.typ=typ
        self.h_typ = h_typ
        if self.h_typ == 'eye':
            self.full_health = 10
        elif self.h_typ == 'boss':
            self.full_health = 50
        elif self.h_typ == 'player':
            self.full_health = 50
        else:
            self.full_health = 30

        self.image=pygame.image.load('/home/sarthak/Programming/PyLagu/level/graphics/healthbar.png').convert_alpha()
        self.rect=self.image.get_rect(topleft=pos)

    def update(self, pos):
        self.rect.topleft=pos
        health = (self.typ.health/self.full_health)*30
        self.blackvoid=pygame.Surface((30-health, 5))
        self.blackvoid.fill('black')
        self.blackrect=self.blackvoid.get_rect(topleft=pos)
        pygame.Surface.blit(self.image, self.blackvoid, (1+health, 15),(0,0,30-health, 5))