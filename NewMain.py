'''
FINAL PROJECT

    This project is going to be a 2 player game which uses Stadia Controllers as Input. I w
'''
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


#Name Reassignments
vec = pg.math.Vector2


#Class for Player
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
        pass

        
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            pg.quit()
            self.direction -= PLAYER_TURN_RATE
        # if keys[pg.K_d]:
        #     self.direction += PLAYER_TURN_RATE
        # if keys[pg.K_w]:
        #     #Alters x and y acceloration coefficients based on the direcitonal angle  to simulate an acceleration at said angle
        #    self.acc.y = SPEED * math.sin(self.direction)
        #    self.acc.x = SPEED * math.cos(self.direction)
        # if keys[pg.K_SPACE]:
        #     # Thanks Andrew for the Delay 
        #     if FRAME % 5 == 0:
        #         pew = (Projectile(10,10))
        #         bullets.add(pew)
        #         all_sprites.add(pew)


    def update(self):
        #if pg.sprite.spritecollide(self, FALSE):
            #if CAN_DIE:
             #   pass
                # print("DEATH")
                # #self.kill()
                # global DEAD
                # DEAD = 1
        #Rotates the sprite according to the direction control
        self.image = pg.transform.rotate(self.original_image, -self.direction *57.2958)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        #Resets Acceloration to zero so it does not become additive
        self.acc = vec(0,0)
        
        #considerinag implementing a collision later on...
        '''hits = pg.sprite.spritecollide(self, all_platforms, False)
        if hits:
            print("I've collided")'''
       
        #Updates Controls 
        self.controls()
        # friction and position updates
        self.acc.x += self.vel.x * -PLAYER_FRIC
        self.acc.y += self.vel.y * -PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos


# init pygame and create a window
pg.init()
pg.mixer.init()

#Init for Joystick Inputs & Prints out devices

pg.joystick.init()
print(str(pg.joystick.get_count()) + " - Joysticks Connected")
print("Joysticks Initialized")
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

#Create Display
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
# instantiate classes
player = Player(0)


# add player to all sprites grousp
all_sprites.add(player, bullets, enemies)
# add platform to all sprites group
# Game loop
running = True
while running:
    print(event.type)
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    ############ Update ##############
    # update all sprites
    all_sprites.update()
    all_platforms.update()


    ########## Draw ################
    # draw the background screen
    screen.fill(BLACK)
    # draw all sprites
    all_sprites.draw(screen)
    #Text 
    # buffer - after drawing everything, flip display
    pg.display.flip()
    
    FRAME += 1


pg.quit()        
if player.pos.x > WIDTH:
    player.pos.x = 0
elif player.vel.x < 0:
    if player.pos.x < 0:
        player.pos.x = WIDTH        