from datetime import datetime
import os
import pygame
import sys
import cv2                      # требуется библиотека OpenCV

import math
DISPLAY = (1280, 720)
name = input("Пожалуйста, введите ФИО пациента (на английском): ")
IMAGES_DIR = f"./patients_data/{'_'.join(name.split())}/{datetime.now().strftime('%Y-%m-%d_%H-%M')}"
os.makedirs(IMAGES_DIR)
print(IMAGES_DIR)
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Здоровые глаза")
object_image = pygame.image.load("images/космический корабль.png")
bg = pygame.image.load("images/background.jpg")
bg2 = pygame.image.load("images/background2.jpg")
bg3 = pygame.image.load("images/background3.jpg")
bg_next = pygame.image.load("images/background_next.jpg")
bg_next2 = pygame.image.load("images/background_next2.jpg")
goodbye = pygame.image.load("images/goodbye.jpg")
level_bg = pygame.image.load("images/фон.jpg")
right = pygame.mixer.Sound('sounds/справа.ogg')
left = pygame.mixer.Sound('sounds/слева.ogg')
up = pygame.mixer.Sound('sounds/наверху.ogg')
down = pygame.mixer.Sound('sounds/внизу.ogg')
instruct = pygame.mixer.Sound('sounds/Инструкция.ogg')
instruct2 = pygame.mixer.Sound('sounds/Инструкция2.ogg')
one_two_three = pygame.mixer.Sound('sounds/Отсчет.ogg')

cam = cv2.VideoCapture(0)


class Ball:

    def __init__(self, level, x, y, img, sound,  xspeed=False, yspeed=False):
        self.x = x
        self.y = y
        self.levelnum = level
        if xspeed:
            self.x_speed = 50
        else:
            self.x_speed = 0
        if yspeed:
            self.y_speed = 50
        else:
            self.y_speed = 0
        self.image = img
        self.width = 215
        self.height = 105

        self.color = "white"
        self.num_of_collides = 0
        self.sound = sound

    def update(self, surface):
        self.x += int(self.x_speed / 10)
        self.y += int(self.y_speed / 10)
        self.collide()

        self.draw(surface)

    def collide(self):
        if self.x + self.width >= 1280 or self.x <= 0:
            self.num_of_collides += 1
            self.x_speed = -self.x_speed
            if self.sound:
                if self.x_speed < 0:
                    right.play()
                else:
                    left.play()
                pygame.time.wait(1000)
            self.image = pygame.transform.flip(self.image, True, False)
            retval, frame = cam.read()
            if retval != True:
                raise ValueError("Can't read frame")
            cv2.imwrite(f"{IMAGES_DIR}/img{self.levelnum}-{self.num_of_collides}.jpg", frame)

        if self.y + self.height >= 720 or self.y <= 0:
            self.num_of_collides += 1
            self.y_speed = -self.y_speed
            if self.sound:
                if self.y_speed < 0:
                    down.play()
                else:
                    up.play()
                pygame.time.wait(1000)
            retval, frame = cam.read()
            if retval != True:
                raise ValueError("Can't read frame")
            cv2.imwrite(f"{IMAGES_DIR}/img{self.levelnum}-{self.num_of_collides}.jpg", frame)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


def instruction(bg, time, camera=False):
    clock = pygame.time.get_ticks()
    done = True
    while done:
        screen.fill((0, 0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
        if camera:
            if pygame.time.get_ticks() - clock > 10000:
                    one_two_three.play()
                    pygame.time.wait(2000)
                    retval, frame = cam.read()
                    if retval != True:
                        raise ValueError("Can't read frame")
                    cv2.imwrite(f"{IMAGES_DIR}/img4_1.jpg", frame)
                    done = False
        else:
            if pygame.time.get_ticks() - clock > time * 1000:
                done = False

        screen.blit(bg, (0, 0))
        pygame.display.flip()


def level(level, x, y, bg, img, bg_nex, sound=True):
    object = Ball(level, 533, 308, img, sound, x, y)
    clock = pygame.time.get_ticks()
    running = True

    while running:

        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        object.update(screen)
        if pygame.time.get_ticks() - clock > 30000:
            screen.fill((0, 0, 0))
            screen.blit(bg_nex, (0, 0))
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False
        pygame.display.flip()



instruction(bg, 3)
instruct.play()
instruction(bg2, 7)

level(1, True, False, level_bg, object_image, bg_next)
level(2, False, True, level_bg, object_image, bg_next)
level(3, True, True, level_bg, object_image, bg_next2, False)

instruct2.play()
instruction(bg3, 10, True)
screen.blit(goodbye, (0, 0))
pygame.display.flip()
pygame.time.wait(3000)
sys.exit()