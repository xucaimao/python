import pygame, sys, time
import  math

pygame.init()
screen=pygame.display.set_mode([800,600])
clock=pygame.time.Clock()

sinpoints=[]
for x in range(800):
    y=int(math.sin(x/800.0 * 4 * math.pi)*200 + 300)
    sinpoints.append([x,y])

screen.fill([255, 255, 255])
pygame.draw.lines(screen, [200, 0, 0], False, sinpoints, 2)
pygame.display.flip()
for i in range(100):
    firstpoint = sinpoints.pop(0)
    sinpoints.append(firstpoint)

time.sleep(5)
screen.fill([255, 255, 255])
pygame.draw.lines(screen, [0, 200, 0], False, sinpoints, 2)
pygame.display.flip()

while True:

    for event in pygame.event.get():
        if event == pygame.QUIT:
            sys.exit()

