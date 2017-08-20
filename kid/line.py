import pygame,sys
from pygame.locals import *

pygame.init()
bk_color=[255,255,255]
posa=[400,500]
posb_y=100
screen=pygame.display.set_mode([800,600])
clock=pygame.time.Clock()
head=pygame.image.load("xgzy-small.png")
head_w=pygame.Surface.get_width(head)
head_h=pygame.Surface.get_height(head)
#取得图片的大小
screen.fill(bk_color)
pygame.draw.circle(screen,[255,0,0],posa,10,0)
pygame.draw.line(screen,[255,0,0],[0,posb_y],[800,posb_y],5)
pygame.display.flip()
bk_surf=pygame.Surface.copy(screen)
#创建一个底纹的备份

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            posb_x=event.pos[0]                 #取得x坐标
            #posb_y=event.pos[1]

        screen.blit(bk_surf,[0,0])              #重绘背景
        pygame.draw.line(screen,[0,255,0],posa,[posb_x,posb_y],3)
        screen.blit(head,[posb_x-head_w/2,posb_y-head_h/2])
        pygame.display.flip()

