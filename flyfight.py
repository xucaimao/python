# -*- coding: utf-8 -*-
#网络教程：从零开发一个小游戏
#http://www.tuicool.com/articles/yuIzMzq

import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf=pygame.Surface((75,25))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()

pygame.init()
screen_size=[800,600]
screen=pygame.display.set_mode(screen_size)

player=Player()

running=True
while running:
    for event in pygame.event.get():
        if event.type==KEYDOWN: #有键按下
            if event.key==K_ESCAPE:
                running=False
        elif event.type==QUIT:
            running=False
            
    screen.blit(player.surf,(400,300))
    
    pygame.display.flip()