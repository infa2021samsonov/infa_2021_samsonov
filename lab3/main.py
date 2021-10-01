import pygame
import math as m
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1300, 550))
rect(screen, (255, 255, 255), [(0, 0), (1300, 600)])


def rukav(color, vertex_count, radius, position, k):
    # k нужен для ориентации - правой или левой - он 1 или -1
    n, r = vertex_count, radius
    x, y = position
    polygon(screen, color, [
        (x + r * m.cos(2 * m.pi * i / n + k * m.pi), y + r * m.sin(2 * m.pi * i / n + k * m.pi))
        for i in range(n)
    ])
    polygon(screen, (0, 0, 0), [
        (x + r * m.cos(2 * m.pi * i / n + k * m.pi), y + r * m.sin(2 * m.pi * i / n + k * m.pi))
        for i in range(n)
    ], 1)


def volos(a, x, y, color):
    # а - угол через который расположены треугольники волос ~10deg
    a = a / 360 * 2 * m.pi
    polygon(screen, color, [(x + 150 * m.sin(a) - 25 * m.cos(a), y - 150 * m.cos(a) - 25 * m.sin(a)),
                            (x + 150 * m.sin(a) + 25 * m.cos(a), y - 150 * m.cos(a) + 25 * m.sin(a)),
                            (x + (150 + 35) * m.sin(a), y - (150 + 35) * m.cos(a))])
    # отрисовка границы
    polygon(screen, (0, 0, 0), [[x + 150 * m.sin(a) - 25 * m.cos(a), y - 150 * m.cos(a) - 25 * m.sin(a)],
                                (x + 150 * m.sin(a) + 25 * m.cos(a), y - 150 * m.cos(a) + 25 * m.sin(a)),
                                (x + (150 + 35) * m.sin(a), y - (150 + 35) * m.cos(a))], 1)


def human(x, y, heir, eyes, shirt):

    circle(screen, shirt, (x, y + 200), 180, draw_top_left=True, draw_top_right=True)  # тело

    circle(screen, (228, 199, 178), (x, y - 60), (150), )  # face

    circle(screen, eyes, (x + 40, y - 100), 27)  # глаз правый
    circle(screen, (0, 0, 0), (x + 40, y - 100), 8)  # зрачек правый
    circle(screen, eyes, (x - 40, y - 100), 27)  # глаз левый
    circle(screen, (0, 0, 0), (x - 40, y - 100), 8)  # зрачек левый

    polygon(screen, (113, 70, 40), [(x, y - 50), (x + 10, y - 70), (x - 10, y - 70)])  # нос
    polygon(screen, (235, 66, 56), [(x, y + 20), (x - 80, y - 40), (x + 80, y - 40)])  # рот

    line(screen, (228, 199, 178), (x - 150, y + 100), (x - 300, y - 260), 25)  # левая рука
    line(screen, (228, 199, 178), (x + 150, y + 100), (x + 300, y - 260), 25)  # правая рука

    circle(screen, (228, 199, 178), (x - 300, y - 260), 33, draw_bottom_left=True, draw_bottom_right=True)  # левая ладонь
    circle(screen, (228, 199, 178), (x + 300, y - 260), 33, draw_bottom_left=True, draw_bottom_right=True)  # правая ладонь

    # отрисовка рукавов
    rukav(shirt, 5, 74, (x - 150, y + 100), 0)
    rukav(shirt, 5, 74, (x + 150, y + 100), 1)

    # отрисовка волос
    for i in range(-90, 105, 15):
        volos(i, x, y - 60, heir)
    return 0


human(350, 360, (249, 212, 83), (192, 199, 184), (55, 125, 34))
human(960, 360, (195, 69, 246), (133, 178, 240), (237, 110, 45))

rect(screen, (160, 250, 88), [(0, 0), (1300, 100)])
rect(screen, (0, 0, 0), [(0, 0), (1300, 100)], 1)
text = pygame.font.SysFont('pingfang', 65, True)
follow = text.render("PYTHON is REALLY AMAZING!", True, (0, 0, 0))

pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    screen.blit(follow, (120, 7))
    pygame.display.update()
pygame.quit()
