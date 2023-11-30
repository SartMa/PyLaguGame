import pygame
from support import import_csv_layout, import_cut_graphics, import_folder
from settings import tile_size, screen_width
from tiles import Tiles, StaticTile, AnimatedTile, Chest, Block, Rope
import level_data
from enemy import Enemy, Boss, Eye, Skeleton
from player import Player

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0
        level_layout = import_csv_layout(level_data['level'])
        background_layout = import_csv_layout(level_data['level_bg'])
        enemy_constraint_layout = import_csv_layout(level_data['enemy_constraint'])
        enemy_layout = import_csv_layout(level_data['enemy'])
        enemy2_layout = import_csv_layout(level_data['enemy2'])
        player_layout = import_csv_layout(level_data['player'])
        chest_layout = import_csv_layout(level_data['chest'])
        block_layout = import_csv_layout(level_data['block'])
        ladder_layout = import_csv_layout(level_data['ladder'])
        enemy3_layout = import_csv_layout(level_data['enemy3'])

        self.level_sprites = self.create_tile_group(level_layout, 'level')
        self.background_sprites = self.create_tile_group(background_layout, 'background')
        self.enemy_constraint_sprites = self.create_tile_group(enemy_constraint_layout, 'enemy_constraint')
        self.enemy_layout_sprites = self.create_tile_group(enemy_layout, 'enemy')
        self.enemy2_layout_sprites = self.create_tile_group(enemy2_layout, 'enemy2')
        self.enemy3_layout_sprites = self.create_tile_group(enemy3_layout, 'enemy3')
        print(self.enemy3_layout_sprites)
        self.blocks = self.create_tile_group(block_layout, 'block')
        self.ropes = self.create_tile_group(ladder_layout, 'ladder')
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.enemy2_layout_sprites)
        self.enemies.add(self.enemy_layout_sprites)
        self.enemies.add(self.enemy3_layout_sprites)
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        self.chest_layout_sprites = self.create_tile_group(chest_layout, 'chest')
    
    def scroll_x(self):

        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        s=3

        if player_x < screen_width/3 and direction_x<0:
            self.world_shift = s
            player.speed= 0 
        elif player_x > 2*screen_width/3 and direction_x > 0:
            self.world_shift = -s
            player.speed = 0
        else:
            self.world_shift=0
            player.speed=s

    def horizontal_movement_collisions(self):
        player = self.player.sprite
        player.rect.x += player.direction.x*player.speed

        for block in self.blocks.sprites(): #block-player collision
            if block.rect.colliderect(player.rect):
                if player.direction.x<0:
                    #player.rect.left=block.rect.right
                    if block.enable:
                        block.rect.right=player.prevx-7
                        player.pushingleft=True
                        block.beingpushed=True
                        break
                    else:
                        player.rect.left=block.rect.right
                elif player.direction.x>0:
                    #player.rect.right = block.rect.left
                    if block.enable:
                        block.rect.left=player.prevx+player.rect.width+7
                        player.pushingright=True
                        block.beingpushed=True
                        break
                    else:
                        player.rect.right=block.rect.left

        for sprite in self.level_sprites.sprites(): #tile-player collision
            if sprite.rect.colliderect(player.rect):
                if player.direction.x<0:
                    player.rect.left=sprite.rect.right
                elif player.direction.x>0:
                    player.rect.right = sprite.rect.left
            for block in self.blocks.sprites(): #block-tile collision
                if block.enable:
                    if sprite.rect.colliderect(block.rect):
                        block.enable=0
                        if player.direction.x<0:
                            #print("collision")
                            #print("Collision")#need to change block position with direction not just place it next to the player. after all if two things are in contact they have the same vel
                            #player.rect.left=sprite.rect.right+block.rect.width
                            block.rect.left=sprite.rect.right
                        elif block.direction.x>0:
                            block.rect.right = sprite.rect.left

        
        for block in self.blocks.sprites():
            if block.beingpushed:
                if player.pushingleft and (player.direction.x>=0 or player.rect.bottom<block.rect.top or player.rect.top>block.rect.bottom):
                    player.pushingleft=False
                    block.beingpushed=False
                if player.pushingright and (player.direction.x<=0 or player.rect.bottom<block.rect.top or player.rect.top>block.rect.bottom):
                    player.pushingright=False
                    block.beingpushed=False
                break
        #print(player.pushingright, player.pushingleft)


    def vertical_movement_collisions(self):
        player=self.player.sprite
        player.apply_gravity()
        for sprite in self.level_sprites.sprites():  #tile - player collision
            if sprite.rect.colliderect(player.rect):
                if player.direction.y<0:
                    player.rect.top=sprite.rect.bottom
                    player.direction.y=0
                elif player.direction.y>0:
                    player.rect.bottom=sprite.rect.top
                    player.direction.y=0
                    player.on_ground=True
        for block in self.blocks.sprites(): #block-tile collision
            if block.enable:
                block.apply_gravity()
                for sprite in self.level_sprites.sprites():
                    if block.rect.colliderect(sprite.rect):
                        if block.direction.y<0:
                            block.rect.top=sprite.rect.bottom
                            block.direction.y=0
                        elif block.direction.y>0:
                            block.rect.bottom=sprite.rect.top
                            block.direction.y=0
        for sprite in self.blocks.sprites():  #block-player collision
            if sprite.rect.colliderect(player.rect):
                if player.direction.y<0:
                    player.rect.top=sprite.rect.bottom
                    player.direction.y=0
                elif player.direction.y>0:
                    player.rect.bottom=sprite.rect.top
                    player.direction.y=0
                    player.on_ground=True
            
        if player.on_ground and player.direction.y<0 or player.direction.y>1:
            player.on_ground=False        

                    

    def check_rope_collisions(self):
        player = self.player.sprite

        for rope in self.ropes.sprites():
            if rope.rect.colliderect(player.rect):
                if player.rect.top>rope.rect.top and player.rect.bottom<=rope.rect.bottom:
                    player.climbing=True
                    break
                else:
                    player.climbing=False
            else:
                player.climbing=False
            if rope.rect.top==player.rect.top:
                player.climbing=False
                player.jump()

    def handle_enemy_collisions(self):
        for enemy in self.enemies.sprites():
            player=self.player.sprite
            #print(enemy.attacking, enemy.frame_index, enemy.rect.colliderect(player.rect))
            if enemy.attacking:
                if ((enemy.frame_index>=6 and enemy.frame_index<=9) and enemy.rect.colliderect(player.rect)):
                    player.taking_damage=True
                    if not enemy.hasattacked:
                        player.health-=enemy.damage
                        if player.health<=0:
                            player.health=0
                        enemy.hasattacked=True
            if enemy.status=='idle':
                if player.attacking and player.frame_index>=3 and player.frame_index<4 and player.rect.colliderect(enemy.hitbox):
                    enemy.taking_damage=True
                    if not player.hasattacked:
                        enemy.health-=player.damage
                        if enemy.health<=0:
                            enemy.health=0
                        player.hasattacked=True
    
    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y))
                    self.player.add(sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val!='-1':
                    x = tile_size * col_index
                    y = tile_size * row_index
                    if type == 'level':
                        level_tile_list = import_cut_graphics('/home/sarthak/Programming/PyLagu/level/graphics/inca_front.png')
                        tile_surface = level_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == 'background':
                        background_tile_list = import_cut_graphics('/home/sarthak/Programming/PyLagu/level/graphics/inca_back2.png')
                        tile_surface = background_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == 'enemy_constraint':
                        sprite = Tiles(tile_size,x,y)
                        sprite_group.add(sprite)
                    
                    if type == 'enemy':
                        # print(tile_size, x, y)
                        # enemy_tile_list = import_cut_graphics('/enemy.png')
                        # tile_surface = enemy_tile_list[int(val)]
                        sprite = Boss((x, y))
                        sprite_group.add(sprite)
                    
                    if type == 'enemy2':
                        sprite = Eye((x,y))
                        sprite_group.add(sprite)
                    
                    if type == 'enemy3':
                        print('ok')
                        sprite = Skeleton((x,y))
                        sprite_group.add(sprite)
                    
                    # if type == 'player':
                    #     player_tile_list = import_cut_graphics('/home/sarthak/Programming/PyLagu/level/graphics/inca_back2.png')
                    #     tile_surface = player_tile_list[int(val)]
                    #     sprite = Player((x, y))
                    #     self.player.add(sprite)
                    if type == 'block':
                        sprite = Block((x,y), tile_size)
                        sprite_group.add(sprite)

                    if type == 'ladder':
                        sprite = Rope((x,y), tile_size)
                        sprite_group.add(sprite)
                    
                    if type == 'chest':
                        player_tile_list = import_cut_graphics('/home/sarthak/Programming/PyLagu/level/graphics/chest/tile000.png')
                        sprite = Chest(tile_size, x, y, '/home/sarthak/Programming/PyLagu/level/graphics/chest', self.display_surface)
                        sprite_group.add(sprite)

        return sprite_group
    
    def enemy_constraint(self):
            for enemy in self.enemies.sprites():
                enemy.healthbar.draw(self.display_surface)
                if pygame.sprite.spritecollide(enemy,self.enemy_constraint_sprites,False):
                    enemy.reverse()
            # for enemy in self.enemy2_layout_sprites.sprites():
            #     enemy.healthbar.draw(self.display_surface)
            #     if pygame.sprite.spritecollide(enemy,self.enemy_constraint_sprites,False):
            #         enemy.reverse()

    def run(self):
        player=self.player.sprite
        player.prevx=player.rect.x
        player.prevy=player.rect.y

        count_surf = pygame.Surface((30,50), flags=pygame.SRCALPHA)
        key = pygame.image.load('/home/sarthak/Programming/PyLagu/level/graphics/key/tile104.png')
        pygame.Surface.blit(count_surf, key, (0,0))
        

        self.background_sprites.update(self.world_shift)
        self.background_sprites.draw(self.display_surface)
        
        self.level_sprites.update(self.world_shift)
        self.level_sprites.draw(self.display_surface)

        self.enemies.update(self.world_shift, player)
        self.enemies.draw(self.display_surface)

        self.enemy_constraint_sprites.update(self.world_shift)
        # self.enemy_layout_sprites.update(self.world_shift, player)
        # self.enemy2_layout_sprites.update(self.world_shift, player)
        self.enemy_constraint()
        # self.enemy_layout_sprites.draw(self.display_surface)
        # self.enemy2_layout_sprites.draw(self.display_surface)

        if player.pushingleft or player.pushingright:
            for block in self.blocks.sprites():
                if block.enable and block.beingpushed:
                    block.update(0)
                else:
                    block.update(self.world_shift)
        else:
            self.blocks.update(self.world_shift)
        self.blocks.draw(self.display_surface)

        self.ropes.update(self.world_shift)
        self.ropes.draw(self.display_surface)

        self.handle_enemy_collisions()
        self.scroll_x()
        self.horizontal_movement_collisions()
        self.vertical_movement_collisions()
        self.check_rope_collisions()

        self.player.update()
        self.player.draw(self.display_surface)
        # self.enemy_constraint_sprites.draw(self.display_surface)
        player.healthbar.draw(self.display_surface)

        self.chest_layout_sprites.update(self.world_shift, player)
        self.chest_layout_sprites.draw(self.display_surface)
        pygame.Surface.blit(self.display_surface, count_surf, (0,10))

        # self.check_rope_collisions()

        