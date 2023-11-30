import pygame
from support import import_folder
import time
from healthbar import Healthbar

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index=0
        self.animation_speed=0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect=self.image.get_rect(topleft = pos)
        self.prevx=pos[0]
        self.prevy=pos[1]

        self.direction = pygame.math.Vector2(0, 0)
        self.gravity=0.4
        self.jump_speed = -12
        self.health=50
        self.damage=5

        #self.healthbar=pygame.image.load('/home/siddharth-kini/PythonCode/Practice/graphics/Darkupdate.png')
        self.healthbar=pygame.sprite.GroupSingle()
        h=Healthbar(self, 'player', (self.rect.x, self.rect.y-10))
        self.healthbar.add(h)

        self.status='idle'
        self.facing_right=True
        self.on_ground=False
        self.attacking=False
        self.pushingright=False
        self.pushingleft=False
        self.climbing=False
        self.onrope=False
        self.taking_damage=False
        self.dead=False
        self.hasattacked=False

    def import_character_assets(self):
        character_path='/home/sarthak/Programming/PyLagu/level/graphics/character/'
        self.animations={'idle':[], 'run':[], 'jump':[], 'fall':[], 'attack':[], 'climb':[], 'take_hit':[], 'dead':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation]=import_folder(full_path, 'player')

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index+=self.animation_speed
        if self.frame_index >= len(animation):
            if self.status=='taking_hit':
                self.status='idle'
                self.taking_damage=False
            elif self.status=='dead':
                self.frame_index=len(animation)-1
            if not self.dead:
                self.frame_index=0

        image=animation[int(self.frame_index)]
        if self.facing_right:
            self.image=image
        else:
            flipped_image=pygame.transform.flip(image, True, False)
            self.image=flipped_image

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.taking_damage and (not self.dead):
            if keys[pygame.K_RIGHT]:
                if not self.attacking:
                    self.direction.x=1
                    self.facing_right=True
            elif keys[pygame.K_LEFT]:
                if not self.attacking:
                    self.direction.x=-1
                    self.facing_right=False
            else:
                self.direction.x=0

            if keys[pygame.K_UP]:
                self.frame_index=0
                self.jump()

            if keys[pygame.K_SPACE]:
                self.attacking=True
                self.startattack=pygame.time.get_ticks()
                self.frame_index=0
            
            if keys[pygame.key.key_code("S")] and self.onrope:
                self.rect.y+=1
            
            if keys[pygame.key.key_code("W")] and self.onrope:
                self.rect.y-=1

            if self.climbing and keys[pygame.key.key_code("D")]:
                self.onrope=True
                self.gravity=0
                self.direction.y=0
            else:
                self.gravity=0.4
                self.onrope=False
    

    def get_status(self):
        keys = pygame.key.get_pressed()
        if self.direction.y<0:
            self.status='jump'
        elif self.direction.y>1:
            self.status='fall'
        else:
            if self.direction.x!=0:
                self.status='run'
            else:
                self.status='idle'
        if self.attacking:
            self.status='attack'
            endattack=pygame.time.get_ticks()
            if(endattack-self.startattack>670):
                self.attacking=False
                self.hasattacked=False
            #pygame.time.set_timer(self.attacking=False, 700)
        if self.onrope:
            self.status='climb'
            if keys[pygame.key.key_code("W")] or keys[pygame.key.key_code("S")]:
                self.animation_speed=0.15
            else:
                self.animation_speed=0
        else:
            self.animation_speed=0.15

        if self.taking_damage:
            self.status='take_hit'
            self.direction.x=0
            self.taking_damage=False

        if self.health==0:
            self.status='dead'
            self.dead=True
        

    def apply_gravity(self):
        self.direction.y+=self.gravity
        self.rect.y+= self.direction.y

    def jump(self):
        if(self.on_ground or self.onrope):
            self.direction.y=self.jump_speed

    def update(self):
        #self.prevx=self.rect.left
        #self.prevy=self.rect.top
        self.get_input()
        self.get_status()
        self.animate()
        self.healthbar.sprite.update((self.rect.x+5 ,self.rect.y-20))