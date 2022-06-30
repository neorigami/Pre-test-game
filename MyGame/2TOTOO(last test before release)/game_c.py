import pygame
import random
import os.path
from os import path

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

LENGTH = 80  # size of stick
WIDE = 9  # size of stick
SPEEDX = 10
d_speed = {'easy': 30, 'medium': 35, 'hard': 40, 'immortal': 50}
immortal_speeds = {0.5: (10, 0), 0.75: (8, 1), 1: (3, 0), 1.25: (2, 2), 1.5: (1, 3)}
WIDTH = 800  # ширина игрового окна
HEIGHT = 800  # высота игрового окна
FPS = 60  # частота кадров в секунду


class DotMouse(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((5, 5))
        # self.image.fill(WHITE)
        self.image = dot_img
        self.image = pygame.transform.scale(dot_img, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 15
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        if min(self.rect.center) < 0:
            self.rect.center = 0
        if max(self.rect.center) > WIDTH:
            self.rect.center = WIDTH
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x, mouse_y)


class Comet(pygame.sprite.Sprite):
    score = 0  # total score
    add = 2  # acceleration adding to score
    level = None

    def __init__(self, speed, cycle, side=0):
        pygame.sprite.Sprite.__init__(self)
        self.side = side  # select parameter from cycle
        self.cycle = cycle
        self.x_0 = 0
        self.xy = 0
        self.immortal_speed = 0
        self.image_comet = img_comet_1
        self.group_image = img_comet
        self.coor = self.cycle[self.side]
        self.speed = speed  # speed of stick
        self.direction = self.coor[2]  # direction of moving from walls
        # self.image = pygame.Surface(self.coor[3])
        self.image = self.image_comet
        self.stick_i = 0
        # self.image = pygame.transform.scale(stick_img, (50, 100))
        self.image = pygame.transform.rotate(self.image, self.coor[4])
        self.image.set_colorkey(BLACK)
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.random_size = 1
        self.radius = WIDE*2
        self.rect.center = (self.coor[0], self.coor[1])
        self.memory_speed = SPEEDX
        self.pause = 0

    @classmethod
    def level(cls, level, score=score, add=add):
        cls.level = level
        cls.score = score
        cls.add = add

    def update(self):
        if self.immortal_speed < immortal_speeds[self.random_size][0]:
            if self.direction == 'x':  # direction of moving from walls
                self.rect.x += 1  # speed of moving
            elif self.direction == 'y':
                self.rect.y += 1
            elif self.direction == '-x':  # direction of moving from walls
                self.rect.x += -1  # speed of moving
            elif self.direction == '-y':
                self.rect.y += -1
            if self.direction in ('xy', '-xy', 'x-y', '-x-y'):
                if self.xy < 3:
                    if self.direction == 'xy':
                        self.rect.y += 1
                        self.rect.x += 1
                        # pygame.Rect.move(self.rect, 1, 1)
                    elif self.direction == '-xy':
                        self.rect.y += 1
                        self.rect.x += -1
                        # pygame.Rect.move(self.rect, -1, 1)
                    elif self.direction == 'x-y':
                        self.rect.y += -1
                        self.rect.x += 1
                        # pygame.Rect.move(self.rect, 1, -1)
                    elif self.direction == '-x-y':
                        self.rect.y += -1
                        self.rect.x += -1
                        # pygame.Rect.move(self.rect, -1, -1)
                    self.xy += 1
                else:
                    self.xy = 0
            self.immortal_speed += 1
        else:
            if self.pause < immortal_speeds[self.random_size][1]:
                self.pause += 1
            else:
                self.immortal_speed = 0
                self.pause = 0

        self.x_0 += 1
        if self.x_0 == group_img_comets[self.random_size][2]:  # group_img_comets[self.random_size][2]
            self.stick_i = stick_img_cycle(self.stick_i)
            self.image = pygame.transform.rotate(self.group_image[self.stick_i], self.coor[4])
            # self.image.set_colorkey(BLACK)
            # self.image = pygame.transform.rotozoom(self.group_image[self.stick_i], self.coor[4], 2 - self.random_size)
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            # self.radius = int(WIDE * (2 * self.random_size)) - 5
            self.image.set_colorkey(BLACK)
            self.x_0 = 0

        if min(self.rect.center) < -50 or max(self.rect.center) > WIDTH + 50:
            point_sound.play()

            if Comet.level == 'easy':  # put in all level limit of speed
                cycle = ((0, random.randint(LENGTH // 2 , WIDTH - LENGTH + 1), 'x', (WIDE, LENGTH), 90, LENGTH, WIDE*2+5),
                            (random.randint(LENGTH // 2 - 10, WIDTH - LENGTH + 1), 0, 'y', (LENGTH, WIDE), 0, WIDE*2+5, LENGTH),
                            (WIDTH, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), '-x', (WIDE, LENGTH), -90, WIDE+10, WIDE*2+5),
                            (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), HEIGHT, '-y', (LENGTH, WIDE), -180, WIDE*2+5, WIDE+10))
                self.cycle = cycle
                self.side += 1
                Comet.score += Comet.add * 10
                if self.side == 4:
                    self.side = 0
                if Comet.score > Comet.add * 2 * 10 and self.memory_speed < SPEEDX + 20:
                    Comet.add += 2
                    self.memory_speed += 1

            if Comet.level == 'medium':
                cycle = (
                    (0, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 'x', (WIDE, LENGTH), 90, LENGTH, WIDE * 2 + 5),
                    (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 0, 'y', (LENGTH, WIDE), 0, WIDE * 2 + 5, LENGTH),
                    (WIDTH, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), '-x', (WIDE, LENGTH), -90, WIDE + 10,
                     WIDE * 2 + 5),
                    (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), HEIGHT, '-y', (LENGTH, WIDE), -180, WIDE * 2 + 5,
                     WIDE + 10))
                self.cycle = cycle
                self.side = random.randint(0, 3)
                Comet.score += Comet.add * 15
                if Comet.score > Comet.add * 3 * 10 and self.memory_speed < SPEEDX + 25:
                    Comet.add += 5
                    self.memory_speed += 1

            if Comet.level == 'hard':
                cycle_hard = ((0, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 'x', (WIDE, LENGTH), 90, LENGTH, WIDE * 2+5),
                              (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 0, 'y', (LENGTH, WIDE), 0, WIDE * 2 + 5, LENGTH),
                              (WIDTH, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), '-x', (WIDE, LENGTH), -90, WIDE + 10, WIDE * 2 + 5),
                              (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), HEIGHT, '-y', (LENGTH, WIDE), -180, WIDE * 2 + 5, WIDE + 10),
                              (0, random.randint(0, WIDTH // 4), 'xy', (WIDE, LENGTH), 45, LENGTH, LENGTH),  # lu
                              (random.randint(0, WIDTH // 4), 0, 'xy', (WIDE, LENGTH), 45, LENGTH, LENGTH),  # lu
                              (0, random.randint(WIDTH // 4 * 3, WIDTH + 1), 'x-y', (WIDE, LENGTH), 135, LENGTH, WIDE * 2 + 5),  # ld
                              (random.randint(0, WIDTH // 4), HEIGHT, 'x-y', (WIDE, LENGTH), 135, LENGTH, WIDE * 2 + 5),  # ld
                              (random.randint(WIDTH // 4 * 3, WIDTH + 1), 0, '-xy', (WIDE, LENGTH), -45, WIDE * 2 + 5, LENGTH),  # ru
                              (WIDTH, random.randint(0, WIDTH // 4), '-xy', (WIDE, LENGTH), -45, WIDE * 2 + 5, LENGTH),  # ru
                              (WIDTH, random.randint(WIDTH // 4 * 3, WIDTH + 1), '-x-y', (WIDE, LENGTH), 225, WIDE * 2 + 5, WIDE * 2 + 5),  # rd
                              (random.randint(WIDTH // 4 * 3, WIDTH + 1), HEIGHT, '-x-y', (WIDE, LENGTH), 225, WIDE * 2 + 5, WIDE * 2 + 5))  # rd
                self.cycle = cycle_hard
                self.side = random.randint(0, 11)
                Comet.score += Comet.add * 30
                if Comet.score > Comet.add * 5 * 10 * 2 and self.memory_speed < SPEEDX + 25:
                    Comet.add += 10
                    self.memory_speed += 1
            if Comet.level == 'immortal':
                cycle_hard = (
                (0, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 'x', (WIDE, LENGTH), 90, LENGTH, WIDE * 2 + 5),
                (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 0, 'y', (LENGTH, WIDE), 0, WIDE * 2 + 5, LENGTH),
                (WIDTH, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), '-x', (WIDE, LENGTH), -90, WIDE + 10,
                 WIDE * 2 + 5),
                (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), HEIGHT, '-y', (LENGTH, WIDE), -180, WIDE * 2 + 5,
                 WIDE + 10),
                (0, random.randint(0, WIDTH // 4), 'xy', (WIDE, LENGTH), 45, LENGTH, LENGTH),  # lu
                (random.randint(0, WIDTH // 4), 0, 'xy', (WIDE, LENGTH), 45, LENGTH, LENGTH),  # lu
                (0, random.randint(WIDTH // 4 * 3, WIDTH + 1), 'x-y', (WIDE, LENGTH), 135, LENGTH, WIDE * 2 + 5),  # ld
                (random.randint(0, WIDTH // 4), HEIGHT, 'x-y', (WIDE, LENGTH), 135, LENGTH, WIDE * 2 + 5),  # ld
                (random.randint(WIDTH // 4 * 3, WIDTH + 1), 0, '-xy', (WIDE, LENGTH), -45, WIDE * 2 + 5, LENGTH),  # ru
                (WIDTH, random.randint(0, WIDTH // 4), '-xy', (WIDE, LENGTH), -45, WIDE * 2 + 5, LENGTH),  # ru
                (WIDTH, random.randint(WIDTH // 4 * 3, WIDTH + 1), '-x-y', (WIDE, LENGTH), 225, WIDE * 2 + 5,
                 WIDE * 2 + 5),  # rd
                (random.randint(WIDTH // 4 * 3, WIDTH + 1), HEIGHT, '-x-y', (WIDE, LENGTH), 225, WIDE * 2 + 5,
                 WIDE * 2 + 5))  # rd
                self.cycle = cycle_hard
                self.side = random.randint(0, 11)
                self.random_size = random.choice((0.5, 0.75, 1, 1.25, 1.5))
                Comet.score += Comet.add * 50
                if Comet.score > Comet.add * 10 * 10 * 3 and self.memory_speed < SPEEDX + 25:
                    Comet.add += 20
                    self.memory_speed += 1
                self.group_image = group_img_comets[self.random_size][0]
                self.image_comet = self.group_image[0]
                self.image = self.image_comet
                self.image.set_colorkey(BLACK)

            self.coor = self.cycle[self.side]
            # self.image = pygame.Surface(self.coor[3])
            # self.image.fill(RED)
            # self.image = pygame.transform.rotozoom(stick_img_1, 0, self.random_size)
            self.image = pygame.transform.rotate(self.image_comet, self.coor[4])
            self.image.set_colorkey(BLACK)

            self.rect = self.image.get_rect()  # centerx=self.coor[5], centery=self.coor[6]
            # if Stick.level == 'immortal':
            #     if self.random_size > 1:
            #         self.radius = int(WIDE * (2 - self.random_size)) - 3
            #     else:
            #         self.radius = int(WIDE * 2 * (2 - self.random_size)) - 3
            # self.radius = int(WIDE * (2 * self.random_size)) - 5
            self.radius = group_img_comets[self.random_size][1]
            self.rect.center = (self.coor[0], self.coor[1])
            self.direction = self.coor[2]
            self.x_0 = 0
            self.pause = 0


class FinalCircle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.scale = 1.0
        self.angle = 1.0
        # self.image = random.choice(final_circle)
        self.image_circle = random.choice(final_circle)
        self.image = self.image_circle
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2 - 65
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.complete = False

    def update(self):
        self.image = pygame.transform.rotozoom(self.image_circle, self.angle, self.scale)
        if self.scale > 0.1:
            self.scale -= 0.003
            self.angle += 1

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius -= (1.05 + self.scale * self.scale)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        if self.scale < 0.1 or self.radius < 8:
            self.complete = True


class Button(pygame.sprite.Sprite):
    # click = False

    def __init__(self, text, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300, 100))
        self.click = False
        # self.image.fill(WHITE)
        # self.image.set_colorkey(BLACK)
        self.text = text
        draw_text(self.image, text, 30, 150, 35)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if pygame.sprite.collide_rect(self, dot):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True


class NickName:
    name = None

    def __init__(self, name):
        self.name = name

    @classmethod
    def nick_name(cls, name):
        return cls.name


class TriangleButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.click = False
        self.image.set_colorkey(BLACK)
        pygame.draw.polygon(self.image, WHITE, ((15, 0), (0, 30), (30, 30)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if pygame.sprite.collide_rect(self, dot):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True


class TriangleButtonDown(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.click = False
        self.image.set_colorkey(BLACK)
        pygame.draw.polygon(self.image, RED, ((0, 0), (30, 0), (15, 30)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if pygame.sprite.collide_rect(self, dot):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True


class VolumeLevel(pygame.sprite.Sprite):
    def __init__(self, x, y, volume_fill=0.5):
        pygame.sprite.Sprite.__init__(self)
        self.volume_fill = volume_fill
        self.x, self.y = x, y
        self.image = pygame.Surface((20, int(200 * self.volume_fill)))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

    def update(self):
        if self.volume_fill < 0.1:
            self.image = pygame.Surface((20, 1))
        else:
            self.image = pygame.Surface((20, int(200 * self.volume_fill)))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        pass


def start_menu():
    button_play = Button('Play', WIDTH // 2, 200)
    button_setting = Button('Setting', WIDTH // 2, 350)
    button_score = Button('Score', WIDTH // 2, 500)
    button_quit = Button('Quit', WIDTH // 2, 650)
    sprite_screen = pygame.sprite.Group()
    sprite_screen.add(button_play)
    sprite_screen.add(button_setting)
    sprite_screen.add(button_score)
    sprite_screen.add(button_quit)
    sprite_screen.add(dot)

    waiting = True
    while waiting:
        clock.tick(FPS)
        sprite_screen.update()
        screen.blit(background, background_rect)
        sprite_screen.draw(screen)
        draw_text(screen, "2TO10", 60, WIDTH // 2, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return False
        if button_quit.click:
            return False
        if button_score.click:
            button_score.click = score()
        if button_setting.click:
            button_setting.click = setting()
        if button_play.click:
            waiting = False
            # pygame.time.wait(100)
            # return choose_level_menu()
            if not choose_level_menu():
                waiting = True
                button_play.click = False
            else:
                return True
        pygame.display.flip()


def setting():
    global volume_point_sound, volume_mixer_music, volume_final_sound, volume_endgame_sound, volume_leading_sound,\
        volume_congratulation_sound, general_sound, all_volume
    if os.path.exists('setting_save.txt'):
        file = open('setting_save.txt', 'r', encoding='utf-8')
        setting_file = file.readlines()
        setting_file = list(map(lambda x: x.strip().split(), setting_file))
        setting_data = {i[0]: float(i[1]) for i in setting_file}
        file.close()
        for setting, volume in zip(setting_data, all_volume):
            if volume != setting_data[setting]:
                volume = setting_data[setting]
    button_back = Button('Back', WIDTH // 4 - 10, 725)
    button_reset = Button('Reset', WIDTH // 4 * 3 + 10, 725)
    button_triangle_up_1 = TriangleButton(100 - 30, 500)  # volume_point_sound
    button_triangle_up_2 = TriangleButton(200 - 20, 500)  # volume_mixer_music
    button_triangle_up_3 = TriangleButton(300 - 10, 500)  # volume_final_sound
    button_triangle_up_4 = TriangleButton(400, 500)  # volume_endgame_sound
    button_triangle_up_5 = TriangleButton(500 + 10, 500)  # volume_leading_sound
    button_triangle_up_6 = TriangleButton(600 + 20, 500)  # volume_congratulation_sound
    button_triangle_up_7 = TriangleButton(700 + 30, 500)  # general volume
    button_triangle_down_1 = TriangleButtonDown(100 - 30, 550)
    button_triangle_down_2 = TriangleButtonDown(200 - 20, 550)
    button_triangle_down_3 = TriangleButtonDown(300 - 10, 550)
    button_triangle_down_4 = TriangleButtonDown(400, 550)
    button_triangle_down_5 = TriangleButtonDown(500 + 10, 550)
    button_triangle_down_6 = TriangleButtonDown(600 + 20, 550)
    button_triangle_down_7 = TriangleButtonDown(700 + 30, 550)
    volume_colum_1 = VolumeLevel(100 - 30, 400, volume_fill=volume_point_sound)
    volume_colum_2 = VolumeLevel(200 - 20, 400, volume_fill=volume_mixer_music * 10)
    volume_colum_3 = VolumeLevel(300 - 10, 400, volume_fill=volume_final_sound)
    volume_colum_4 = VolumeLevel(400, 400, volume_fill=volume_endgame_sound)
    volume_colum_5 = VolumeLevel(500 + 10, 400, volume_fill=volume_leading_sound)
    volume_colum_6 = VolumeLevel(600 + 20, 400, volume_fill=volume_congratulation_sound)
    volume_colum_7 = VolumeLevel(700 + 30, 400, volume_fill=general_sound)
    triangle_buttons = (button_triangle_up_1, button_triangle_up_2, button_triangle_up_3, button_triangle_up_4,
                        button_triangle_up_5, button_triangle_up_6, button_triangle_up_7,
                        button_triangle_down_1, button_triangle_down_2, button_triangle_down_3, button_triangle_down_4,
                        button_triangle_down_5, button_triangle_down_6, button_triangle_down_7,
                        volume_colum_1,  volume_colum_2,  volume_colum_3,  volume_colum_4,  volume_colum_5,
                        volume_colum_6,  volume_colum_7)

    sprite_screen_options = pygame.sprite.Group()
    sprite_screen_options.add(button_back)
    for button in triangle_buttons:
        sprite_screen_options.add(button)
    sprite_screen_options.add(button_reset)
    sprite_screen_options.add(dot)
    waiting_s = True
    while waiting_s:
        clock.tick(FPS)
        sprite_screen_options.update()
        screen.blit(background, background_rect)
        text_description = ('point', 'music', 'final sound', 'fail sound', 'speed sound', 'win sound', 'general')
        for i in range(7):
            area_volume = pygame.Surface((20, 200))
            area_volume.fill(BLACK)
            area_volume = pygame.transform.rotate(area_volume, 180)
            screen.blit(area_volume, (90 + i * 110 - 30, 200))
            back = pygame.Surface((100, 60))
            # back.get_rect().midbottom = (10 + i * 100, 100)
            screen.blit(back, (25 + i * 110, 130))
            if len(text_description[i].split()) == 2:
                draw_text(screen, text_description[i].split()[0].upper(), 20, 75 + i * 110, 135)
                draw_text(screen, text_description[i].split()[1].upper(), 20, 75 + i * 110, 160)
            else:
                draw_text(screen, text_description[i].upper(), 20, 75 + i * 110, 150)
        draw_text(screen, "2TO10", 60, WIDTH // 2, 0)
        sprite_screen_options.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                setting_save(volume_point_sound=volume_point_sound, volume_mixer_music=volume_mixer_music,
                             volume_final_sound=volume_final_sound, volume_endgame_sound=volume_endgame_sound,
                             volume_leading_sound=volume_leading_sound,
                             volume_congratulation_sound=volume_congratulation_sound, general_sound=general_sound)
                waiting_s = False
                waiting = False
                pygame.quit()
        if button_back.click:
            waiting_s = False
            setting_save(volume_point_sound=volume_point_sound, volume_mixer_music=volume_mixer_music,
                             volume_final_sound=volume_final_sound, volume_endgame_sound=volume_endgame_sound,
                             volume_leading_sound=volume_leading_sound,
                             volume_congratulation_sound=volume_congratulation_sound, general_sound=general_sound)
            return False
        if any((button_triangle_up_1.click, button_triangle_up_2.click, button_triangle_up_3.click,
               button_triangle_up_4.click, button_triangle_up_5.click, button_triangle_up_6.click,
               button_triangle_up_7.click, button_triangle_down_1.click, button_triangle_down_2.click,
               button_triangle_down_3.click, button_triangle_down_3.click, button_triangle_down_4.click,
               button_triangle_down_5.click, button_triangle_down_6.click, button_triangle_down_7.click,
                button_reset.click)):
            for track in (point_sound, final_sound_5, endgame3_sound, leading_sound_5, congratulation_sound_2):
                track.stop()
            if button_triangle_up_1.click:
                button_triangle_up_1.click = False
                if volume_point_sound < 1.0:
                    volume_point_sound += 0.1
                    volume_colum_1.volume_fill += 0.1
                    point_sound.set_volume(volume_point_sound * general_sound)
                    point_sound.play()
            if button_triangle_down_1.click:
                button_triangle_down_1.click = False
                if volume_point_sound > 0.0:
                    volume_point_sound -= 0.1
                    volume_colum_1.volume_fill -= 0.1
                    point_sound.set_volume(volume_point_sound * general_sound)
                    point_sound.play()
            if button_triangle_up_2.click:
                button_triangle_up_2.click = False
                if volume_mixer_music < 0.1:
                    volume_mixer_music += 0.01
                    volume_colum_2.volume_fill += 0.1
                    pygame.mixer.music.set_volume(volume_mixer_music * general_sound)
            if button_triangle_down_2.click:
                button_triangle_down_2.click = False
                if volume_mixer_music > 0.0:
                    volume_mixer_music -= 0.01
                    volume_colum_2.volume_fill -= 0.1
                    pygame.mixer.music.set_volume(volume_mixer_music * general_sound)
            if button_triangle_up_3.click:
                button_triangle_up_3.click = False
                if volume_final_sound < 1.0:
                    volume_final_sound += 0.1
                    volume_colum_3.volume_fill += 0.1
                    for track in final:
                        track.set_volume(volume_final_sound * general_sound)
                    final_sound_5.play()
            if button_triangle_down_3.click:
                button_triangle_down_3.click = False
                if volume_final_sound > 0.0:
                    volume_final_sound -= 0.1
                    volume_colum_3.volume_fill -= 0.1
                    for track in final:
                        track.set_volume(volume_final_sound * general_sound)
                    final_sound_5.play()
            if button_triangle_up_4.click:
                button_triangle_up_4.click = False
                if volume_endgame_sound < 1.0:
                    volume_endgame_sound += 0.1
                    volume_colum_4.volume_fill += 0.1
                    for track in endgame:
                        track.set_volume(volume_endgame_sound * general_sound)
                    endgame3_sound.play()
            if button_triangle_down_4.click:
                button_triangle_down_4.click = False
                if volume_endgame_sound > 0.0:
                    volume_endgame_sound -= 0.1
                    volume_colum_4.volume_fill -= 0.1
                    for track in endgame:
                        track.set_volume(volume_endgame_sound * general_sound)
                    endgame3_sound.play()
            if button_triangle_up_5.click:
                button_triangle_up_5.click = False
                if volume_leading_sound < 1.0:
                    volume_leading_sound += 0.1
                    volume_colum_5.volume_fill += 0.1
                    for track in leading:
                        track.set_volume(volume_leading_sound * general_sound)
                    leading_sound_5.play()
            if button_triangle_down_5.click:
                button_triangle_down_5.click = False
                if volume_leading_sound > 0.0:
                    volume_leading_sound -= 0.1
                    volume_colum_5.volume_fill -= 0.1
                    for track in leading:
                        track.set_volume(volume_leading_sound * general_sound)
                    leading_sound_5.play()
            if button_triangle_up_6.click:
                button_triangle_up_6.click = False
                if volume_congratulation_sound < 1.0:
                    volume_congratulation_sound += 0.1
                    volume_colum_6.volume_fill += 0.1
                    for track in congratulation:
                        track.set_volume(volume_congratulation_sound * general_sound)
                    congratulation_sound_2.play()
            if button_triangle_down_6.click:
                button_triangle_down_6.click = False
                if volume_congratulation_sound > 0.0:
                    volume_congratulation_sound -= 0.1
                    volume_colum_6.volume_fill -= 0.1
                    for track in congratulation:
                        track.set_volume(volume_congratulation_sound * general_sound)
                    congratulation_sound_2.play()
            if button_triangle_up_7.click:
                button_triangle_up_7.click = False
                if general_sound < 1.0:
                    general_sound += 0.1
                    volume_colum_7.volume_fill += 0.1
                    for track in endgame:
                        track.set_volume(volume_endgame_sound * general_sound)
                    for track in congratulation:
                        track.set_volume(volume_congratulation_sound * general_sound)
                    for track in final:
                        track.set_volume(volume_final_sound * general_sound)
                    for track in leading:
                        track.set_volume(volume_leading_sound * general_sound)
                    point_sound.set_volume(volume_point_sound * general_sound)
                    pygame.mixer.music.set_volume(volume_mixer_music * general_sound)
            if button_triangle_down_7.click:
                button_triangle_down_7.click = False
                if general_sound > 0.0:
                    general_sound -= 0.1
                    volume_colum_7.volume_fill -= 0.1
                    for track in endgame:
                        track.set_volume(volume_endgame_sound * general_sound)
                    for track in congratulation:
                        track.set_volume(volume_congratulation_sound * general_sound)
                    for track in final:
                        track.set_volume(volume_final_sound * general_sound)
                    for track in leading:
                        track.set_volume(volume_leading_sound * general_sound)
                    point_sound.set_volume(volume_point_sound * general_sound)
                    pygame.mixer.music.set_volume(volume_mixer_music * general_sound)
            if button_reset.click:
                button_reset.click = False
                volume_mixer_music = 0.1
                volume_point_sound = 0.8
                volume_endgame_sound = 0.5
                volume_leading_sound = 0.5
                volume_final_sound = 0.5
                volume_congratulation_sound = 0.5
                general_sound = 1.0
                volume_colum_1.volume_fill = volume_point_sound
                volume_colum_2.volume_fill = volume_mixer_music * 10
                volume_colum_3.volume_fill = volume_endgame_sound
                volume_colum_4.volume_fill = volume_leading_sound
                volume_colum_5.volume_fill = volume_final_sound
                volume_colum_6.volume_fill = volume_congratulation_sound
                volume_colum_7.volume_fill = general_sound
                for track in endgame:
                    track.set_volume(volume_endgame_sound * general_sound)
                for track in congratulation:
                    track.set_volume(volume_congratulation_sound * general_sound)
                for track in final:
                    track.set_volume(volume_final_sound * general_sound)
                for track in leading:
                    track.set_volume(volume_leading_sound * general_sound)
                point_sound.set_volume(volume_point_sound * general_sound)
                pygame.mixer.music.set_volume(volume_mixer_music * general_sound)
        pygame.display.flip()


def score():
    button_back = Button('Back', WIDTH // 4 - 10, 725)
    button_reset = Button('Reset', WIDTH // 4 * 3 + 10, 725)
    sprite_screen_score = pygame.sprite.Group()
    sprite_screen_score.add(button_back)
    sprite_screen_score.add(button_reset)
    sprite_screen_score.add(dot)

    waiting_s = True
    while waiting_s:
        clock.tick(FPS)
        sprite_screen_score.update()
        screen.blit(background, background_rect)
        draw_text(screen, "2TO10", 60, WIDTH // 2, 0)
        field_score = pygame.Surface((600, 550))
        screen.blit(field_score, (100, 80))
        sprite_screen_score.draw(screen)
        if os.path.exists('score_data.txt'):
            file = open('score_data.txt', 'r', encoding='utf-8')
            data_file = list(map(lambda x: x.strip().split(), file.readlines()))
            data_score = {data[0]: int(data[1]) for data in data_file}
            amount = len(data_score)
            file.close()
            if len(data_file) == 0:
                draw_text(screen, "No results", 60, WIDTH // 2, 200)
            else:
                for data, num in zip(data_score, range(1, amount+1)):
                    font = pygame.font.Font(None, 40)
                    space_text = font.render(f'{num}.{data}{data_score[data]}', True, WHITE)
                    space = font.render(" ", True, WHITE)
                    draw_text(screen, f'{num}. {data}{" "*((420 - space_text.get_width())//space.get_width())}{data_score[data]}', 40, WIDTH // 2, 40 + num * 40)
                    if num == 10:
                        break
        else:
            draw_text(screen, "No results", 60, WIDTH // 2, 200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_s = False
                waiting = False
                pygame.quit()
        if button_back.click:

            # waiting_s = False
            return False
        if button_reset.click:
            button_reset.click = False
            field_score = pygame.Surface((600, 550))
            screen.blit(field_score, (100, 80))
            file = open('score_data.txt', 'w', encoding='utf-8')
            file.close()
        pygame.display.flip()


def setting_save(**kwargs):
    try:
        file = open('setting_save.txt', 'r', encoding='utf-8')
        setting_file = file.readlines()
        setting_file = list(map(lambda x: x.strip().split(), setting_file))
        setting_data = {i[0]: float(i[1]) for i in setting_file}
    except:
        global volume_point_sound, volume_mixer_music, volume_final_sound, volume_endgame_sound, volume_leading_sound, \
            volume_congratulation_sound, general_sound
        file = open('setting_save.txt', 'w', encoding='utf-8')
        setting_data = {"volume_point_sound": volume_point_sound, 'volume_mixer_music': volume_mixer_music,
                        "volume_final_sound": volume_final_sound, "volume_endgame_sound": volume_endgame_sound,
                        'volume_leading_sound': volume_leading_sound,
                        'volume_congratulation_sound': volume_congratulation_sound, 'general_sound': general_sound}
    finally:
        file.close()

    for setting in setting_data:
        if setting_data[setting] != kwargs[setting]:
            setting_data[setting] = kwargs[setting]

    with open('setting_save.txt', 'w', encoding='utf-8') as file:
        for setting in setting_data:
            file.write(f'{setting} {setting_data[setting]}\n')


def score_result(nick_name, score):
    try:
        file = open('score_data.txt', 'r', encoding='utf-8')
        data_file = file.readlines()
        data_file = list(map(lambda x: x.strip().split(), data_file))
        data = {i[0]: int(i[1]) for i in data_file}
    except:
        file = open('score_data.txt', 'w', encoding='utf-8')
        data = {}
    finally:
        file.close()

    if nick_name in data:
        if score > data[nick_name]:
            data[nick_name] = score
    else:
        data[nick_name] = data.setdefault(nick_name, score)

    file = open('score_data.txt', 'w', encoding='utf-8')
    data2 = sorted(data, key=lambda x: data[x], reverse=True)
    for k in data2:
        file.write(f'{k}  {data[k]}\n')
    file.close()


def choose_level_menu():
    button_easy = Button('Easy', WIDTH // 2, 150)
    button_medium = Button('Medium', WIDTH // 2, 275)
    button_hard = Button('Харків 2022', WIDTH // 2, 400)
    button_immortal = Button('Маріуполь    ', WIDTH // 2, 525)
    button_back = Button('Back', WIDTH // 2, 650)
    sprite_screen = pygame.sprite.Group()
    sprite_screen.add(button_back)
    sprite_screen.add(button_hard)
    sprite_screen.add(button_medium)
    sprite_screen.add(button_easy)
    sprite_screen.add(button_immortal)
    sprite_screen.add(dot)
    waiting = True
    while waiting:
        clock.tick(FPS)
        sprite_screen.update()
        screen.blit(background, background_rect)
        sprite_screen.draw(screen)

        button_immortal.image.blit(img_emoji, (220, 30))
        draw_text(screen, "2TO10", 60, WIDTH // 2, 30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                return False
        if button_back.click:
            button_back.click = False
            return False
        if button_easy.click:
            nick_name = NickName(play()).name
            NickName.name = nick_name
            if nick_name:
                Comet.level = 'easy'
                all_sprites.add(c)
                comets.add(c)
                return True
            else:
                button_easy.click = False
        if button_medium.click:
            nick_name = NickName(play()).name
            NickName.name = nick_name
            if nick_name:
                Comet.level = 'medium'
                all_sprites.add(c)
                comets.add(c)
                return True
            else:
                button_medium.click = False
        if button_hard.click:
            nick_name = NickName(play()).name
            NickName.name = nick_name
            if nick_name:
                Comet.level = 'hard'
                all_sprites.add(c)
                all_sprites.add(c1)
                comets.add(c)
                comets.add(c1)
                return True
            else:
                button_hard.click = False
        if button_immortal.click:
            nick_name = NickName(play()).name
            NickName.name = nick_name
            if nick_name:
                Comet.level = 'immortal'
                all_sprites.add(c)
                all_sprites.add(c1)
                comets.add(c)
                comets.add(c1)
                return True
            else:
                button_immortal.click = False
        pygame.display.flip()


def play():
    input_box = pygame.Rect(WIDTH // 2 - 100, 300, 200, 64)
    input_box_s = pygame.Surface((200, 64))
    input_box_s.fill(BLACK)
    button_back = Button('Back', WIDTH // 2, 600)
    sprite_screen_play = pygame.sprite.Group()
    sprite_screen_play.add(button_back)
    sprite_screen_play.add(dot)
    font = pygame.font.Font(None, 64)
    text = ''
    waiting_p = True
    while waiting_p:
        clock.tick(FPS)
        sprite_screen_play.update()
        screen.blit(background, background_rect)
        sprite_screen_play.draw(screen)
        draw_text(screen, "Type your nickname", 60, WIDTH // 2, 80)
        draw_text(screen, "and enter", 60, WIDTH // 2, 140)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_p = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        if button_back.click:
            button_back.click = False
            waiting_p = False
            return False
        # Render the current text.
        txt_surface = font.render(text, True, WHITE)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(input_box_s, (WIDTH // 2 - 100, 300))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, WHITE, input_box, 2)
        pygame.display.flip()


def hit(fall=True):
    # running = False
    if sound:
        sound.stop()
    pygame.mixer.music.stop()
    if fall:
        end_sound = random.choice(endgame)
    else:
        end_sound = random.choice(congratulation)
    end_sound.play()
    pygame.time.delay(int(end_sound.get_length() * 1000) + 500)
    pygame.mixer.music.play(loops=-1)
    # Stick.side = 0; Stick.score = 0; Stick.speed = SPEEDX
    score_result(NickName.name, Comet.score)
    Comet.score = 0
    Comet.add = 2
    if circle in all_sprites:
        all_sprites.remove(circle)
    all_sprites.empty()
    all_sprites.add(dot)
    # reset
    return start_menu()


def reset_sprites(circle=False):
    for i in comets:
        i.side = 0
        i.speed = SPEEDX
        i.image_comet = img_comet_1
        i.group_image = img_comet
        i.coor = i.cycle[i.side]
        i.image = i.image_comet
        i.image.set_colorkey(BLACK)
        i.image = pygame.transform.rotate(img_comet_1, i.coor[4])
        i.rect = i.image.get_rect()
        i.direction = i.coor[2]
        i.memory_speed = SPEEDX
        i.random_size = 1
        i.radius = WIDE * 2
        i.rect.center = (i.coor[0], i.coor[1])
    comets.empty()
    if circle:
        circle.complete = False
        circle.scale = 1.0
        circle.angle = 1.0
        circle.image = final_circle_1
        circle.image.set_colorkey(BLACK)
        circle.rect = circle.image.get_rect()
        circle.radius = circle.rect.width / 2 - 60

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


cycle = ((0, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 'x', (WIDE, LENGTH), 90, LENGTH, WIDE*2+5),
         (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 0, 'y', (LENGTH, WIDE), 0, WIDE * 2 + 5, LENGTH),
         (WIDTH, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), '-x', (WIDE, LENGTH), -90, WIDE + 10, WIDE * 2 + 5),
         (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), HEIGHT, '-y', (LENGTH, WIDE), -180, WIDE * 2 + 5, WIDE + 10))


cycle_hard = ((0, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 'x', (WIDE, LENGTH), 90, LENGTH, WIDE // 2),
              (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), 0, 'y', (LENGTH, WIDE), 0, WIDE, LENGTH // 2),
              (WIDTH, random.randint(LENGTH // 2, WIDTH - LENGTH + 1), '-x', (WIDE, LENGTH), -90, -LENGTH, WIDE // 2),
              (random.randint(LENGTH // 2, WIDTH - LENGTH + 1), HEIGHT, '-y', (LENGTH, WIDE), -180, -WIDE, LENGTH // 2),
              (0, random.randint(0, WIDTH // 4), 'xy', (WIDE, LENGTH), 45),  # lu
              (random.randint(0, WIDTH // 4), 0, 'xy', (WIDE, LENGTH), 45),  # lu
              (0, random.randint(WIDTH // 4 * 3, WIDTH + 1), 'x-y', (WIDE, LENGTH), 135),  # ld
              (random.randint(0, WIDTH // 4), HEIGHT, 'x-y', (WIDE, LENGTH), 135),  # ld
              (random.randint(WIDTH // 4 * 3, WIDTH + 1), 0, '-xy', (WIDE, LENGTH), -45),  # ru
              (WIDTH, random.randint(0, WIDTH // 4), '-xy', (WIDE, LENGTH), -45),  # ru
              (WIDTH, random.randint(WIDTH // 4 * 3, WIDTH + 1), '-x-y', (WIDE, LENGTH), 225),  # rd
              (random.randint(WIDTH // 4 * 3, WIDTH + 1), HEIGHT, '-x-y', (WIDE, LENGTH), 225))  # rd

pygame.init()  # command of turning on pygame

if os.path.exists('setting_save.txt'):
    file = open('setting_save.txt', 'r', encoding='utf-8')
    setting_file = file.readlines()
    setting_file = list(map(lambda x: x.strip().split(), setting_file))
    setting_data = {i[0]: float(i[1]) for i in setting_file}
    file.close()
    volume_point_sound = setting_data['volume_point_sound']
    volume_mixer_music = setting_data['volume_mixer_music']
    volume_final_sound = setting_data['volume_final_sound']
    volume_endgame_sound = setting_data['volume_endgame_sound']
    volume_leading_sound = setting_data['volume_leading_sound']
    volume_congratulation_sound = setting_data['volume_congratulation_sound']
    general_sound = setting_data['general_sound']
else:
    volume_mixer_music = 0.1
    volume_point_sound = 0.8
    volume_endgame_sound = 0.5
    volume_leading_sound = 0.5
    volume_final_sound = 0.5
    volume_congratulation_sound = 0.5
    general_sound = 1.0
# sound
pygame.mixer.init()  # for sound
snd_dir = path.join(path.dirname(__file__), 'snd')
point_sound = pygame.mixer.Sound(path.join(snd_dir, 'sd_0.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'Cheers For Starlight Loop.mp3'))
pygame.mixer.music.set_volume(volume_mixer_music)
point_sound.set_volume(volume_point_sound)
snd_endgame_dir = path.join(path.dirname(__file__), 'snd/endgame')
endgame_sound = pygame.mixer.Sound(path.join(snd_endgame_dir, 'oh-no_7.mp3'))
endgame2_sound = pygame.mixer.Sound(path.join(snd_endgame_dir, '-jojo-nigerundayo.mp3'))
endgame3_sound = pygame.mixer.Sound(path.join(snd_endgame_dir, 'arrivederci.mp3'))
endgame4_sound = pygame.mixer.Sound(path.join(snd_endgame_dir, 'dio-wryyy.mp3'))
endgame5_sound = pygame.mixer.Sound(path.join(snd_endgame_dir, 'kira-laughter.mp3'))
endgame6_sound = pygame.mixer.Sound(path.join(snd_endgame_dir, 'oh-my-god-jojo.mp3'))
endgame7_sound = pygame.mixer.Sound(path.join(snd_endgame_dir, 'oh-no-oh-my-god-mp3cut.mp3'))
endgame8_sound = pygame.mixer.Sound(path.join(snd_endgame_dir, 'shizaaaaaa_w7zSfcu.mp3'))
endgame = (endgame_sound, endgame2_sound, endgame3_sound, endgame4_sound,
           endgame5_sound, endgame6_sound, endgame7_sound, endgame8_sound)

snd_leading_dir = path.join(path.dirname(__file__), 'snd/Leading')
leading_sound_1 = pygame.mixer.Sound(path.join(snd_leading_dir, 'jojos-bizarre-adventure-giorno-giovannas-7-page-muda.mp3'))
leading_sound_2 = pygame.mixer.Sound(path.join(snd_leading_dir, 'muda_muda_muda_sound_effect.mp3'))
leading_sound_3 = pygame.mixer.Sound(path.join(snd_leading_dir, 'muda_requiem.mp3'))
leading_sound_4 = pygame.mixer.Sound(path.join(snd_leading_dir, 'oraoraoraoraora-sound-effect.mp3'))
leading_sound_5 = pygame.mixer.Sound(path.join(snd_leading_dir, 'ringtone-jojo-jotaro-ora-ora-ora_-mp3cut.mp3'))
leading_sound_6 = pygame.mixer.Sound(path.join(snd_leading_dir, 'the-world-vs-star-platinum-muda-muda-muda-vs-ora-ora-ora_1.mp3'))
leading = (leading_sound_1, leading_sound_2, leading_sound_3, leading_sound_4, leading_sound_5, leading_sound_6)

snd_final_dir = path.join(path.dirname(__file__), 'snd/Final')
final_sound_1 = pygame.mixer.Sound(path.join(snd_final_dir, 'dio-za-warudo-time-stop-sound-effect_gBOeeUk.mp3'))
final_sound_2 = pygame.mixer.Sound(path.join(snd_final_dir, 'do-you-understand.mp3'))
final_sound_3 = pygame.mixer.Sound(path.join(snd_final_dir, 'za-warudo-mp3cut.mp3'))
final_sound_4 = pygame.mixer.Sound(path.join(snd_final_dir, 'za-warudo-stop-time-sound.mp3'))
final_sound_5 = pygame.mixer.Sound(path.join(snd_final_dir, 'za-warudo-the-world-time-resume.mp3'))
final = (final_sound_1, final_sound_2, final_sound_3, final_sound_4, final_sound_5)

snd_congratulation_dir = path.join(path.dirname(__file__), 'snd/congratulation')
congratulation_sound_1 = pygame.mixer.Sound(path.join(snd_congratulation_dir, 'jojos-golden-wind.mp3'))
congratulation_sound_2 = pygame.mixer.Sound(path.join(snd_congratulation_dir, 'joseph-joestar-nice.mp3'))
congratulation_sound_3 = pygame.mixer.Sound(path.join(snd_congratulation_dir, 'new-jjbatas-pb-intro.mp3'))
congratulation_sound_4 = pygame.mixer.Sound(path.join(snd_congratulation_dir, 'rero-rero-rero.mp3'))
congratulation_sound_5 = pygame.mixer.Sound(path.join(snd_congratulation_dir, 'yoshikage-kira-theme-ringtone.mp3'))
congratulation = (congratulation_sound_1, congratulation_sound_2, congratulation_sound_3, congratulation_sound_4, congratulation_sound_5)
# sound of win
all_volume = (volume_point_sound, volume_mixer_music, volume_final_sound, volume_endgame_sound,
                  volume_leading_sound, volume_congratulation_sound, general_sound)
# image
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load(path.join(img_dir, 'animesky3.jpeg')).convert()
background_rect = background.get_rect()
img_emoji = pygame.image.load(path.join(img_dir, 'loudly-crying-face_1f62d.png')).convert()
img_emoji = pygame.transform.scale(img_emoji, (40, 40))
img_emoji.set_colorkey(BLACK)

dot_img = pygame.image.load(path.join(img_dir, "ufoYellow.png")).convert()
img_comet_1 = pygame.image.load(path.join(img_dir, "comet_1_1.png")).convert()
img_comet_2 = pygame.image.load(path.join(img_dir, "comet_1_2.png")).convert()
img_comet_3 = pygame.image.load(path.join(img_dir, "comet_1_3.png")).convert()
img_comet_4 = pygame.image.load(path.join(img_dir, "comet_1_4.png")).convert()
img_comet_1 = pygame.transform.scale(img_comet_1, (70, 140))
img_comet_2 = pygame.transform.scale(img_comet_2, (70, 140))
img_comet_3 = pygame.transform.scale(img_comet_3, (70, 140))
img_comet_4 = pygame.transform.scale(img_comet_4, (70, 140))
img_comet = (img_comet_1, img_comet_2, img_comet_3, img_comet_4)
img_comet_05_1 = pygame.image.load(path.join(img_dir, "comet_0.5_1.png")).convert()
img_comet_05_2 = pygame.image.load(path.join(img_dir, "comet_0.5_2.png")).convert()
img_comet_05_3 = pygame.image.load(path.join(img_dir, "comet_0.5_3.png")).convert()
img_comet_05_4 = pygame.image.load(path.join(img_dir, "comet_0.5_4.png")).convert()
img_comet_05_1 = pygame.transform.scale(img_comet_05_1, (25, 90))
img_comet_05_2 = pygame.transform.scale(img_comet_05_2, (25, 90))
img_comet_05_3 = pygame.transform.scale(img_comet_05_3, (25, 90))
img_comet_05_4 = pygame.transform.scale(img_comet_05_4, (25, 90))
img_comet_05 = (img_comet_05_1, img_comet_05_2, img_comet_05_3, img_comet_05_4)
img_comet_075_1 = pygame.image.load(path.join(img_dir, "comet_0.75_1.png")).convert()
img_comet_075_2 = pygame.image.load(path.join(img_dir, "comet_0.75_2.png")).convert()
img_comet_075_3 = pygame.image.load(path.join(img_dir, "comet_0.75_3.png")).convert()
img_comet_075_4 = pygame.image.load(path.join(img_dir, "comet_0.75_4.png")).convert()
img_comet_075_1 = pygame.transform.scale(img_comet_075_1, (33, 110))
img_comet_075_2 = pygame.transform.scale(img_comet_075_2, (33, 110))
img_comet_075_3 = pygame.transform.scale(img_comet_075_3, (33, 110))
img_comet_075_4 = pygame.transform.scale(img_comet_075_4, (33, 110))
img_comet_075 = (img_comet_075_1, img_comet_075_2, img_comet_075_3, img_comet_075_4)
img_comet_125_1 = pygame.image.load(path.join(img_dir, "comet_1.25_1.png")).convert()
img_comet_125_2 = pygame.image.load(path.join(img_dir, "comet_1.25_2.png")).convert()
img_comet_125_3 = pygame.image.load(path.join(img_dir, "comet_1.25_3.png")).convert()
img_comet_125_4 = pygame.image.load(path.join(img_dir, "comet_1.25_4.png")).convert()
img_comet_125_1 = pygame.transform.scale(img_comet_125_1, (90, 200))
img_comet_125_2 = pygame.transform.scale(img_comet_125_2, (90, 200))
img_comet_125_3 = pygame.transform.scale(img_comet_125_3, (90, 200))
img_comet_125_4 = pygame.transform.scale(img_comet_125_4, (90, 200))
img_comet_125 = (img_comet_125_1, img_comet_125_2, img_comet_125_3, img_comet_125_4)
img_comet_15_1 = pygame.image.load(path.join(img_dir, "comet_1.5_1.png")).convert()
img_comet_15_2 = pygame.image.load(path.join(img_dir, "comet_1.5_2.png")).convert()
img_comet_15_3 = pygame.image.load(path.join(img_dir, "comet_1.5_3.png")).convert()
img_comet_15_4 = pygame.image.load(path.join(img_dir, "comet_1.5_4.png")).convert()
img_comet_15_1 = pygame.transform.scale(img_comet_15_1, (140, 140))
img_comet_15_2 = pygame.transform.scale(img_comet_15_2, (140, 140))
img_comet_15_3 = pygame.transform.scale(img_comet_15_3, (140, 140))
img_comet_15_4 = pygame.transform.scale(img_comet_15_4, (140, 140))
img_comet_15 = (img_comet_15_1, img_comet_15_2, img_comet_15_3, img_comet_15_4)
group_img_comets = {0.5: (img_comet_05, 7, 10), 0.75: (img_comet_075, WIDE, 15),
                    1: (img_comet, WIDE * 2 - 5, 20), 1.25: (img_comet_125, WIDE * 3 + 5, 30),
                    1.5: (img_comet_15, WIDE * 6 + 5, 40)}

def stick_img_cycle(i):
    i += 1
    if i == 4:
        i = 0
    return i


final_circle_1 = pygame.image.load(path.join(img_dir, "circle_final_1.png")).convert()
final_circle_2 = pygame.image.load(path.join(img_dir, "circle_final_2.png")).convert()
final_circle_3 = pygame.image.load(path.join(img_dir, "circle_final_3.png")).convert()
final_circle = (final_circle_2, final_circle_1, final_circle_3)
pygame.display.set_caption("2TO10")
clock = pygame.time.Clock()  # game work in define fps

all_sprites = pygame.sprite.Group()
comets = pygame.sprite.Group()
dot = DotMouse()
all_sprites.add(dot)

font_name = pygame.font.match_font('arial')

c = Comet(SPEEDX, cycle_hard)
c1 = Comet(SPEEDX, cycle_hard)
c2 = Comet(SPEEDX, cycle_hard)
c3 = Comet(SPEEDX, cycle_hard)
c4 = Comet(SPEEDX, cycle_hard)
circle = FinalCircle()
pygame.mouse.set_visible(False)
pygame.mixer.music.play(loops=-1)
running = start_menu()
sound = False
lead = True
final_bool = True
while running:

    clock.tick(FPS)
    all_sprites.update()
    if Comet.level == 'easy':
        if c.speed == 20 and lead:
            sound = random.choice(leading)
            sound.play()
            lead = False
            time_1 = 0
            random_final_score = random.randint(40000, 70000)
        if not lead and Comet.score > random_final_score and circle not in all_sprites:
            if time_1 == 0:
                sound_f = random.choice(final)
                time_1 = pygame.time.get_ticks()
                sound_f.play()
            if pygame.time.get_ticks() - time_1 > int(sound_f.get_length()*1000) - 1500 and final_bool:
                reset_sprites(comets)
                all_sprites.add(circle)
                final_bool = False
                FPS += d_speed[Comet.level] * 3
    elif Comet.level == 'medium':
        if Comet.score > 20000 and lead:
            all_sprites.add(c1)
            comets.add(c1)
            sound = random.choice(leading)
            sound.play()
            lead = False
            time_1 = 0
            random_final_score = random.randint(180000, 250000)
        if not lead and Comet.score > random_final_score and circle not in all_sprites:
            if time_1 == 0:
                sound_f = random.choice(final)
                time_1 = pygame.time.get_ticks()
                sound_f.play()
            if pygame.time.get_ticks() - time_1 > int(sound_f.get_length()*1000) - 1500 and final_bool:
                reset_sprites()
                all_sprites.add(circle)
                final_bool = False
                FPS += d_speed[Comet.level] * 5
    elif Comet.level == 'hard':
        if Comet.score > 100000 and c2 not in comets:
            all_sprites.add(c2)
            comets.add(c2)
            sound = random.choice(leading)
            sound.play()
        if Comet.score > 800000 and c3 not in comets:
            all_sprites.add(c3)
            comets.add(c3)
            sound = random.choice(leading)
            sound.play()
            time_1 = 0
            random_final_score = random.randint(1100000, 1500000)
        if c3 in comets and Comet.score > random_final_score and circle not in all_sprites:
            if time_1 == 0:
                sound_f = random.choice(final)
                time_1 = pygame.time.get_ticks()
                sound_f.play()
            if pygame.time.get_ticks() - time_1 > int(sound_f.get_length()*1000) - 1500 and final_bool:
                reset_sprites()
                all_sprites.add(circle)
                final_bool = False
                FPS += d_speed[Comet.level] * 5
    elif Comet.level == 'immortal':
        if Comet.score > 200000 and c2 not in comets:
            all_sprites.add(c2)
            comets.add(c2)
            c2.memory_speed = c.memory_speed
            sound = random.choice(leading)
            sound.play()
        if Comet.score > 1000000 and c3 not in comets:
            all_sprites.add(c3)
            comets.add(c3)
            c3.memory_speed = c.memory_speed
            sound = random.choice(leading)
            sound.play()
        if Comet.score > 3000000 and c4 not in comets:
            all_sprites.add(c4)
            comets.add(c4)
            c4.memory_speed = c.memory_speed
            sound = random.choice(leading)
            sound.play()
            time_1 = 0
            random_final_score = random.randint(5000000, 10000000)
        if c4 in comets and Comet.score > random_final_score and circle not in all_sprites:
            if time_1 == 0:
                sound_f = random.choice(final)
                time_1 = pygame.time.get_ticks()
                sound_f.play()
            if pygame.time.get_ticks() - time_1 > int(sound_f.get_length()*1000) - 1500 and final_bool:
                reset_sprites()
                all_sprites.add(circle)
                final_bool = False
                FPS += d_speed[Comet.level] * 6
    if c in comets:
        for _ in range(c.memory_speed // 3 * 2):
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
            hits = pygame.sprite.spritecollide(dot, comets, False, pygame.sprite.collide_circle)
            if hits:
                lead = True
                draw_text(screen, 'LOL', 60, WIDTH // 2, HEIGHT // 2 - 200)
                draw_text(screen, 'nu i loh', 60, WIDTH // 2, HEIGHT // 2 - 140)
                pygame.display.flip()
                reset_sprites(comets)
                running = hit()
    else:
        all_sprites.update()
        print(circle.radius)
        print(circle.scale)
        dot.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        hits = pygame.sprite.collide_circle(circle, dot)
        hits_2 = pygame.sprite.spritecollide(dot, comets, False, pygame.sprite.collide_circle)
        if not hits or hits_2:
            if sound_f:
                sound_f.stop()
            draw_text(screen, 'LOL', 60, WIDTH // 2, HEIGHT // 2 - 200)
            draw_text(screen, 'nu i loh', 60, WIDTH // 2, HEIGHT // 2 - 140)
            reset_sprites(circle)
            FPS = 60
            lead = True
            final_bool = True
            running = hit()
        else:
            if circle.complete:
                draw_text(screen, "!CONGRATULATION!", 60, WIDTH // 2, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(1000)
                FPS = 60
                lead = True
                final_bool = True
                circle.complete = False
                reset_sprites(circle)
                running = hit(fall=False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # check for closing window
            running = False

    # screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(c.score), 20, 100, 20)

    pygame.display.flip()
    # end

pygame.quit()
