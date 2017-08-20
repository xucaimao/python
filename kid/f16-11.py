import pygame, sys
pygame.init()
screen=pygame.display.set_mode([800,600])
BKcolor=[255,255,255]
screen.fill(BKcolor)
my_head=pygame.image.load("xgzy-small.png")
x=50
y=50
x_speed=5
ball_width=pygame.Surface.get_width(my_head)
ball_height=pygame.Surface.get_height(my_head)
screen_w=screen.get_width()

screen.blit(my_head,[x,y])
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    pygame.time.delay(20)
    pygame.draw.rect(screen, BKcolor, [x, y, ball_width, ball_height], 0)
    x = x + x_speed
    if x+ ball_width > screen_w or x<0:
        x_speed= - x_speed
    screen.blit(my_head, [x, y])
    pygame.display.flip()