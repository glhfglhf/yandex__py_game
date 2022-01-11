import sys
import random
import pygame
from random import randrange as rnd
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Pong_choose_menu.ui', self)
        self.operation = str()
        self.init_ui()
        self.setFixedSize(self.size())
        self.level = 0

    def init_ui(self):
        self.pushButton_9.clicked.connect(self.start)

    def start(self):
        self.close()

        def pong():
            def bot1lvl():
                if paddle.x + 75 > ball.x:
                    if (paddle.x + 75) - ball.x < 3:
                        paddle.x -= (paddle.x + 75) - ball.x
                    else:
                        paddle.x -= 3
                else:
                    if ball.x - (paddle.x + 75) < 3:
                        paddle.x += ball.x - (paddle.x + 75)
                    else:
                        paddle.x += 3

            def bot2lvl():
                if paddle.x + 75 > ball.x:
                    if (paddle.x + 75) - ball.x < 5:
                        paddle.x -= (paddle.x + 75) - ball.x
                    else:
                        paddle.x -= 5
                else:
                    paddle.x += 5

            def bot3lvl():
                if paddle.x + 75 > ball.x:
                    if (paddle.x + 75) - ball.x < 6:
                        paddle.x -= (paddle.x + 75) - ball.x
                    else:
                        paddle.x -= 6
                else:
                    if ball.x - (paddle.x + 75) < 6:
                        paddle.x += ball.x - (paddle.x + 75)
                    else:
                        paddle.x += 6

            def human_vs_human():
                if key[pygame.K_LEFT] and paddle.left > 0:
                    paddle.left -= paddle_speed
                if key[pygame.K_RIGHT] and paddle.right < width:
                    paddle.right += paddle_speed

            def detect_collision(d_x, d_y, boll, rect):
                if d_x > 0:
                    delta_x = boll.right - rect.left
                else:
                    delta_x = rect.right - boll.left
                if d_y > 0:
                    delta_y = boll.bottom - rect.top
                else:
                    delta_y = rect.bottom - boll.top

                if abs(delta_x - delta_y) < 10:
                    d_x, d_y = -d_x, -d_y
                elif delta_x > delta_y:
                    d_y = -d_y
                elif delta_y > delta_x:
                    d_x = -d_x
                sound_collision.play()
                return d_x, d_y

            lvl = 2
            width, height = 800, 800
            fps = 60
            # paddle settings
            paddle_w = 150
            paddle_h = 25
            paddle_speed = 4
            paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)
            paddle1 = pygame.Rect(300, 15, paddle_w, paddle_h)
            # ball settings
            ball_radius = 15
            ball_speed = 6
            ball_rect = int(ball_radius * 2 ** 0.5)
            ball = pygame.Rect(rnd(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
            a = random.randint(0, 1)
            if a == 1:
                dx = 1
            else:
                dx = -1
            a = random.randint(0, 1)
            if a == 0:
                dy = 1
            else:
                dy = -1
            pygame.init()
            sc = pygame.display.set_mode((width, height))
            clock = pygame.time.Clock()
            col1 = 0
            col2 = 0

            # background image
            ball1 = pygame.image.load('Ball_real.png')
            ball1.set_colorkey((0, 0, 0))
            img = pygame.image.load('fon.jpg').convert()
            start_ticks = pygame.time.get_ticks()  # starter tick
            sound_collision = pygame.mixer.Sound("collision.wav")
            sound_loose = pygame.mixer.Sound("loose.wav")
            sound_collision_wall = pygame.mixer.Sound("collision_wall.wav")
            num_sound = pygame.mixer.Sound('otschet.wav')
            start_sound = pygame.mixer.Sound('start.wav')
            pygame.mixer.music.load("fon.mp3")
            pygame.mixer.music.play(-1)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
                if seconds > 4:
                    # ball movement
                    ball.x += ball_speed * dx
                    ball.y += ball_speed * dy
                    # collision left right
                    if ball.centerx < ball_radius or ball.centerx > width:
                        dx = -dx
                        sound_collision_wall.play()
                    # collision top
                    if ball.colliderect(paddle1) and dy < 800:
                        dx, dy = detect_collision(dx, dy, ball, paddle1)
                        fps += 5
                    # collision ball
                    if ball.x >= 800:
                        ball.x = random.randint(50, 750)
                        ball.y = 400
                        fps = 60
                        sound_collision.play()
                        a = random.randint(0, 1)
                        if a == 1:
                            dx = 1
                        else:
                            dx = -1
                        a = random.randint(0, 1)
                        if a == 0:
                            dy = 1
                        else:
                            dy = -1
                    if ball.centery < 40:
                        a = random.randint(0, 1)
                        dx, _ = 1, -1
                        if a == 1:
                            dx = 1
                        else:
                            dx = -1
                        a = random.randint(0, 1)
                        if a == 0:
                            dy = 1
                        else:
                            dy = -1
                        ball.x = random.randint(50, 750)
                        ball.y = 400
                        fps = 60
                        col1 += 1
                        sound_loose.play()

                    if ball.centery > 760:
                        ball.x = random.randint(50, 750)
                        ball.y = 400
                        fps = 60
                        a = random.randint(0, 1)
                        if a == 1:
                            dx = 1
                        else:
                            dx = -1
                        a = random.randint(0, 1)
                        if a == 0:
                            dy = 1
                        else:
                            dy = -1
                        col2 += 1
                        sound_loose.play()
                    # collision paddle
                    if ball.colliderect(paddle) and dy > 0:
                        dx, dy = detect_collision(dx, dy, ball, paddle)
                        fps += 5
                        sound_collision.play()
                    # control bot
                    key = pygame.key.get_pressed()
                    if lvl == 1:
                        bot1lvl()
                        font = pygame.font.Font('freesansbold.ttf', 15)
                        text_surface_obj = font.render(f'Mode: bot vs people level: easy', True, pygame.Color('red'))
                        text_rect_obj = text_surface_obj.get_rect()
                        text_rect_obj.center = (680, 780)
                        sc.blit(text_surface_obj, text_rect_obj)
                    elif lvl == 2:
                        bot2lvl()
                        font = pygame.font.Font('freesansbold.ttf', 15)
                        text_surface_obj = font.render(f'Mode: bot vs people level: middle', True, pygame.Color('red'))
                        text_rect_obj = text_surface_obj.get_rect()
                        text_rect_obj.center = (660, 780)
                        sc.blit(text_surface_obj, text_rect_obj)
                    elif lvl == 3:
                        bot3lvl()
                        font = pygame.font.Font('freesansbold.ttf', 15)
                        text_surface_obj = font.render(f'Mode: bot vs people level: impossible', True,
                                                       pygame.Color('red'))
                        text_rect_obj = text_surface_obj.get_rect()
                        text_rect_obj.center = (660, 780)
                        sc.blit(text_surface_obj, text_rect_obj)
                    elif lvl == 11:
                        human_vs_human()
                    # control people
                    if key[pygame.K_a] and paddle1.left > 0:
                        paddle1.left -= paddle_speed
                    if key[pygame.K_d] and paddle1.right < width:
                        paddle1.right += paddle_speed
                sc.blit(img, (0, 0))
                # drawing world
                pygame.draw.rect(sc, pygame.Color('Orange'), (0, 400, 800, 15), 2)
                sc.blit(ball1, (ball.x - 50, ball.y - 30))
                pygame.draw.rect(sc, pygame.Color(0, 255, 0), paddle, 3)
                pygame.draw.rect(sc, pygame.Color(0, 255, 0), paddle1, 3)
                # timer
                if seconds + 1 < 4:
                    font = pygame.font.Font('freesansbold.ttf', 150)
                    text_surface_obj = font.render(str(int(seconds + 1)), True, pygame.Color('green'))
                    text_rect_obj = text_surface_obj.get_rect()
                    text_rect_obj.center = (400, 400)
                    sc.blit(text_surface_obj, text_rect_obj)
                    if int(seconds) + 1 == 1:
                        num_sound.play()
                    if int(seconds) + 1 == 2:
                        num_sound.play()
                    if int(seconds) + 1 == 3:
                        num_sound.play()
                elif seconds + 1 < 5:
                    font = pygame.font.Font('freesansbold.ttf', 150)
                    text_surface_obj = font.render('START', True, pygame.Color('red'))
                    text_rect_obj = text_surface_obj.get_rect()
                    text_rect_obj.center = (400, 400)
                    sc.blit(text_surface_obj, text_rect_obj)
                    start_sound.play()
                # score player 2
                font = pygame.font.Font('freesansbold.ttf', 40)
                text_surface_obj = font.render(str(col2), True, pygame.Color('red'))
                text_rect_obj = text_surface_obj.get_rect()
                text_rect_obj.center = (50, 50)
                sc.blit(text_surface_obj, text_rect_obj)
                # score player 1
                font = pygame.font.Font('freesansbold.ttf', 40)
                text_surface_obj = font.render(str(col1), True, pygame.Color('red'))
                text_rect_obj = text_surface_obj.get_rect()
                text_rect_obj.center = (50, 750)
                sc.blit(text_surface_obj, text_rect_obj)
                if lvl == 1:
                    font = pygame.font.Font('freesansbold.ttf', 15)
                    text_surface_obj = font.render(f'Mode: bot vs people level: easy', True, pygame.Color('red'))
                    text_rect_obj = text_surface_obj.get_rect()
                    text_rect_obj.center = (660, 780)
                    sc.blit(text_surface_obj, text_rect_obj)
                elif lvl == 2:
                    font = pygame.font.Font('freesansbold.ttf', 15)
                    text_surface_obj = font.render(f'Mode: bot vs people level: middle', True, pygame.Color('red'))
                    text_rect_obj = text_surface_obj.get_rect()
                    text_rect_obj.center = (660, 780)
                    sc.blit(text_surface_obj, text_rect_obj)
                elif lvl == 3:
                    font = pygame.font.Font('freesansbold.ttf', 15)
                    text_surface_obj = font.render(f'Mode: bot vs people level: impossible', True, pygame.Color('red'))
                    text_rect_obj = text_surface_obj.get_rect()
                    text_rect_obj.center = (660, 780)
                    sc.blit(text_surface_obj, text_rect_obj)
                pygame.display.flip()
                clock.tick(fps)
        pong()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Window()
    exe.show()
    sys.exit(app.exec())
