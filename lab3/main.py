import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill([255,255,255])
circle(screen, (255, 255, 0), (200, 175), 150)
line(screen, 'black', (50,50), (170,120), width=17)
line(screen, 'black', (190,120), (310,50), width=17)
circle(screen, 'red', (120, 130), 25)
circle(screen, 'black', (120, 130), 10)
circle(screen, 'red', (250, 120), 25)
circle(screen, 'black', (250, 120), 10)
line(screen, 'black', (130,250), (250,250), width=17)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()