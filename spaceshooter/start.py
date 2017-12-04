

from __future__ import division
import pygame
import random
from os import path
import platform
import inputbox

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
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')
text_dir = path.join(path.dirname(__file__), 'text')

#Code added by doo
root = Tk() ##tk 윈도우 생성
root.withdraw() ##아마도 이게 윈도우 가리게 해주는 함수같음

#Code added by Jiwoo
make_dialog = path.join(path.dirname(__file__), 'make_dialog')
music_flag = 0 #To distinguish between default playing and user_setting playing
dual_play_flag = 1 #To distinguish between default playing and user_setting playing
life_count = 1 #To make lifeup item
death_count = 1 #To make lifedown item
death_count2 = 1 #To make lifedown item one more

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

font_name = pygame.font.match_font('arial')

# Code added by Jiwoo
# To Show Operation Guide

def operation_guide():
    global screen

    title = pygame.image.load(path.join(img_dir, "operation_guide.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)

    screen.blit(title, (0,0))
    pygame.display.update()
    
    while True:
        #When the user pulls off his hand from TAB-key
        #go back to the menu screen
        ev = pygame.event.poll()
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_TAB:
                title = pygame.image.load(path.join(img_dir, "main.png")).convert()
                title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
                screen.blit(title, (0, 0))

                draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH / 2, HEIGHT / 2)
                draw_text(screen, "or [Q] To Quit", 30, WIDTH / 2, (HEIGHT / 2) + 40)
                draw_text(screen, "Press [TAB] To See Operation Guide", 25, WIDTH / 2, (HEIGHT - 40))
                pygame.display.update()
                break


def main_menu():
    global screen

    # Code added by Jiwoo
    global music_flag #To use global variable, music_flag
    global dual_play_flag #To use global variable, dual_play_flag

    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg"))
    pygame.mixer.music.play(-1)

    title = pygame.image.load(path.join(img_dir, "main.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)

    screen.blit(title, (0,0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                subprocess.call(['python3', path.join(make_dialog, 'game_setting.py')])
                break
            elif ev.key == pygame.K_q:
                #Code added by doo
                if messagebox.askokcancel("GAME EXIT", "정말로 종료하시겠습니까?") == TRUE:
                    pygame.quit()
                    quit()
                else:
                    continue
                quit()

            #when the user press the TAB-key on keyboard, he can see the operation guide
            elif ev.key == pygame.K_TAB:
                operation_guide()

        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "or [Q] To Quit", 30, WIDTH/2, (HEIGHT/2)+40)

            # Code added by Jiwoo
            #Add Text in main_menu to give users additional option
            draw_text(screen, "Press [TAB] To See Operation Guide", 25, WIDTH / 2, (HEIGHT - 40))

            pygame.display.update()

    #pygame.mixer.music.stop()
    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    ready.play()
    screen.fill(BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH/2, HEIGHT/2)
    pygame.display.update()

# Code added by Jiwoo

def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


main_menu()
pygame.mixer.music.stop()
subprocess.call(['python3', path.join(path.dirname(__file__), 'spaceShooter.py')])

pygame.quit()
