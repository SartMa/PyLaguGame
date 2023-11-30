import pygame
from support import import_folder

class Tiles(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, shift):
        self.rect.x += shift
        #Y scroll to be added

class StaticTile(Tiles):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

# class Crate(StaticTile):
#     def __init__(self, size, x, y):
#         super().__init__()

class AnimatedTile(Tiles):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self,shift):
        self.animate()
        self.rect.x += shift
        #Y scroll to be added

class Key(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '/home/sarthak/Programming/PyLagu/level/graphics/key')
        self.display = False
        self.iscollected = False

    def update(self, shift):
        if self.display == True:
            self.animate()
        self.rect.x += shift


class Chest(AnimatedTile):
    def __init__(self, size, x, y, path, surface):
        super().__init__(size, x, y, path)
        self.surface = surface
        self.can_open = False
        self.key = Key(size, x, y-10)
        self.key_sprite = pygame.sprite.GroupSingle()
        self.key_sprite.add(self.key)
    
    def get_player_distance(self, player):
        crate_pos = pygame.math.Vector2(self.rect.topleft)
        player_pos = pygame.math.Vector2(player.rect.center)
        return (player_pos-crate_pos).magnitude()
    
    def get_key_distance(self, player):
        key_pos = pygame.math.Vector2(self.key.rect.center)
        player_pos = pygame.math.Vector2(player.rect.center)
        return (key_pos-player_pos).magnitude()

    def animate(self):
        if self.can_open == True:
            self.frame_index += 0.25
            if self.frame_index >= len(self.frames):
                self.image = self.frames[len(self.frames)-1]
                # self.key_sprite.update()
                self.key.display = True
                self.key_sprite.draw(self.surface)
            else:
                self.image = self.frames[int(self.frame_index)]

    def update(self, shift, player):
        keys = pygame.key.get_pressed()

        distance = self.get_player_distance(player)
        if distance in range(0,100):
            self.can_open = True
        self.animate()
        if pygame.Rect.colliderect(player.rect, self.key.rect) and keys[pygame.key.key_code("K")]:
            self.key.kill()
        
        self.key_sprite.update(shift)
        self.rect.x += shift

class bg_effects(AnimatedTile):
    pass

class final_boss(AnimatedTile):
    pass

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('/home/sarthak/Programming/PyLagu/level/graphics/block.png')
        self.image = pygame.transform.scale(self.image, (64,64))
        self.rect=self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity=0.4
        self.prevx=pos[0]
        self.prevy=pos[1]
        self.enable=1
        self.beingpushed=False

    def apply_gravity(self):
        self.direction.y+=self.gravity
        self.rect.y+= self.direction.y

    def update(self, x_shift):
        self.prevx=self.rect.x
        self.prevy=self.rect.y
        self.rect.x += (x_shift)

class Rope(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('/home/sarthak/Programming/PyLagu/level/graphics/ladder.png')
        # self.image = pygame.transform.scale(self.image)
        self.rect=self.image.get_rect(topleft=pos)
    def update(self, x_shift):
        self.rect.x += (x_shift)