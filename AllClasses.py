#Importing Misc. libraries and modules
import sys
from os import kill
from pickle import FALSE, TRUE

#Importing Pygame Libraries
import pygame as pg
#from pygame import *
from pygame.sprite import Sprite
from pygame.locals import *


#Importing Math Related Libraries
import math
import random
from random import randint

#Created Libraries
from Settings import *
from NewMain import *

#Name Reassignments
vec = pg.math.Vector2

#reassigns name to Vector2
vec = pg.math.Vector2


class Player(Sprite):
    def __init__(self,direction):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 20), pg.SRCALPHA)
        self.image.fill(BLACK)
        self.original_image = self.image
        self.rect = pg.draw.polygon(self.image, (WHITE), ((0, 0), (0, 20), (50, 10)))
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = math.radians(direction)
    #Controls altered to use a direction and magnitude instead of individual x and y inputs 
    def controls(self):
        if abs(JOYSTICK_Location_Left[1]) > DEADZONE:
            self.vel.y = JOYSTICK_Location_Left[1] * SPEED
        if abs(JOYSTICK_Location_Left[0]) > DEADZONE:
            self.vel.x = JOYSTICK_Location_Left[0] * SPEED
        if abs(JOYSTICK_Location_Right[0]) > DEADZONE:
            if JOYSTICK_Location_Right[0] > 0:
                self.direction = math.atan((JOYSTICK_Location_Right[1] / JOYSTICK_Location_Right[0]))
            elif JOYSTICK_Location_Right[0] < 0:
                self.direction = math.pi + math.atan((JOYSTICK_Location_Right[1] / JOYSTICK_Location_Right[0]))
    def shoot():
        global SHOT_TIMER
        if SHOT_TIMER > 10:
            print("I FIRED")
            pew = (Projectile(10,10))
            bullets.add(pew)
            all_sprites.add(pew)
            SHOT_TIMER = 0     
        
        
        '''keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.direction -= PLAYER_TURN_RATE
        if keys[pg.K_d]:
            self.direction += PLAYER_TURN_RATE
        if keys[pg.K_w]:
            #Alters x and y acceloration coefficients based on the direcitonal angle  to simulate an acceleration at said angle
           self.acc.y = SPEED * math.sin(self.direction)
           self.acc.x = SPEED * math.cos(self.direction)
        if keys[pg.K_SPACE]:
            #Prevents firing for the first second
            if FRAME > 30:
                # Thanks Andrew for the Delay 
                if FRAME % 3 == 0:
                    pew = (Projectile(10,10))
                    bullets.add(pew)
                    all_sprites.add(pew)'''   
    def update(self):
        if pg.sprite.spritecollide(self, enemies, FALSE):
            #Prevents Player Death for the first second
            if FRAME > 30:
                if CAN_DIE == True:
                    self.kill()
                    global DEAD
                    DEAD = 1
        #Rotates the sprite according to the direction control
        self.image = pg.transform.rotate(self.original_image, math.degrees(-self.direction))
        self.rect = self.image.get_rect(center=self.rect.center)
        #Resets Acceloration to zero so it does not become additive
        self.acc = vec(0,0)
        #Updates Controls 
        self.controls()
        # friction and position updates
        self.acc.x += self.vel.x * -PLAYER_FRIC
        self.acc.y += self.vel.y * -PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        if self.vel.y > 0:
            if self.pos.y > HEIGHT: 
                self.pos.y = 0
        elif self.vel.y < 0:
            if self.pos.y  < 0:
                self.pos.y = HEIGHT
        if self.vel.x > 0:
            if self.pos.x > WIDTH:
                self.pos.x = 0
        elif self.vel.x < 0:
            if self.pos.x < 0:
                self.pos.x = WIDTH    

###############################################Platfroms###############################################
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

###############################################Projectile###############################################
class Projectile(Sprite): 
    def __init__(self,w,h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (player.pos.x, player.pos.y)
        self.pos = vec(player.pos.x, player.pos.y)
        
        # Makes the velocity equal to the player direction, but in terms of x and y
        #Then multiplied by the setting of bullet speed
        self.vel = vec(math.cos(player.direction) * BULLET_SPEED,math.sin(player.direction)* BULLET_SPEED)
        self.acc = vec(0,0)
   
    def update(self):
        if self.vel.y > 0:
            if self.pos.y > HEIGHT: 
                self.pos.y = 0
        elif self.vel.y < 0:
            if self.pos.y  < 0:
                self.pos.y = HEIGHT
        if self.vel.x > 0:
            if self.pos.x > WIDTH:
                self.pos.x = 0
        elif self.vel.x < 0:
            if self.pos.x < 0:
                self.pos.x = WIDTH 
        #If the bullet hits a enemy, the enemy is removed
        hit = pg.sprite.spritecollide(self, enemies, TRUE)
        if hit:
            #Not entirely sure why I had to mark this as global here, even though it is defined earlier...
            global SCORE
            SCORE +=1 
        #Resets Acceleration to zero so it does not become additive
        self.acc = vec(0,0) 
        self.rect = self.image.get_rect(center=self.rect.center)

        # Updating movement
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

###############################################Enemy###############################################

# Coutesy of Mr. Cozort
class Enemy(Sprite):
    def __init__(self, x, y, w, h, color, health, direction):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.health = health
        self.initialized = False
        self.direction = math.radians(direction) 

    def update(self):
        if BULLET_PEN:
        #If the bullet hits a enemy, the bullet gets removed (AKA no penetration)
            pg.sprite.spritecollide(self, bullets, TRUE)
        #Looping Boundaries for Enemies 
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        
        self.rect.y += self.speed * math.sin(self.direction)
        self.rect.x += self.speed * math.cos(self.direction)

# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
bullets = pg.sprite.Group()
enemies = pg.sprite.Group()

# instantiate classes
player = Player(0)

#From Mr. Cozort to instantiate multiple enemies
for i in range(30):
    m = Enemy(randint(0,WIDTH), randint(0,HEIGHT), 20, 20, (), 1, random.uniform(0,360))
    all_sprites.add(m)
    enemies.add(m)
    Enemy.add(m)
# add player to all sprites grousp

all_sprites.add(player, bullets, enemies)
# add platform to all sprites group

        