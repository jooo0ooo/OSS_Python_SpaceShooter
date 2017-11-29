#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Original Author: tasdik
# @Original Contributers : Branden (Github: @bardlean86)
# @Original Author's Email:  prodicus@outlook.com  Github: @tasdikrahman
# @Original OSS URL : https://github.com/tasdikrahman/spaceShooter
# MIT License. You can find a copy of the License @ http://prodicus.mit-license.org

# Modified by Jiwoo Jung
# Why would you change it?
# -> For studying python
# How would you change it?
# -> Add new functions
# You can see the changing process at https://github.com/pingrae/OSS_Python_SpaceShooter

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

#Code added by doo
root = Tk() ##tk 윈도우 생성
root.withdraw() ##아마도 이게 윈도우 가리게 해주는 함수같음

#Code added by Jiwoo
make_dialog = path.join(path.dirname(__file__), 'make_dialog')
music_flag = 0 #To distinguish between default playing and user_setting playing
dual_play_flag = 0 #To distinguish between default playing and user_setting playing
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
                draw_text(screen, "Press [T] To Play With Ur Music", 30, WIDTH / 2, (HEIGHT / 2) + 80)
                draw_text(screen, "Press [D] To Play With A Friend", 30, WIDTH / 2, (HEIGHT / 2) + 120)
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
                break
            elif ev.key == pygame.K_q:
                #Code added by doo
                if messagebox.askokcancel("GAME EXIT", "정말로 종료하시겠습니까?") == TRUE:
                    pygame.quit()
                    quit()
                else:
                    continue
                quit()

            # Code added by Jiwoo
            # When the user press the T-key on keyboard, go into the conditional statement
            elif ev.key == pygame.K_t:
                #Use subprocess Module to execute bash command in a python script
                if platform.system()=="Windows":
                    subprocess.call(['python', path.join(make_dialog, 'select_my_music.py')],shell=True)
                else:
                    subprocess.call(['python3', path.join(make_dialog, 'select_my_music.py')], shell=True)
                #change value of music_flag
                music_flag = 1
                break
            # When the user press the D-key on keyboard, go into the conditional statement
            elif ev.key == pygame.K_d:
                #change value of dual_play_flag
                dual_play_flag = 1
                break
            #when the user press the TAB-key on keyboard, he can see the operation guide
            elif ev.key == pygame.K_TAB:
                operation_guide()

        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "or [Q] To Quit", 30, WIDTH/2, (HEIGHT/2)+40)

            # Code added by Jiwoo
            #Add Text in main_menu to give users additional option
            draw_text(screen, "Press [T] To Play With Ur Music", 30, WIDTH/2, (HEIGHT/2)+80)
            draw_text(screen, "Press [D] To Play With A Friend", 30, WIDTH/2, (HEIGHT/2)+120)
            draw_text(screen, "Press [TAB] To See Operation Guide", 25, WIDTH / 2, (HEIGHT - 40))

            pygame.display.update()

    #pygame.mixer.music.stop()
    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    ready.play()
    screen.fill(BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH/2, HEIGHT/2)
    pygame.display.update()

# Code added by Jiwoo
def game_over():
    global screen
    global running

    i = 1
    s_player=[]
    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg"))
    pygame.mixer.music.play(-1)
    font = pygame.font.SysFont('Arial Black', 17)

    title = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
    player_name = inputbox.ask(screen, "Your name ")
    s_player = highscore.update(player_name,score,font)
    screen.blit(title, (0,0))
    pygame.display.update()


    title = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
    screen.blit(title, (0, 0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                highscore.cur.close()
                highscore.db.commit()
                highscore.db.close()
                print(sys.executable)
                print(sys.argv)
                print([sys.executable] + sys.argv)
                executable = sys.executable
                args = sys.argv[:]
                args.insert(0,sys.executable)
                os.execvp(sys.executable,sys.argv)
                #1os.execv(__file__,sys.argv)
                #os.execv(sys.executable, ['python'] + sys.argv)
                #os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
                #os.execl(sys.executable,sys.argv)
                #os.execv('C:\\Program Files\\Python36\\python.exe', sys.argv)
                break
            elif ev.key == pygame.K_ESCAPE:
                print("poll?",score)
                pygame.quit()
                highscore.cur.close()
                highscore.db.commit()
                highscore.db.close()
                quit()
        else:

            draw_text(screen, "GAME OVER", 80, WIDTH/2, HEIGHT/2 - 200)
            highscore.draw(s_player,font)
            draw_text(screen, "Press [ENTER] To Play Again", 30, WIDTH/2, HEIGHT-100)
            draw_text(screen, "or [ESC] To Quit", 30, WIDTH/2, HEIGHT-50)
            score_temp = player_name + " : " + str(score)
            draw_text(screen, score_temp, 30, WIDTH/2, (HEIGHT/2)+150)
            pygame.display.update()


def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    # if pct < 0:
    #     pct = 0
    pct = max(pct, 0) 
    ## moving them to top
    # BAR_LENGTH = 100
    # BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

# Code added by Jiwoo
def bonus(): #make bonus item
    bonus_element = Bonus()
    all_sprites.add(bonus_element)
    bonuses.add(bonus_element)

def newlife(): #make lifeup item
    life_element = Life()
    all_sprites.add(life_element)
    lifes.add(life_element)

def newdeath(): #make lifedown item
    death_element = Death()
    all_sprites.add(death_element)
    deaths.add(death_element)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
## dbconnection

class Highscore:
    # Init higscore
    def __init__(self, surface):

        # Creates a sqlite connection to test.db, will be created if non-exist
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()

        # Creates a table where name and score are stored
        try:
            cursor.execute('CREATE TABLE highscore (id INTEGER PRIMARY KEY, name VARCHAR(50), score INTEGER)')
            cursor.close()
        except sqlite3.Error as e:
            cursor.close()

        self.surface = surface
        self.db = connection
        self.cur = self.db.cursor()

        # Updates highscore and store in database

    def update(self, name, score, font):
        player = []
        i = 1

        self.cur.execute("SELECT COUNT(*) FROM highscore")  # Check number of rows in table
        result = self.cur.fetchall()
        print(result)
        nrecs = result[0][0]
        print(nrecs)
        if nrecs > 10:  # If 10 or more rows
            self.cur.execute(
                'SELECT * FROM highscore ORDER BY score DESC LIMIT 9,1')  # Compares the last row with the current score
            last = self.cur.fetchone()
            # print last
            if last[2] < score:
                try:
                    self.cur.execute('UPDATE highscore SET name=?, score=? WHE  RE id=?',
                                     (name, score, last[0]))  # Update the last row with new score and name
                except sqlite3.Error as e:
                    print("Ooops:11", e.args[0])
        else:  # Add a new row in table
            try:
                self.cur.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
            except sqlite3.Error as e:
                print("Ooops:222", e.args[0])

        try:
            self.cur.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 0,10')  # Choose the first 10 rows
        except sqlite3.Error as e:
            print("Ooops:33", e.args[0])
        font = pygame.font.SysFont("arial", 20)
        for row in self.cur:  # Loop though the rows and adds to a array
            player.append(
                font.render(str(i) + '. ' + str(row[1]) + "" * (8 - len(row[1])) +"    "+ str(row[2]), True, (255, 255, 255)))
            i += 1

        return player  # Return the array

    # Genereate and prints highscore.
    def draw(self, player, font):
        i = 20
        font2 = pygame.font.SysFont('Arial Black', 40)

        for row in player:  # Loops through player and blits every row with 20px between
            self.surface.blit(row, (self.surface.get_width() / 2 - 75, 180 + i))
            i += 20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

        # Code added by Jiwoo
        #winitializing for first speed of up_down
        self.speedy = 0
        
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        ## time out for powerups
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        ## unhide 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0     ## makes the player static in the screen by default. 

        # Code added by Jiwoo
        self.speedy = 0     ## makes the player static in the screen by default. 

        # then we have to check whether there is an event hanlding being done for the arrow keys being 
        ## pressed 

        ## will give back a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5

        # Code added by Jiwoo
        elif keystate[pygame.K_UP]: #when pressing UP Key
            self.speedy = -5
        elif keystate[pygame.K_DOWN]: #when pressing DOWN Key
            self.speedy = 5

        #Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            self.shoot()

        ## check for the borders at the left and right
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # Code added by Jiwoo
        #To prevent user_object(airplane) from leaving out of the screen
        if self.rect.bottom > HEIGHT - 30:
            self.rect.bottom = HEIGHT - 30
        if self.rect.top < 0:
            self.rect.top = 0

        self.rect.x += self.speedx

        # Code added by Jiwoo
        self.rect.y += self.speedy #Adjust the vertical position

    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()

            """ MOAR POWAH """
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top) # Missile shoots from center of ship
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# Code added by Jiwoo
# For dual playing, add another player object
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(player2_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 3 * 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        ## time out for powerups
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        ## unhide 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0     ## makes the player static in the screen by default.
        self.speedy = 0     ## makes the player static in the screen by default. 

        # then we have to check whether there is an event hanlding being done for the arrow keys being 
        ## pressed 

        ## will give back a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_f]:
            self.speedx = -5
        elif keystate[pygame.K_h]:
            self.speedx = 5
        elif keystate[pygame.K_t]:
            self.speedy = -5
        elif keystate[pygame.K_g]:
            self.speedy = 5

        #Fire weapons by holding spacebar
        if keystate[pygame.K_z]:
            self.shoot()

        ## check for the borders at the left and right
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT - 30:
            self.rect.bottom = HEIGHT - 30
        if self.rect.top < 0:
            self.rect.top = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy #Adjust the vertical position

    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()

            """ MOAR POWAH """
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top) # Missile shoots from center of ship
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

# Code added by Jiwoo
class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = item_puppy['puppy']
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            
        if score > 20000:
            self.kill()


class Life(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = item_images['life+']
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            
        if score > 5000:
            self.kill()

class Death(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = item_images['life-']
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# defines the enemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)        ## for randomizing the speed of the Mob

        ## randomize the movements a little more 
        self.speedx = random.randrange(-3, 3)

        ## adding rotation to the mob element
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen
        
    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        ## now what if the mob element goes out of the screen

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)        ## for randomizing the speed of the Mob

## defines the sprite for Powerups
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.center = center
        self.speedy = 2

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.top > HEIGHT:
            self.kill()

            

## defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.bottom < 0:
            self.kill()

        ## now we need a way to shoot
        ## lets bind it to "spacebar".
        ## adding an event for it in Game loop

## FIRE ZE MISSILES
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


###################################################
## Load all game images

background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
## ^^ draw this rect first 

player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

# Code added by Jiwoo
# Setting for another player
player2_img = pygame.image.load(path.join(img_dir, 'playerShip2_orange.png')).convert()
player_mini_img2 = pygame.transform.scale(player2_img, (25, 19))
player_mini_img2.set_colorkey(BLACK)

bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert_alpha()
# meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, image)).convert())

## meteor explosion
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

# Code added by Jiwoo
explosion_anim['player2'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    ## resize the explosion
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    ## player explosion
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

    # Code added by Jiwoo
    explosion_anim['player2'].append(img)

## load power ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

#Code added by jiwoo
item_images = {}
item_images['life+'] = pygame.image.load(path.join(img_dir, 'item_red.png')).convert_alpha()
item_images['life-'] = pygame.image.load(path.join(img_dir, 'item_yello.png')).convert_alpha()

item_puppy = {}
item_puppy['puppy'] = pygame.image.load(path.join(img_dir, 'item_bonus.png')).convert_alpha()

###################################################


###################################################
### Load all game sounds
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
## main background music
#pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))

#pygame.mixer.music.set_volume(0.2)      ## simmered the sound down a little
# Code added by Jiwoo
pygame.mixer.music.set_volume(3)

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))
###################################################

## group all the sprites together for ease of update
all_sprites = pygame.sprite.Group()
player = Player()

# Code added by Jiwoo
player2 = Player2()

all_sprites.add(player)

## spawn a group of mob
mobs = pygame.sprite.Group()
for i in range(8):      ## 8 mobs
    # mob_element = Mob()
    # all_sprites.add(mob_element)
    # mobs.add(mob_element)
    newmob()

# Code added by Jiwoo
lifes = pygame.sprite.Group()
deaths = pygame.sprite.Group()
bonuses = pygame.sprite.Group()

## group for bullets
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

#### Score board variable
score = 0

## TODO: make the game music loop over again and again. play(loops=-1) is not working
# Error : 
# TypeError: play() takes no keyword arguments
#pygame.mixer.music.play()

#############################
## Game loop
running = True
menu_display = True
while running:
    if menu_display:
        main_menu()
        highscore = Highscore(screen)
        pygame.time.wait(3000)

        #Stop menu music
        pygame.mixer.music.stop()
        #Play the gameplay music

        # Code added by Jiwoo
        if music_flag == 1:
            #Read the user's music path
            text_dir = path.join(path.dirname(__file__), 'text')
            f = open(path.join(text_dir, 'user_music_location.txt'), 'r')
            line = f.readline()
            my_song = line
            f.close()
            #play with user's music
            pygame.mixer.music.load(my_song)
            pygame.mixer.music.play(-1)  ## makes the gameplay sound in an endless loop

        #Setting for dual play mode
        elif dual_play_flag == 1:
            all_sprites.add(player2)
            player.rect.centerx = WIDTH / 3
            player.rect.bottom = HEIGHT
            pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
            pygame.mixer.music.play(-1)  ## makes the gameplay sound in an endless loop

        elif music_flag == 0:
            #default play
            pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
            pygame.mixer.music.play(-1)  ## makes the gameplay sound in an endless loop

        menu_display = False
        
    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        # ## event for shooting the bullets
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()      ## we have to define the shoot()  function

    #2 Update
    all_sprites.update()


    ## check if a bullet hit a mob
    ## now we have a group of bullets and a group of mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    ## now as we delete the mob element when we hit one with a bullet, we need to respawn them again
    ## as there will be no mob_elements left out 
    for hit in hits:
        score += 50 - hit.radius         ## give different scores for hitting big and small metoers
        random.choice(expl_sounds).play()
        # m = Mob()
        # all_sprites.add(m)
        # mobs.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()        ## spawn a new mob

    ## ^^ the above loop will create the amount of mob objects which were killed spawn again
    #########################

    ## check if the player collides with the mob
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)        ## gives back a list, True makes the mob element disappear
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0: 
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            # running = False     ## GAME OVER 3:D
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Code added by Jiwoo
    if score> 10000 :
        bonus()

    for i in (1, 10, 2):
        if score > 1000 * i and life_count == i:
            newlife()
            life_count += 1

    for i in range(1, 10, 2):
        if score > 500 * i and death_count == i:
            newdeath()
            death_count += 1

    for i in range(1, 10, 2):
        if score > 1000 * i and death_count2 == i:
            newdeath()
            newdeath()
            death_count2 += 1

    hit_bonus = pygame.sprite.spritecollide(player, bonuses, True, pygame.sprite.collide_circle)  ## gives back a list, True makes the mob element disappear
    for hit in hit_bonus:
        score += 100

    hit_life = pygame.sprite.spritecollide(player, lifes, True, pygame.sprite.collide_circle)  ## gives back a list, True makes the mob element disappear
    for hit in hit_life:
        newlife()
        if(player.lives < 5):
            player.lives += 1

    hit_death = pygame.sprite.spritecollide(player, deaths, True, pygame.sprite.collide_circle)  ## gives back a list, True makes the mob element disappear
    for hit in hit_death:
        newdeath()
        if(player.lives >1):
            player.lives -= 1

    hit_bonus = pygame.sprite.spritecollide(player2, bonuses, True, pygame.sprite.collide_circle)  ## gives back a list, True makes the mob element disappear
    for hit in hit_bonus:
        score += 100

    hit_life = pygame.sprite.spritecollide(player2, lifes, True, pygame.sprite.collide_circle)  ## gives back a list, True makes the mob element disappear
    for hit in hit_life:
        newlife()
        if(player.lives < 5):
            player.lives += 1

    hit_death = pygame.sprite.spritecollide(player2, deaths, True, pygame.sprite.collide_circle)  ## gives back a list, True makes the mob element disappear
    for hit in hit_death:
        newdeath()
        if(player.lives >1):
            player.lives -= 1
            
    # Code added by Jiwoo
    # Setting for another player
    hits = pygame.sprite.spritecollide(player2, mobs, True, pygame.sprite.collide_circle)  ## gives back a list, True makes the mob element disappear
    for hit in hits:
        player2.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player2.shield <= 0:
            player_die_sound.play()
            death_explosion2 = Explosion(player2.rect.center, 'player2')
            all_sprites.add(death_explosion2)
            # running = False     ## GAME OVER 3:D
            player2.hide()
            player2.lives -= 1
            player2.shield = 100

    ## if the player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    # Code added by Jiwoo
    # Setting for another player
    hits = pygame.sprite.spritecollide(player2, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player2.shield += random.randrange(10, 30)
            if player2.shield >= 100:
                player2.shield = 100
        if hit.type == 'gun':
            player2.powerup()


    
    ## if player died and the explosion has finished, end game
    if dual_play_flag == 0:
        if player.lives == 0 and not death_explosion.alive():
            game_over()
            #running = False
            # menu_display = True
            # pygame.display.update()
    

    #3 Draw/render
    screen.fill(BLACK)
    ## draw the stargaze.png image
    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)     ## 10px down from the screen
    draw_shield_bar(screen, 5, 5, player.shield)

    # Code added by Jiwoo
    if dual_play_flag == 1:
        #draw shield_bar For player2
        draw_shield_bar(screen, 5, 30, player2.shield)
        #draw lives_bar For player2
        draw_lives(screen, WIDTH - 150, 30, player2.lives, player_mini_img2)

        #If either of them is alive, the program will not shut down.
        if player.lives == 0 and not player2.lives == 0:
            player.kill()
        elif player2.lives == 0 and not player.lives == 0:
            player2.kill()
        #When both are dead, the program shuts down.
        elif player2.lives == 0  and player.lives == 0:
            game_over()
            #running = False

    # Draw lives
    draw_lives(screen, WIDTH - 150, 5, player.lives, player_mini_img)

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()
