import os
import sqlite3
import sys
import random
from random import randrange as rnd

import pygame
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QTableWidgetItem, QDialog
from PyQt5.QtGui import QMovie


name_of_player = ''
count_of_flags = 22
count_of_lives = 3
count_of_opened_cells = 0
# global game settings
sound_value = 1
col_num_1 = 0
col_num_2 = 0
fon_number = ''
record = 0


# выбор фона и режима понга
class ChoosePongMod(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\\pong_choose_menu.ui', self)
        self.setWindowTitle('Выбор режима')
        self.operation = str()
        self.init_ui()
        self.setFixedSize(self.size())
        self.cancel.clicked.connect(self.close_pong_choose_menu)
        global col_num_1
        global col_num_2

    def close_pong_choose_menu(self):
        self.close()

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
        global sound_value
        sound_value = int(self.horizontalSlider.value())

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


# окно с выводом данных из базы с результатами игроков
class Results(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\\results.ui', self)
        self.setWindowTitle('Результаты')
        database = sqlite3.connect('py_game.db')
        cur = database.cursor()
        result = list(map(lambda x: x, cur.execute("SELECT * FROM results")))
        self.tableWidget.setRowCount(len(result))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        database.close()


# меню выбора игры
class ChooseGame(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\\choose_game.ui', self)
        self.setWindowTitle('Выбор игры')
        self.choose_mod = ChoosePongMod()
        self.cancel.clicked.connect(self.close_choose_game)
        self.pong.clicked.connect(self.open_choose_mod)
        self.sapper.clicked.connect(self.miner_start)
        self.tetriss.clicked.connect(self.tetris_start)

    def open_choose_mod(self):
        self.choose_mod.show()

    def close_choose_game(self):
        self.close()

    # запуск сапера
    def miner_start(self):
        self.hide()
        miner()
        database = sqlite3.connect('py_game.db')
        cur = database.cursor()
        cur.execute(f"""INSERT INTO results (
                                                    name,
                                                    game,
                                                    result)
                                                    VALUES (
                                                    '{name_of_player}',
                                                    'Сапер',
                                                    'Открыто клеток: {count_of_opened_cells}'
                                                    );""")
        database.commit()
        database.close()
        self.show()

    # запуск тетриса
    def tetris_start(self):
        self.hide()
        tetris()
        database = sqlite3.connect('py_game.db')
        cur = database.cursor()
        cur.execute(f"""INSERT INTO results (
                                                        name,
                                                        game,
                                                        result)
                                                        VALUES (
                                                        '{name_of_player}',
                                                        'Тетрис',
                                                        'Рекорд: {record}'
                                                        );""")
        database.commit()
        database.close()
        self.show()


# меню с данными о проекте
class AboutProject(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\\about_project.ui', self)
        self.setWindowTitle('О проекте')
        self.cancel.clicked.connect(self.close_about_project)

    def close_about_project(self):
        self.close()


# главное меню
class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\\Menu.ui', self)
        self.setWindowTitle('Меню')
        self.operation = str()
        self.setFixedSize(self.size())
        self.movie = QMovie("images\\rain.gif")
        self.gif.setMovie(self.movie)
        self.movie.start()

        self.about_project.clicked.connect(self.open_about_project)
        self.choose_game.clicked.connect(self.open_choose_game)
        self.table_of_records.clicked.connect(self.open_records)

        self.choose_game = ChooseGame()
        self.about_project = AboutProject()

    def open_choose_game(self):
        global name_of_player
        name_of_player = QInputDialog.getText(self, 'Получение имени', 'Как Вас зовут?')[0]
        self.choose_game.show()

    def open_about_project(self):
        self.about_project.show()

    def open_records(self):
        self.results = Results()
        self.results.show()


# игра понг
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
            if (paddle.x + 75) - ball.x < 6:
                paddle.x -= (paddle.x + 75) - ball.x
            else:
                paddle.x -= random.randint(5, 6)
        else:
            if ball.x - (paddle.x + 75) < random.randint(5, 6):
                paddle.x += ball.x - (paddle.x + 75)
            else:
                paddle.x += random.randint(6, 6)

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

    # add picture for anim
    def load_image():
        image = pygame.image.load('images\\star.png')
        return image

    # anim
    class Particle(pygame.sprite.Sprite):
        # сгенерируем частицы разного размера
        fire = [load_image()]
        for scale in (5, 10, 20):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))

        def __init__(self, pos, d_x, d_y):
            super().__init__(all_sprites)
            self.image = random.choice(self.fire)
            self.rect = self.image.get_rect()
            # у каждой частицы своя скорость - это вектор
            if d_x > 0:
                d_x = abs(d_x)
            self.velocity = [d_x, d_y]
            # и свои координаты
            self.rect.x, self.rect.y = pos
            # гравитация будет одинаковой
            self.gravity = gravity

        def update(self):
            # применяем гравитационный эффект:
            # движение с ускорением под действием гравитации
            self.velocity[1] += self.gravity
            # перемещаем частицу
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            # убиваем, если частица ушла за экран
            if not self.rect.colliderect(screen_rect):
                self.kill()

    def create_particles(position):
        # количество создаваемых частиц
        particle_count = random.randint(20, 30)
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))
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
    gravity = 0.25
    # stats
    col1 = 0
    col2 = 0
    # background image
    global fon_number
    ball1 = pygame.image.load('images\\Ball_real.png')
    ball1.set_colorkey((0, 0, 0))
    if fon_number == '1':
        img = pygame.image.load('images\\fon1.jpg').convert()
    elif fon_number == '2':
        img = pygame.image.load('images\\fon2.jpg').convert()
    elif fon_number == '3':
        img = pygame.image.load('images\\fon3.jpg').convert()
    elif fon_number == '4':
        img = pygame.image.load('images\\fon4.jpg').convert()
    else:
        img = pygame.image.load('images\\fon.jpg').convert()
    screen_rect = (0, 0, width + 100, height)
    start_ticks = pygame.time.get_ticks()  # starter tick
    # sound and music
    all_sprites = pygame.sprite.Group()
    sound_collision = pygame.mixer.Sound("sounds\\collision.wav")
    sound_loose = pygame.mixer.Sound("sounds\\loose.wav")
    sound_win = pygame.mixer.Sound("sounds\\win.mp3")
    sound_not_win = pygame.mixer.Sound("sounds\\not_win.mp3")
    sound_collision_wall = pygame.mixer.Sound("sounds\\collision_wall.wav")
    start_sound = pygame.mixer.Sound('sounds\\start.wav')
    pygame.mixer.music.load("sounds\\fon.mp3")
    sound_win.set_volume(sound_value / 100)
    start_sound.set_volume(sound_value / 100)
    sound_collision_wall.set_volume(sound_value / 100)
    sound_collision.set_volume(sound_value / 100)
    sound_loose.set_volume(sound_value / 100)
    sound_not_win.set_volume(sound_value / 100)
    running = True
    pygame.mixer.music.play(-1)
    # application name
    pygame.display.set_caption('Pong')
    pygame.mixer.music.set_volume(sound_value / 100)
    while running:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.display.quit()
                pygame.mixer.music.stop()
                return
            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_ESCAPE:
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
                create_particles(ball.center)
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
            database = sqlite3.connect('py_game.db')
            cur = database.cursor()
            cur.execute(f"""INSERT INTO results (
                                                                name,
                                                                game,
                                                                result)
                                                                VALUES (
                                                                '{name_of_player}',
                                                                'Понг',
                                                                'Счет - {str(col1)}:{str(col2)}'
                                                                );""")
            database.commit()
            database.close()
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
        all_sprites.draw(sc)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)


class Sapper:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.board = [[-1] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        count = 0
        while count < mines:
            y, x = random.randint(0, width - 1), random.randint(0, height - 1)
            if self.board[x][y] != 10:
                self.board[x][y] = 10
                count += 1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        global count_of_opened_cells
        count_of_opened_cells = 0
        screen.blit(pygame.font.Font(None, 60).render(f"Жизней: {count_of_lives}", True, 'green'), (75, 925))
        pygame.draw.rect(screen, (0, 255, 0), (100, 800, 100, 50), -1)
        screen.blit(pygame.font.Font(None, 60).render(f"Флагов: {count_of_flags}", True, 'yellow'), (600, 925))
        pygame.draw.rect(screen, (0, 255, 0), (100, 800, 100, 50), -1)

        y = self.top
        for i in self.board:
            x = self.left
            for j in i:
                if j != -1:
                    count_of_opened_cells += 1
                if j == 11:
                    pygame.draw.rect(screen, pygame.Color('red'),
                                     ((x, y), (self.cell_size, self.cell_size)), 0)
                elif j in (12, 13):
                    pygame.draw.rect(screen, pygame.Color('yellow'),
                                     ((x, y), (self.cell_size, self.cell_size)), 0)
                elif (j >= 0) and (j != 10) and (j != 11):
                    screen.blit(pygame.font.Font(None, 50).render(str(j), True, (0, 255, 0)), (x, y))
                    pygame.draw.rect(screen, (0, 255, 0), (x, y, self.cell_size, self.cell_size), 1)
                pygame.draw.rect(screen, pygame.Color('white'),
                                 ((x, y), (self.cell_size, self.cell_size)), 1)
                x += self.cell_size
            y += self.cell_size

    def get_click(self, mouse_pos, button):
        cell = self.get_cell(mouse_pos)
        if cell:
            if button == 1:
                self.open_cell(cell)
            elif button == 3:
                self.put_up_flag(cell)
            return
        print(None)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if x > self.width - 1 or y > self.height - 1 or x < 0 or y < 0:
            return None
        return list([x, y])

    def number_of_neighbors(self, cell):
        number = 0
        try:
            number += (self.board[cell[1] - 1][cell[0] - 1] in (10, 11, 12))
        except IndexError:
            pass
        try:
            number += (self.board[cell[1]][cell[0] - 1] in (10, 11, 12))
        except IndexError:
            pass
        try:
            number += (self.board[cell[1] + 1][cell[0] - 1] in (10, 11, 12))
        except IndexError:
            pass
        try:
            number += (self.board[cell[1] - 1][cell[0]] in (10, 11, 12))
        except IndexError:
            pass
        try:
            number += (self.board[cell[1] + 1][cell[0]] in (10, 11, 12))
        except IndexError:
            pass
        try:
            number += (self.board[cell[1] - 1][cell[0] + 1] in (10, 11, 12))
        except IndexError:
            pass
        try:
            number += (self.board[cell[1]][cell[0] + 1] in (10, 11, 12))
        except IndexError:
            pass
        try:
            number += (self.board[cell[1] + 1][cell[0] + 1] in (10, 11, 12))
        except IndexError:
            pass
        return number

    def open_cell(self, cell):
        global count_of_lives, count_of_opened_cells
        stock = cell[:]
        if self.board[cell[1]][cell[0]] == 10:
            self.board[cell[1]][cell[0]] = 11
            count_of_lives -= 1
            count_of_opened_cells += 1
            print(count_of_lives)
        elif self.board[cell[1]][cell[0]] == -1:
            self.board[cell[1]][cell[0]] = self.number_of_neighbors(cell)
            while True:
                try:
                    number = self.number_of_neighbors(cell)
                    self.board[cell[1]][cell[0]] = number
                    cell[0] -= 1
                    if cell[0] < 0 or number > 0 or self.board[cell[1]][cell[0]] > -1:
                        break
                except IndexError:
                    break
            cell = stock[:]
            while True:
                try:
                    number = self.number_of_neighbors(cell)
                    self.board[cell[1]][cell[0]] = number
                    cell[0] += 1
                    if cell[0] > self.width or number > 0 or self.board[cell[1]][cell[0]] > -1:
                        break
                except IndexError:
                    break
            cell = stock[:]
            while True:
                try:
                    number = self.number_of_neighbors(cell)
                    self.board[cell[1]][cell[0]] = number
                    cell[1] -= 1
                    if cell[1] < 0 or number > 0 or self.board[cell[1]][cell[0]] > -1:
                        break
                except IndexError:
                    break
            cell = stock[:]
            while True:
                try:
                    number = self.number_of_neighbors(cell)
                    self.board[cell[1]][cell[0]] = number
                    cell[1] += 1
                    if cell[1] > self.height or number > 0 or self.board[cell[1]][cell[0]] > -1:
                        break
                except IndexError:
                    break

    def put_up_flag(self, cell):
        global count_of_flags, count_of_opened_cells
        if (self.board[cell[1]][cell[0]] in (-1, 10)) and (count_of_flags > 0):
            if self.board[cell[1]][cell[0]] == 10:
                self.board[cell[1]][cell[0]] = 12
            else:
                self.board[cell[1]][cell[0]] = 13
            count_of_flags -= 1
            count_of_opened_cells += 1


# игровой цикл
def miner():
    pygame.init()
    screen = pygame.display.set_mode((900, 1000))
    screen.fill((0, 0, 0))
    board = Sapper(22, 22, 22)
    board.set_view(10, 10, 40)
    running = True

    while running:
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                pygame.display.quit()
                pygame.mixer.music.stop()
                return
            if event2.type == pygame.MOUSEBUTTONDOWN:
                if count_of_lives > 0:
                    board.get_click(event2.pos, event2.button)

        screen.fill((0, 0, 0))
        if (count_of_lives > 0) and (count_of_opened_cells < 484):
            board.render(screen)
        else:
            font = pygame.font.Font(None, 60)
            text = font.render(f"Игра окончена!", True, 'yellow')
            screen.blit(text, (310, 200))
            pygame.draw.rect(screen, (0, 255, 0), (100, 800, 100, 50), -1)
            text = font.render(f"Осталось жизней: {count_of_lives}", True, 'red')
            screen.blit(text, (258, 300))
            pygame.draw.rect(screen, (0, 255, 0), (100, 800, 100, 50), -1)
            text = font.render(f"Открыто клеток: {count_of_opened_cells}", True, 'blue')
            screen.blit(text, (270, 400))
            pygame.draw.rect(screen, (0, 255, 0), (100, 800, 100, 50), -1)
            if count_of_opened_cells == 484:
                text = font.render(f"Вы победили!", True, (128, 166, 255))
            else:
                text = font.render(f"Вы проиграли", True, (255, 203, 219))
            screen.blit(text, (320, 500))
            pygame.draw.rect(screen, (0, 255, 0), (100, 800, 100, 50), -1)
        pygame.display.flip()
    print(name_of_player)


colors = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 69, 0)
]

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

level = 1
lines_to_clear = 1


# игра тетрис
class Tetris:
    lines_cleared = 0
    score = 0
    state = "start"
    field = []
    HEIGHT = 0
    WIDTH = 0
    startX = 10
    startY = 50
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.field = []
        self.figure = None
        self.height = height
        self.width = width
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def create_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersects = False
        for i in range(4):
            for j in range(4):
                if (i * 4) + j in self.figure.get_image():
                    if (i + self.figure.y) > (self.height - 1) or \
                        (j + self.figure.x) > (self.width - 1) or \
                        (j + self.figure.x) < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersects = True
        return intersects

    def freeze_figure(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.get_image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.create_figure()
        if self.intersects():
            self.state = "gameover"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(0, self.width):
                if self.field[i][j] == 0:
                    zeros += 1

            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]

        self.score += lines ** 2
        self.lines_cleared += lines
        self.check_level_up()

    def check_level_up(self):
        global level
        global lines_to_clear
        if self.lines_cleared >= level:
            level += 1
            lines_to_clear = level
            self.lines_cleared = 0
            return True
        else:
            lines_to_clear = level - self.lines_cleared
            return False

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze_figure()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze_figure()

    def go_sideways(self, dx):
        previous_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = previous_x

    def rotate(self):
        previous_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():

            self.figure.rotation = previous_rotation


# класс для тетриса
class Figure:
    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
        [[5, 6, 9, 10]],
        [[1, 2, 4, 5], [0, 4, 5, 9], [5, 6, 8, 9], [1, 5, 6, 10]],
        [[1, 2, 6, 7], [3, 6, 7, 10], [5, 6, 10, 11], [2, 5, 6, 9]]
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, (len(self.figures) - 1))
        self.color = random.randint(1, (len(colors) - 1))
        self.rotation = 0

    def get_image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % (len(self.figures[self.type]))


# игровой цикл
def tetris():
    global level, event, record
    global lines_to_clear
    screen_height = 400
    screen_width = 452
    game_height = 20
    game_width = 10
    pressing_down = False
    gameover = False
    counter = 0
    fps = 30

    pygame.init()
    window = pygame.display.set_mode((screen_height, screen_width), pygame.NOFRAME)
    clock = pygame.time.Clock()
    game = Tetris(game_height, game_width)

    while not gameover:
        if game.figure is None:
            game.create_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.go_sideways(1)
                if event.key == pygame.K_LEFT:
                    game.go_sideways(-1)
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    return
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
        window.fill(BLACK)
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(window, GREY, [game.startX + game.zoom * j, game.startY + game.zoom * i,
                                                game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(window, colors[game.field[i][j]],
                                     [game.startX + game.zoom * j, game.startY + game.zoom * i,
                                      game.zoom - 2, game.zoom - 1])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.get_image():
                        pygame.draw.rect(window, colors[game.figure.color],
                                         [
                                             game.startX + game.zoom * (j + game.figure.x) + 1,
                                             game.startY + game.zoom * (i + game.figure.y) + 1,
                                             game.zoom - 2,
                                             game.zoom - 2
                                         ])

        record = str(game.score)
        font1 = pygame.font.SysFont('Engravers MT', 21, bold=True)
        title_tetris = font1.render("TETRIS", True, WHITE)
        text_score = font1.render("Score: " + str(game.score), True, WHITE)
        text_level = font1.render("Level: " + str(level), True, WHITE)
        text_lines_to_clear = font1.render("Lines to clear: " + str(lines_to_clear), True, WHITE)
        text_game_over1 = font1.render("Game Over", True, WHITE)
        text_game_over2 = font1.render("Press ESC", True, WHITE)

        window.blit(text_score, [220, 20])
        window.blit(text_lines_to_clear, [220, 60])
        window.blit(text_level, [220, 40])
        window.blit(title_tetris, [61, 10])
        if game.check_level_up():
            tetris()
        if game.state == "gameover":
            window.blit(text_game_over1, [220, 220])
            window.blit(text_game_over2, [220, 275])
            break
        pygame.display.flip()
        clock.tick(fps)


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


path = resource_path(os.path.join('Folder', 'images\\icon.jpg'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Menu()
    exe.show()
    sys.exit(app.exec())
