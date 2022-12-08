'''
Citations: 

Controller Input - DaFluffyPotateo on YT: https://www.youtube.com/watch?v=Hp0M8iExfDc&ab_channel=DaFluffyPotato
Pygame Docuementation - https://www.pygame.org/docs/
Various Commands - Mr. Cozort 
'''

#Importing Misc. libraries and modules
import sys
import os
from os import path



#Importing Pygame Libraries
import pygame as pg
from pygame.sprite import Sprite
from pygame.locals import *


#Importing Math Related Libraries for input and vector Calculations 
import math
import random
from random import randint

#Created Libraries
from Settings import *


#Name Reassignments
vec = pg.math.Vector2

#reassigns name to Vector2
vec = pg.math.Vector2

#From M. Cozort  
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('Impact')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)
def RandColor():
    return random.randint(0,255)

###############################################Class Player One (WSD SPACE)###############################################
class Player(Sprite):
    def __init__(self,direction, player_num):
        Sprite.__init__(self)  
        self.player_num = player_num      
        self.image = pg.Surface((25, 19))
        #Differentiates Images For Player 1 & 2
        if player_num ==1: 
            self.original_image = player1_img
            self.original_image = pg.transform.scale(player1_img, (25, 19))
            self.pos = vec(WIDTH/2, HEIGHT/2)
        if player_num == 2:
            self.original_image = player2_img
            self.original_image = pg.transform.scale(player2_img, (25, 19))
            self.pos = vec(WIDTH/2 - 20, HEIGHT/2 - 20)
        self.original_image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.player_num = player_num
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = math.radians(direction)
    #Controls altered to use a direction and magnitude instead of individual x and y inputs 
    def controls(self):
        #Differentiates Controls for Player 1 & 2
        if self.player_num == 1:
            if abs(JOY1_Location_Left[1]) > DEADZONE:
                self.vel.y = JOY1_Location_Left[1] * SPEED
            if abs(JOY1_Location_Left[0]) > DEADZONE:
                self.vel.x = JOY1_Location_Left[0] * SPEED
            if abs(JOY1_Location_Right[0]) > DEADZONE:
                if JOY1_Location_Right[0] > 0:
                    self.direction = math.atan((JOY1_Location_Right[1] / JOY1_Location_Right[0]))
                elif JOY1_Location_Right[0] < 0:
                    self.direction = math.pi + math.atan((JOY1_Location_Right[1] / JOY1_Location_Right[0]))
        if self.player_num == 2:
            if abs(JOY2_Location_Left[1]) > DEADZONE:
                self.vel.y = JOY2_Location_Left[1] * SPEED
            if abs(JOY2_Location_Left[0]) > DEADZONE:
                self.vel.x = JOY2_Location_Left[0] * SPEED
            if abs(JOY2_Location_Right[0]) > DEADZONE:
                if JOY2_Location_Right[0] > 0:
                    self.direction = math.atan((JOY2_Location_Right[1] / JOY2_Location_Right[0]))
                elif JOY2_Location_Right[0] < 0:
                    self.direction = math.pi + math.atan((JOY2_Location_Right[1] / JOY2_Location_Right[0]))
    #Seperated Shoot Functions to not kill the player itself
    def shoot1():
        global SHOT_TIMER_2
        if SHOT_TIMER_2 > 5:
            if event.joy == 0:
                pew = (Projectile(2,2, 2))        
                p2_bullets.add(pew)
                all_sprites.add(pew)
            SHOT_TIMER_2 = 0
    def shoot2(): 
        global SHOT_TIMER_1
        if SHOT_TIMER_1 > 5:
            if event.joy == 1: 
                pew = (Projectile(2,2, 1))
                p1_bullets.add(pew)
                all_sprites.add(pew)
            SHOT_TIMER_1 = 0     
    #Update Function For Player
    def update(self):
        #Wall Collision
        if pg.sprite.spritecollide(self, walls, False):
            if self.player_num == 1:
                print("Player 1 Colliding")
                self.acc = (0,0)
                player1.vel == (0,0)
            if self.player_num == 2:
                print("Player 2 Colliding")
            self.vel.y = 0
        if self.player_num == 2:
            if pg.sprite.spritecollide(self, p1_bullets, True):
                print("P2 DEAD")
                #Prevents Player Death for the first second
                if CAN_DIE == True:
                    self.kill()
                    global DEAD
                    DEAD = 1
        if self.player_num == 1:
            if pg.sprite.spritecollide(self, p2_bullets, True):
                print("P1 DEAD?")
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
        #Screen Boundaries
        if self.pos.x > WIDTH - SAFEZONE:
            self.pos.x = WIDTH - SAFEZONE
        if self.pos.y > HEIGHT - SAFEZONE:
            self.pos.y = HEIGHT - SAFEZONE
        if self.pos.x < 0 + SAFEZONE:
            self.pos.x = 0 + SAFEZONE
        if self.pos.y < 0 + SAFEZONE:
            self.pos.y = 0 + SAFEZONE
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
    def __init__(self,w,h, player_num):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.player_num = player_num
        if player_num == 1:
            self.rect.center = (player1.pos.x, player1.pos.y)
            self.pos = vec(player1.pos.x, player1.pos.y)
            self.vel = vec(math.cos(player1.direction) * BULLET_SPEED,math.sin(player1.direction)* BULLET_SPEED)
        if player_num == 2:
            self.rect.center = (player2.pos.x, player2.pos.y)
            self.pos = vec(player2.pos.x, player2.pos.y)
            self.vel = vec(math.cos(player2.direction) * BULLET_SPEED,math.sin(player2.direction)* BULLET_SPEED)
        self.TIME_ALIVE = 0
        # Makes the velocity equal to the player direction, but in terms of x and y
        #Then multiplied by the setting of bullet speed
        self.acc = vec(0,0)
   
    def update(self):
        if self.player_num == 1:
            pg.sprite.spritecollide(self, player1, True)
        if self.player_num == 2:
            #pg.sprite.spritecollide(self, player2, True)
            pass

        #Kills bullet when leaving screen
        if self.pos.y > HEIGHT or self.pos.y < 0:
            self.kill() 
        if self.pos.x > WIDTH or self.pos.y < 0:
            self.kill()
        #Resets Acceleration to zero so it does not become additive
        self.acc = vec(0,0) 
        self.rect = self.image.get_rect(center=self.rect.center)

        #   Updating movement
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

###############################################Walls###############################################

#Courtesy of Andrew:
class Wall(Sprite):
    def __init__(self, x, y, iterations):
        Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.iterations = iterations
    
    def update(self):
        prevx = self.x
        prevy = self.y
        if self.iterations == 1:
            for i in range(10):
                x = prevx + random.choice([-9, 0, 9])
                y = prevy + random.choice([-9, 0, 9])
                prevx = x
                prevy = y
                wall = Wall(x, y, 0)
                wall_list.append(wall)
                walls.add(wall)
                all_sprites.add(wall)
            self.kill()
        #Kills Bullets upon touching wall
        pg.sprite.spritecollide(self, p1_bullets, True)
        pg.sprite.spritecollide(self, p2_bullets, True)



# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
#Image Loading from Andrew

game_folder = os.path.dirname(__file__)
img_dir1 = os.path.join(game_folder, 'images')

#img_dir1 = path.join(path.dirname(__file__), r'C:\GitHub\introToProgramming\introToProgrammingFinalProject\images')
#Image Loading 
player1_img = pg.image.load(path.join(img_dir1, "player_blue.png")).convert()
player2_img = pg.image.load(path.join(img_dir1, "player_orange.png")).convert()
# create a group for all sprites

all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
p2_bullets = pg.sprite.Group()
walls = pg.sprite.Group()
p1_bullets = pg.sprite.Group()


# instantiate classes
player1 = Player(0,1)
player2 = Player(0,2)

#From Mr. Cozort to instantiate multiple enemies
# add player to all sprites grousp

all_sprites.add(player1,player2)
# add platform to all sprites group

#Walls Option
if WALLS == True:  
    for i in range(AMOUNT_WALLS): 
        x = random.randint(0, WIDTH/20 - 1) * 20 + 10
        y = random.randint(0, HEIGHT/20 - 1) * 20 + 10
        wall = Wall(x, y, 1)
        wall_list.append(wall)
        walls.add(wall)
        all_sprites.add(wall)


# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == JOYBUTTONDOWN:
            if event.button == 0:
                pass
        if event.type == JOYBUTTONUP:
            pass
        if event.type == JOYAXISMOTION:
            #Trigger is Considered an Axis
            if event.joy == 1:
                if event.axis == 5:
                    if event.value == 1:
                        Player.shoot2()
                #Sorts out which Joystick the Value is comming from 0 & 1 is left joystick axis while 2 & 3 is right
                if event.axis == 0 or event.axis == 1:
                    JOY1_Location_Left[event.axis] = event.value
                if event.axis == 2 or event.axis == 3:
                    JOY1_Location_Right[event.axis - 2] = event.value
            if event.joy == 0:
                if event.axis == 5:
                    if event.value == 1:
                        Player.shoot1()
                #Sorts out which Joystick the Value is comming from 0 & 1 is left joystick axis while 2 & 3 is right
                if event.axis == 0 or event.axis == 1:
                    JOY2_Location_Left[event.axis] = event.value
                if event.axis == 2 or event.axis == 3:
                    JOY2_Location_Right[event.axis - 2] = event.value
        if event.type == JOYDEVICEADDED:
            joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
            for joystick in joysticks:
                print(joystick.get_name())
        if event.type == JOYDEVICEREMOVED:
            joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                sys.exit()
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    

    #Collision Detection
    hits1 = pg.sprite.spritecollide(player1, walls, False)
    hits2 = pg.sprite.spritecollide(player2, walls, False)
    print(hits1)
    print(hits2)

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
    draw_text("SCORE:     " + str(SCORE), 20, WHITE, WIDTH/2, 20)
    if DEAD == 1:
        draw_text("YOU DIED :|", 100, WHITE, WIDTH/2, HEIGHT/2)
    # buffer - after drawing everything, flip display
    pg.display.flip()
    
    FRAME += 1
    SHOT_TIMER_1 += 1
    SHOT_TIMER_2 += 1
pg.quit()
