import math
from random import choice
from random import randint
import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
WIDTH = 800
HEIGHT = 600
g = 2


class Tank:
    def __init__(self):
        self.x = 20
        self.y = 450
        self.alpha = 0
        self.rot_right = False
        self.rot_left = False
        self.forward = False
        self.back = False

    def draw(self):
        h = 40
        if self.rot_left:
            self.alpha += math.pi / 64
        if self.rot_right:
            self.alpha -= math.pi / 64
        if self.forward:
            self.x -= 2 * math.sin(self.alpha)
            self.y -= 2 * math.cos(self.alpha)
        if self.back:
            self.x += 2 * math.sin(self.alpha)
            self.y += 2 * math.cos(self.alpha)
        pygame.draw.polygon(screen, (100, 0, 0),
                            [(self.x + h * math.cos(1.2 - self.alpha), self.y + h * math.sin(1.2 - self.alpha)),
                             (self.x + h * math.cos(1.2 + self.alpha), self.y - h * math.sin(1.2 + self.alpha)),
                             (self.x - h * math.cos(1.2 - self.alpha), self.y - h * math.sin(1.2 - self.alpha)),
                             (self.x - h * math.cos(1.2 + self.alpha), self.y + h * math.sin(1.2 + self.alpha))])

    def tank_management(self, obj):
        if obj.type == pygame.KEYDOWN and obj.key == pygame.K_d:
            self.rot_right = True
        if obj.type == pygame.KEYUP and obj.key == pygame.K_d:
            self.rot_right = False
        if obj.type == pygame.KEYDOWN and obj.key == pygame.K_a:
            self.rot_left = True
        if obj.type == pygame.KEYUP and obj.key == pygame.K_a:
            self.rot_left = False
        if obj.type == pygame.KEYDOWN and obj.key == pygame.K_w:
            self.forward = True
        if obj.type == pygame.KEYUP and obj.key == pygame.K_w:
            self.forward = False
        if obj.type == pygame.KEYDOWN and obj.key == pygame.K_s:
            self.back = True
        if obj.type == pygame.KEYUP and obj.key == pygame.K_s:
            self.back = False


class Pause:
    def __init__(self):
        self.start_time = 0
        self.is_going = False

    def launch(self):
        self.start_time = pygame.time.get_ticks()
        self.is_going = True

    def time(self):
        return pygame.time.get_ticks() - self.start_time

    def stop(self, obj):
        self.start_time = 0
        self.is_going = False
        obj.live = 0
        obj.new_target()
        balls.clear()


class Bullet_Menu:

    def __init__(self):
        self.style = False
        self.selected = [BLACK, (255, 255, 255)]

    def draw(self):
        font3 = pygame.font.SysFont('Rockwell', 40)
        ball_menu = font3.render('Ball', True, self.selected[self.style], self.selected[not self.style])
        bomb_menu = font3.render('Bomb', True, self.selected[not self.style], self.selected[self.style])
        screen.blit(ball_menu, (320, 40))
        screen.blit(bomb_menu, (390, 40))

    def change(self):
        self.style = not self.style


def print_points(points):
    pygame.font.init()
    font1 = pygame.font.SysFont('Rockwell', 60)
    score = font1.render(str(points), True, BLACK, (255, 255, 255))
    font2 = pygame.font.SysFont('Rockwell', 30)
    info = font2.render("Вы уничтожили мишень за " + str(len(balls)) + " выстрелов", True, BLACK, (255, 255, 255))
    screen.blit(score, (40, 40))
    if pause.is_going:
        screen.blit(info, (200, 200))


class Ball:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.undermine = False
        self.style = bullet_menu.style
        self.screen = screen
        self.x = tank.x
        self.y = tank.y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.style:
            if abs(self.vx) < 1.5:
                self.vx = 0
                self.vy = 0

            if self.x == WIDTH - self.r:
                self.vx *= -0.6
                self.vy *= 0.6
                self.x += self.vx
                self.y -= self.vy
            elif self.y == HEIGHT - 90 - self.r:
                self.vy *= -0.6
                self.vx *= 0.6
                self.x += self.vx
                self.y -= self.vy
            else:
                if self.x + self.r + self.vx > WIDTH:
                    self.x = WIDTH - self.r
                else:
                    self.x += self.vx
                if self.vx != 0:
                    self.vy -= g
                if self.y + self.r - self.vy > HEIGHT - 90:
                    self.y = HEIGHT - 90 - self.r
                else:
                    self.y -= self.vy
        else:
            if self.undermine:
                self.vx = 0
                self.vy = 0
                if self.r < 60:
                    self.r *= 1.1
                else:
                    self.x = 0
                    self.y = 0
                    self.r = 0
            else:
                self.vy -= g
                self.x += self.vx
                self.y -= self.vy

    def draw(self):
        if self.style:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
            pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 1)
        else:
            pygame.draw.circle(self.screen, RED, (self.x, self.y), self.r)
            pygame.draw.circle(self.screen, YELLOW, (self.x, self.y), self.r, 1)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        strike = False
        if self.r + obj.r > ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5:
            strike = True
            print("strike")
        return strike


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = BLACK

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1

        new_ball = Ball(self.screen)
        new_ball.r += 5
        new_ball.style = bullet_menu.style
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            x_mouse = event.pos[0]
            if x_mouse == tank.x:
                x_mouse = tank.x+1
            self.an = math.atan((event.pos[1] - tank.y) / (x_mouse - tank.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = BLACK

    def draw(self):
        # FIXIT don't know how to do it
        # me
        if self.f2_on == 1:
            pygame.draw.line(self.screen, RED, (tank.x, tank.y),
                             (tank.x + self.f2_power * math.cos(self.an), tank.y + self.f2_power * math.sin(self.an)), 7)
        else:
            pygame.draw.line(self.screen, BLACK, (tank.x, tank.y),
                             (tank.x + 3 * self.f2_power * math.cos(self.an), tank.y + 3 * self.f2_power * math.sin(self.an)),
                             7)

        # me

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = BLACK


class Target:
    def __init__(self):
        self.stile = 1
        self.points = 0
        self.live = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = randint(0, 5)
        self.vy = 5
        self.x_r = randint(200, 780)
        self.y_r = randint(100, 550)
        self.r_r = 200
        self.alpha = 0

    def new_target(self):
        self.stile = randint(1, 2)
        self.x = randint(600, 780)
        self.y = randint(300, HEIGHT - 90)
        self.r = randint(2, 25)
        self.color = randint(0, 5)
        self.live = 1

    def hit(self):
        self.r = 0
        self.x = 0
        self.y = 0
        self.points += 1

    def draw(self):
        if self.stile == 1:
            if not (self.y - self.r > 10 and self.y + self.r < HEIGHT):
                self.vy *= -1
            self.y += self.vy

        if self.stile == 2:
            self.x = self.x_r + self.r_r * math.cos(self.alpha)
            self.y = self.y_r + self.r_r * math.sin(self.alpha)
            self.alpha += 0.05
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
pause = Pause()
clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False
bullet_menu = Bullet_Menu()
tank = Tank()

while not finished:
    screen.fill(WHITE)
    tank.draw()
    gun.draw()
    target.draw()
    bullet_menu.draw()
    for b in balls:
        b.draw()
    print_points(target.points)
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        tank.tank_management(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            bullet_menu.change()
            print('hello')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            balls[len(balls) - 1].undermine = True
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()

        if pause.is_going:
            if pause.time() > 4000:
                pause.stop(target)
        else:
            if b.hittest(target) and target.live:
                pause.launch()
                target.hit()

    gun.power_up()

pygame.quit()

