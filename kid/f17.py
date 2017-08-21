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
        if self.rect.left<0 or self.rect.right>width:   #边界检测，到边改变方向
            self.speed[0]= - self.speed[0]
        if self.rect.top<0 or self.rect.bottom>height:
            self.speed[1]= - self.speed[1]

BKcolor=(255,255,255)
screen_size= width, height = 800, 600
screen=pygame.display.set_mode(screen_size)
screen.fill(BKcolor)
img_file="beach_ball.png"
balls=[]
for r in range(0,3):
    for c in range(0,3):
        pos=[c*180+10,r*180+10]
        speed=[choice([-2,2]),choice([-2,2])]
        ball=MyBallClass(img_file,pos,speed)
        balls.append(ball)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    pygame.time.delay(20)
    screen.fill(BKcolor)
    for ball in balls:
        ball.move()
        screen.blit(ball.image, ball.rect)
    pygame.display.flip()