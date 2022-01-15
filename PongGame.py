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
        self.window = Window
        self.setFixedSize(self.size())
        global col_num_1
        global col_num_2

    # initialize
    def init_ui(self):
        self.pushButton_9.clicked.connect(self.start)
        self.pushButton_5.clicked.connect(self.start)
        self.pushButton_7.clicked.connect(self.start)
        self.pushButton_6.clicked.connect(self.start)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.start)
        self.pushButton_3.clicked.connect(self.start)
        self.pushButton_4.clicked.connect(self.start)
        self.horizontalSlider.valueChanged.connect(self.sound)

    # sound menu settings
    def sound(self):
        global sound_value
        value = str(self.horizontalSlider.value())
        sound_value = int(value)
        self.label_14.setText(value)

    # start game
    def start(self):
        send = self.sender().text()
        if send != '1' and send != '2' and send != '3' and send != '4':
            self.hide()
            pong(send)
            self.show()
            self.label_8.setText(str(col_num_2))
            self.label_9.setText(str(col_num_1))
            # results
            if col_num_1 > col_num_2:
                self.label_10.setText('Игрок № 2 победил!')
            elif col_num_1 == col_num_2:
                self.label_10.setText('Ничья')
            else:
                self.label_10.setText('Игрок № 1 победил!')
        else:
            # fon settings
            global fon_number
            if send == '1':
                fon_number = '1'
            elif send == '2':
                fon_number = '2'
            elif send == '3':
                fon_number = '3'
            elif send == '4':
                fon_number = '4'
            self.label_13.setText('Фон успешно выбран!')


# global game settings
sound_value = 0
col_num_1 = 0
col_num_2 = 0
fon_number = ''


# game
def pong(send):
    global level
    global sound_value
    # game mode settings

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
            if (paddle.x + 75) - ball.x < 5.9:
                paddle.x -= (paddle.x + 75) - ball.x
            else:
                paddle.x -= 5.9
        else:
            if ball.x - (paddle.x + 75) < 5.9:
                paddle.x += ball.x - (paddle.x + 75)
            else:
                paddle.x += 5.9

    def human_vs_human():
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < width:
            paddle.right += paddle_speed

    # paddle collision
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
    sound_value = sound_value / 100
    # set mode
    if send == '1 на 1':
        level = 11
    elif send == "Бот: уровень легко":
        level = 1
    elif send == "Бот: уровень средне":
        level = 2
    elif send == "Бот: уровень невозможно":
        level = 3
    width, height = 800, 800
    fps = 60
    # paddle settings
    paddle_w = 150
    paddle_h = 25
    paddle_speed = 5
    paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)
    paddle1 = pygame.Rect(300, 15, paddle_w, paddle_h)
    # ball settings
    ball_radius = 15
    ball_speed = 6
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(rnd(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
    # ball direction
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
    # stats
    col1 = 0
    col2 = 0
    # background image
    global fon_number
    ball1 = pygame.image.load('Ball_real.png')
    ball1.set_colorkey((0, 0, 0))
    if fon_number == '1':
        img = pygame.image.load('fon1.jpg').convert()
    elif fon_number == '2':
        img = pygame.image.load('fon2.jpg').convert()
    elif fon_number == '3':
        img = pygame.image.load('fon3.jpg').convert()
    elif fon_number == '4':
        img = pygame.image.load('fon4.jpg').convert()
    else:
        img = pygame.image.load('fon.jpg').convert()
    start_ticks = pygame.time.get_ticks()  # starter tick
    # sound and music
    sound_collision = pygame.mixer.Sound("collision.wav")
    sound_loose = pygame.mixer.Sound("loose.wav")
    sound_win = pygame.mixer.Sound("win.mp3")
    sound_not_win = pygame.mixer.Sound("not_win.mp3")
    sound_collision_wall = pygame.mixer.Sound("collision_wall.wav")
    start_sound = pygame.mixer.Sound('start.wav')
    pygame.mixer.music.load("fon.mp3")
    sound_win.set_volume(sound_value)
    start_sound.set_volume(sound_value)
    sound_collision_wall.set_volume(sound_value)
    sound_collision.set_volume(sound_value)
    sound_loose.set_volume(sound_value)
    sound_not_win.set_volume(sound_value)
    running = True
    pygame.mixer.music.play(-1)
    # application name
    pygame.display.set_caption('Pong')
    pygame.mixer.music.set_volume(sound_value)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.mixer.music.stop()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.mixer.music.stop()
                    return
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
            # loose player 2
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
            # loose player 1
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
            if level == 1:
                bot1lvl()
            elif level == 2:
                bot2lvl()
            elif level == 3:
                bot3lvl()
            elif level == 11:
                human_vs_human()
            # control people
            if key[pygame.K_a] and paddle1.left > 0:
                paddle1.left -= paddle_speed
            if key[pygame.K_d] and paddle1.right < width:
                paddle1.right += paddle_speed
        global col_num_1
        global col_num_2
        col_num_1 = col1
        col_num_2 = col2
        # win or loose sound and exit
        if (level == 1 or level == 2 or level == 3) and col2 >= 10:
            sound_win.play()
        elif (level == 1 or level == 2 or level == 3) and col1 >= 10:
            sound_not_win.play()
        if col1 >= 10 or col2 >= 10:
            pygame.display.quit()
            pygame.mixer.music.stop()
            return
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
        # player1 num
        font = pygame.font.Font('freesansbold.ttf', 25)
        text_surface_obj = font.render('Player 1', True, pygame.Color('red'))
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (50, 350)
        sc.blit(text_surface_obj, text_rect_obj)
        # player2 num
        font = pygame.font.Font('freesansbold.ttf', 25)
        text_surface_obj = font.render('Player 2', True, pygame.Color('red'))
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (50, 450)
        sc.blit(text_surface_obj, text_rect_obj)
        # game mode settings view
        if level == 1:
            font = pygame.font.Font('freesansbold.ttf', 15)
            text_surface_obj = font.render(f'Mode: bot vs people level: easy', True, pygame.Color('red'))
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (660, 780)
            sc.blit(text_surface_obj, text_rect_obj)
        elif level == 2:
            font = pygame.font.Font('freesansbold.ttf', 15)
            text_surface_obj = font.render(f'Mode: bot vs people level: middle', True, pygame.Color('red'))
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (660, 780)
            sc.blit(text_surface_obj, text_rect_obj)
        elif level == 3:
            font = pygame.font.Font('freesansbold.ttf', 15)
            text_surface_obj = font.render(f'Mode: bot vs people level: impossible', True, pygame.Color('red'))
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (660, 780)
            sc.blit(text_surface_obj, text_rect_obj)
        elif level == 11:
            font = pygame.font.Font('freesansbold.ttf', 15)
            text_surface_obj = font.render(f'Mode: people vs people', True, pygame.Color('red'))
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (660, 780)
            sc.blit(text_surface_obj, text_rect_obj)
        pygame.display.flip()
        clock.tick(fps)


# window start
if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Window()
    exe.show()
    sys.exit(app.exec())
