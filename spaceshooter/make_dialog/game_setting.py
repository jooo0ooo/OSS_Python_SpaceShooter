

from __future__ import division
import pygame
import random
from os import path
import platform

#Code added by doo
from tkinter import *
from tkinter import messagebox

#Code added by Jiwoo
#for using bash
#we should 'import subprocess' for using subprocess Module

import subprocess

import os
import sys
import sqlite3

## assets folder
img_dir = path.join(path.join(path.dirname(__file__), ".."), 'assets')
make_dialog = path.join(path.dirname(__file__), 'make_dialog')
text_dir = path.join(path.abspath(path.join(path.dirname(__file__),"..")), 'text')


###############################
## to be placed in "constant.py" later
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
###############################

###############################
## to placed in "__init__.py" later
## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()     ## For syncing the FPS
###############################
class p1_setting(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "p1_img.png")), (20, 15))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = 60
        self.rect.bottom = 260
        self.speedx = 0


    def update(self):
        ## unhide
        self.speedx = 0  ## makes the player static in the screen by default.


        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -58
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 58

        ## check for the borders at the left and right
        if self.rect.right > 430:
            self.rect.right = 430
        if self.rect.left <= 60:
            self.rect.left = 60

        self.rect.x += self.speedx
        pygame.time.delay(80)

class p2_setting(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "p2_img.png")), (20, 15))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = 60
        self.rect.bottom = 290
        self.speedx = 0


    def update(self):
        ## unhide
        self.speedx = 0  ## makes the player static in the screen by default.


        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_f]:
            self.speedx = -58
        elif keystate[pygame.K_h]:
            self.speedx = 58

        ## check for the borders at the left and right
        if self.rect.right > 430:
            self.rect.right = 430
        if self.rect.left <= 60:
            self.rect.left = 60

        self.rect.x += self.speedx
        pygame.time.delay(80)


setting_sprites = pygame.sprite.Group()
p1_setting = p1_setting()
p2_setting = p2_setting()
setting_sprites.add(p1_setting)


background = pygame.image.load(path.join(img_dir, 'setting_img.png')).convert()
#background = pygame.transform.scale(background, (WIDTH, HEIGHT), screen)
####
background_rect = background.get_rect()



pygame.mixer.music.set_volume(3)
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def save_data(level, player1_color, player2_color):
    Setting_text_file = open(path.join(text_dir, 'game_setting.txt'),"w",encoding="utf-8")
    Selected_level = level
    Player1_Selected_Color = player1_color
    Player2_Selected_Color = player2_color
    temp = "Selected_Level="+Selected_level+" P1_Selected_Color="+Player1_Selected_Color+" P2_Selected_Color="+Player2_Selected_Color
    Setting_text_file.write(temp)
    Setting_text_file.close()

#############################
## Game loop
running = True
level = "Level1"
player1_color = ""
player2_color = ""

while running:
    setting_sprites.update()
    ev = pygame.event.poll()
    if ev.type == pygame.KEYDOWN:
        if ev.key == pygame.K_RETURN:
            if p1_setting.rect.centerx == 70 or p1_setting.rect.centerx == 72 :
                player1_color = "playerShip1_yellow.png"
            elif p1_setting.rect.centerx == 128 or p1_setting.rect.centerx == 130:
                player1_color = ("playerShip1_red.png")
            elif p1_setting.rect.centerx == 186 or p1_setting.rect.centerx == 188:
                player1_color = ("playerShip1_purple.png")
            elif p1_setting.rect.centerx == 244 or p1_setting.rect.centerx == 246:
                player1_color = ("playerShip1_pink.png")
            elif p1_setting.rect.centerx == 302 or p1_setting.rect.centerx == 304:
                player1_color = ("playerShip1_orange.png")
            elif p1_setting.rect.centerx == 360 or p1_setting.rect.centerx == 362:
                player1_color = ("playerShip1_gold.png")
            elif p1_setting.rect.centerx == 418 or p1_setting.rect.centerx == 420:
                player1_color = ("playerShip1_blue.png")

            if p2_setting.rect.centerx == 70 or p2_setting.rect.centerx == 72 :
                player2_color = "playerShip1_yellow.png"
            elif p2_setting.rect.centerx == 128 or p2_setting.rect.centerx == 130:
                player2_color = ("playerShip1_red.png")
            elif p2_setting.rect.centerx == 186 or p2_setting.rect.centerx == 188:
                player2_color = ("playerShip1_purple.png")
            elif p2_setting.rect.centerx == 244 or p2_setting.rect.centerx == 246:
                player2_color = ("playerShip1_pink.png")
            elif p2_setting.rect.centerx == 302 or p2_setting.rect.centerx == 304:
                player2_color = ("playerShip1_orange.png")
            elif p2_setting.rect.centerx == 360 or p2_setting.rect.centerx == 362:
                player2_color = ("playerShip1_gold.png")
            elif p2_setting.rect.centerx == 418 or p2_setting.rect.centerx == 420:
                player2_color = ("playerShip1_blue.png")

            save_data(level, player1_color, player2_color)
            break

        elif ev.key == pygame.K_1:
            level = "Level1"
        elif ev.key == pygame.K_2:
            level = "Level2"
        elif ev.key == pygame.K_3:
            level = "Level3"
        elif ev.key == pygame.K_4:
            level = "Level4"
        elif ev.key == pygame.K_5:
            level = "Level5"

        elif ev.key == pygame.K_f:
            setting_sprites.add(p2_setting)
        elif ev.key == pygame.K_m:
            subprocess.call(['python3', path.join(path.dirname(__file__), 'select_my_music.py')])


    screen.fill(BLACK)
    screen.blit(background, background_rect)
    setting_sprites.draw(screen)
    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time

    draw_text(screen, "Press 1~5 To Choose Level", 30, 140, 15)
    draw_text(screen, "Level -> ", 30, 50, 50)
    draw_text(screen, "Press Enter To Begin", 30, WIDTH / 2, (HEIGHT / 2) + 50)
    draw_text(screen, "Press F To Play With A Friend", 30, WIDTH / 2, (HEIGHT / 2) + 80)
    draw_text(screen, "Press M To Play With Ur Music", 30, WIDTH / 2, (HEIGHT / 2) + 110)
    if level == "Level1":
        draw_text(screen, "1", 30, 95, 50)
    if level == "Level2":
        draw_text(screen, "2", 30, 95, 50)
    if level == "Level3":
        draw_text(screen, "3", 30, 95, 50)
    if level == "Level4":
        draw_text(screen, "4", 30, 95, 50)
    if level == "Level5":
        draw_text(screen, "5", 30, 95, 50)




    ## Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()

