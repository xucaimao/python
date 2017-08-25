import pygame, sys, random
from random import *

class MyBallClass(pygame.sprite.Sprite):                #继承
    def __init__(self,image_file,position,speed):
        pygame.sprite.Sprite.__init__(self)             #调用父类的初始化进程
        self.image=pygame.image.load(image_file)        #由图像生成Surface
        self.rect=self.image.get_rect()                 #获得图像的Rect
        self.rect.left,self.rect.top = position         #设置对象的初始位置
        self.speed=speed

    def move(self):
        self.rect=self.rect.move(self.speed)            #移动
        if self.rect.left < 0 or self.rect.right>width:   #边界检测，到边改变方向
            self.speed[0] = - self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = - self.speed[1]

def animate(ballgroup):
    screen.fill(BKcolor)
    for ball in ballgroup:
        ball.move()
    for ball in ballgroup:
        ballgroup.remove(ball)                          #从组删除当前精灵

    #spritecollide(sprite, group, dokill, collided = None)
    #第一个参数指定被检测的精灵
    #第二个参数指定一个组，由 sprite.Group() 生成
    #第三个参数设置是否从组中删除检测到碰撞的精灵
    #第四个参数设置一个回调函数，用于定制特殊的检测方法。如果该参数忽略，那么默认是检测精灵之间的 rect 是否产生重叠
        if pygame.sprite.spritecollide(ball,ballgroup,False):
            ball.speed[0] = - ball.speed[0]
            ball.speed[1] = - ball.speed[1]

        ballgroup.add(ball)
        screen.blit(ball.image, ball.rect)
    pygame.display.flip()

BKcolor=(255,255,255)
screen_size= width, height = 800, 600
screen=pygame.display.set_mode(screen_size)
screen.fill(BKcolor)
img_file="beach_ball.png"
clock=pygame.time.Clock()
ballgroup=pygame.sprite.Group()                         #创建精灵组
for r in range(0,3):
    for c in range(0,3):
        pos=[c*180+10,r*180+10]
        speed=[choice([-2,2]),choice([-2,2])]
        ball=MyBallClass(img_file,pos,speed)
        ballgroup.add(ball)                             #注意用add方法，不是append



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            frame_rate=clock.get_fps()
            print("Frame rate = ",frame_rate)
            pygame.display.quit()
            sys.exit()

    animate(ballgroup)
    clock.tick(30)
