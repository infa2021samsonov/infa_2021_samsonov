import pygame
import math
from pygame.draw import *
from random import randint

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
name = input()
pygame.init()
count = 0
FPS = 60
screen = pygame.display.set_mode((1200, 900))
gametime = 0
man_data = []
score_data = []

#добавление данных о рекорде в файл
def append_data():
    f = open('players.txt', "r+")
    i = 0
    flag = True
    for line in f:
        print('line ',i)
        if 2 >= i >= 0:
            score_data.append(line)
            print('app_score')
        if 3 <= i <= 5:
            print('add_data')
            man_data.append(line)
            if (int(score_data[i - 3]) < count) and flag:
                score_data[i - 3] = str(count) + '\n'
                man_data[i - 3] = name + '\n'
                flag = False
        i = i + 1

    f1  = open('players.txt','w')
    for i in score_data:
        f1.write(str(i))
    for i in man_data:
        f1.write(str(i))

# класс для пятиугольников
class pentagramm:

    def __init__(self, Vx0, Vy0, x, y, r, Vx, Vy, color):
        self.Vx0 = Vx0
        self.Vy0 = Vy0
        self.x = x
        self.y = y
        self.r = r
        self.Vx = Vx
        self.Vy = Vy
        self.color = color

    def move(self):
        self.color = (randint(1, 200), randint(1, 200), randint(1, 200))
        if gametime % FPS == 0:
            self.Vx = self.Vx0 * math.cos(randint(0, 12) * (math.pi / 12))
            self.Vy = self.Vy0 * math.cos(randint(0, 12) * (math.pi / 12))
        if self.x > 1200 - self.r:
            self.Vx = -self.Vx
        if self.y > 900 - self.r:
            self.Vy = -self.Vy
        if self.x < 0 + self.r:
            self.Vx = -self.Vx
        if self.y < 0 + self.r:
            self.Vy = -self.Vy
        self.x = self.Vx / FPS + self.x
        self.y = self.Vy / FPS + self.y

# класс для шариков
class ball:
    def __init__(self, x, y, r, Vx, Vy, color):
        self.x = x
        self.y = y
        self.r = r
        self.Vx = Vx
        self.Vy = Vy
        self.color = color

    def move(self):
        if self.x > 1200 - self.r:
            self.Vx = -self.Vx
        if self.y > 900 - self.r:
            self.Vy = -self.Vy
        if self.x < 0 + self.r:
            self.Vx = -self.Vx
        if self.y < 0 + self.r:
            self.Vy = -self.Vy
        self.x = self.Vx / FPS + self.x
        self.y = self.Vy / FPS + self.y

# массивы для доступа ко всем шарам и пятиугольниикам
pentagramms = []
balls = []

#заполненеи массива шарами и пятиугольниками
def init_balls(balls):
    n = 25
    for i in range(1, n + 1):
        newB = ball(randint(100, 1100), randint(100, 800), randint(15, 70), randint(50, 500), randint(50, 500),
                    COLORS[randint(0, 5)])
        balls.append(newB)


def init_pentagramms(pentagramms):
    n = 10
    for i in range(1, n + 1):
        newP = pentagramm(randint(200, 500), randint(200, 500), randint(100, 1100), randint(100, 800), randint(15, 25),
                          randint(80, 500), randint(80, 500), (randint(1, 200), randint(1, 200), randint(1, 200)))
        pentagramms.append(newP)


init_balls(balls)

init_pentagramms(pentagramms)

#вывод текста на экран
def print_info():
    pygame.font.init()
    myfont = pygame.font.SysFont('Rockwell', 60)
    score = myfont.render('Score: ' + str(count), True, (255, 255, 255))
    screen.blit(score, (40, 40))

    timer = myfont.render(str(60 - round(gametime / FPS)), True, (255, 255, 255))
    screen.blit(timer, (600, 40))

#отррисовка всех фигур за временной сдвиг
def draw():
    for i in balls:
        i.move()
        circle(screen, i.color, (i.x, i.y), i.r)
    for i in pentagramms:
        i.move()
        polygon(screen, i.color, [
            (i.x + i.r * math.cos(2 * math.pi * k / 5 + math.pi), i.y + i.r * math.sin(2 * math.pi * k / 5 + math.pi))
            for k in range(5)
        ])


pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            xm, ym = event.pos
            push = False
            # проверки для нажимания на шар/пятиугольник
            for i in balls:
                if (i.x + i.r > xm) and (i.x - i.r < xm) and (i.y - i.r < ym) and (i.y + i.r > ym):
                    if not push:
                        count += round(30 / i.r + math.sqrt(i.Vx ** 2 + i.Vy ** 2) / 300)
                        balls.remove(i)
                        push = True
            for i in pentagramms:
                if (i.x + i.r > xm) and (i.x - i.r < xm) and (i.y - i.r < ym) and (i.y + i.r > ym):
                    if not push:
                        count += 5
                        pentagramms.remove(i)
                        push = True
            print(count)
    #переменная для времени - один раунд идет минуту
    gametime += 1
    draw()
    print_info()
    pygame.display.update()
    screen.fill(BLACK)
    # окончание раунда
    if (gametime % FPS == 0) and (gametime / FPS) == 60:
        print(count)
        append_data()
        pygame.quit()

pygame.quit()
