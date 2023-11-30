import pygame as p
import time
from settings import *
from level import Level
from level_data import level_0
from player import Player

p.init()
screen = p.display.set_mode((screen_width,screen_height))
# lol = p.Surface((screen_width, screen_height))

clock = p.time.Clock()
p.transform.scale(screen,(800,400))
level = Level(level_0, screen)
p.display.set_caption('PyLagu: Lost in Woods')

while True:
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            exit()
    screen.fill('black')
    level.run()
    # scaled_lol = p.transform.smoothscale(lol, (screen.get_size()[0]*3, screen.get_size()[1]*3))

    # screen.blit(scaled_lol, (0, -screen_height*2))
    p.display.update()
    clock.tick(60)
