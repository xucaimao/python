import pygame


global boardsize,boardtopleft,boardrightbottom
global gsize  #棋盘格子的尺寸
global buttontop,buttonbottom
global buttonleft,buttonright
global bsize     #按钮尺寸
boardsize=550
boardtopleft=22
boardrightbottom=572
gsize=68.75  #棋盘格子的尺寸
buttontop=180
buttonbottom=204
buttonleft=628
buttonright=876
bsize=62     #按钮尺寸

def piece_animate(win,background,animateimg,pos,dir):
    #棋子翻转动画
    #background是背景棋盘，animateimg是棋子动画序列
    #pos[r,c]为棋盘中的位置
    #dir=1黑变白，dir=-1白变黑
    framerate = pygame.time.Clock()
    r,c=pos
    px=c * gsize + boardtopleft
    py=r * gsize + boardtopleft
    i=0
    if dir==1:
        i=0
    elif dir==-1:
        i = 9

    for j in range(10):
        framerate.tick(3)
        ticks = pygame.time.get_ticks()

        imgrect = pygame.Rect(i * 69, 0, 69, 70)
        piece_img = animateimg.subsurface(imgrect)
        back_img = background.subsurface(px, py, 69, 70)

        win.blit(back_img, [px, py])
        win.blit(piece_img, [px, py])
        pygame.display.flip()
        i += dir


pygame.init()
screen = pygame.display.set_mode([900, 600])
pygame.display.set_caption("黑白棋 ver0.1")
background=pygame.image.load("qipan9x6.png")
animateimg=pygame.image.load("qizi_animate.png")
#framerate = pygame.time.Clock()
screen.blit(background, [0, 0])
pygame.display.flip()

piece_animate(screen,background,animateimg,[2,1],1)
piece_animate(screen,background,animateimg,[2,3],-1)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
