import pygame
from csv import reader
from settings import tile_size
from os import walk

def import_folder(path, type='n'):
    surface_list = []
    for information in walk(path):
        # for working_folder, sub_folders, items in information:
        for item in sorted(information[2]):
            loc = f'{path}/{item}'
            item_surf = pygame.image.load(loc).convert_alpha()
            if type =='n':
                surface_list.append(item_surf)
            
            elif type == 'skeleton':
                crop = (14, 46, 136, 56)
                new_surf=pygame.Surface((136, 56), flags=pygame.SRCALPHA)
                #item_surf = pygame.transform.flip(item_surf, True, False)
                new_surf.blit(item_surf, (0,0), crop)
                new_surf.convert_alpha()
                new_surf=pygame.transform.flip(new_surf, True, False)
                surface_list.append(new_surf)
            
            elif type =='eye':
                crop = (51, 59, 45, 31)
                new_surf = pygame.Surface((45,31), flags=pygame.SRCALPHA)
                new_surf.blit(item_surf, (0,0), crop)
                new_surf.convert_alpha()
                new_surf=pygame.transform.flip(new_surf, True, False)
                surface_list.append(new_surf)
            
            elif type == 'boss':
                crop = (4, 23, 184, 88)
                new_surf = pygame.Surface((184,88), flags=pygame.SRCALPHA)
                new_surf.blit(item_surf, (0,0), crop)
                new_surf.convert_alpha()
                surface_list.append(new_surf)
            
            elif type == 'player':
                if path !='/home/sarthak/Programming/PyLagu/level/graphics/character/dead':
                    crop = (15, 20, 26, 36)
                    new_surf = pygame.Surface((26,36), flags=pygame.SRCALPHA)
                    new_surf.blit(item_surf, (0,0), crop)
                    # new_surf.convert_alpha()
                    new_surf = pygame.transform.scale(new_surf, (26*1.5, 36*1.5))
                    surface_list.append(new_surf)
                else:
                    crop=(0, 20, 56, 36)
                    new_surf=pygame.Surface((56, 36), flags=pygame.SRCALPHA)
                    new_surf.blit(item_surf, (0, 0), crop)
                    new_surf=pygame.transform.scale(new_surf, (56*1.5, 36*1.5))
                    surface_list.append(new_surf)

    return surface_list

 
def import_csv_layout(path):
    level_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            level_map.append(list(row))
    
    return level_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0]/tile_size)
    tile_num_y = int(surface.get_size()[1]/tile_size)

    cut_tiles = []
    
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size))
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
    return cut_tiles
