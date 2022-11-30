'''
Citations: 

Controller Input - DaFluffyPotateo on YT: https://www.youtube.com/watch?v=Hp0M8iExfDc&ab_channel=DaFluffyPotato
Pygame Docuementation - https://www.pygame.org/docs/
Various Commands - Mr. Cozort 
'''

#Importing Misc. libraries and modules
import sys
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
    def __init__(self,direction):
        Sprite.__init__(self)        
        '''self.image = pg.Surface((50, 20), pg.SRCALPHA)
        self.image.fill(BLACK)
        self.original_image = self.image
        self.rect = pg.draw.polygon(self.image, (WHITE), ((0, 0), (0, 20), (50, 10)))
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = math.radians(direction)'''

        self.image = pg.Surface((25, 19))
        self.original_image = player1_img
        self.original_image = pg.transform.scale(player1_img, (25, 19))
        self.original_image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = math.radians(direction)
    #Controls altered to use a direction and magnitude instead of individual x and y inputs 
    def controls(self):
        keys= pg.key.get_pressed()


        if keys[pg.K_a]:
            self.vel.x = -SPEED * 10
        if keys[pg.K_d]:
            self.vel.x = SPEED * 10
        if keys[pg.K_w]:
            self.vel.y = -SPEED * 10
        if keys[pg.K_s]:
            self.vel.y = SPEED *10


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
        if SHOT_TIMER > 5:
            print("I FIRED")
            pew = (Projectile(10,10))
            bullets.add(pew)
            all_sprites.add(pew)
            SHOT_TIMER = 0        
    def update(self):
        if pg.sprite.spritecollide(self, walls, False):
            self.vel.xy = (0,0)
        if pg.sprite.spritecollide(self, bullets, False):
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
    def __init__(self,w,h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (player.pos.x, player.pos.y)
        self.pos = vec(player.pos.x, player.pos.y)
        self.TIME_ALIVE = 0
        # Makes the velocity equal to the player direction, but in terms of x and y
        #Then multiplied by the setting of bullet speed
        self.vel = vec(math.cos(player.direction) * BULLET_SPEED,math.sin(player.direction)* BULLET_SPEED)
        self.acc = vec(0,0)
   
    def update(self):
        #kills bullet after Time Alive 
        if self.TIME_ALIVE > BULLET_LIFESPAN:
            self.kill()
            print("Bullet DIED")
        self.TIME_ALIVE += 1
        print(self.TIME_ALIVE)

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
        #Resets Acceleration to zero so it does not become additive
        self.acc = vec(0,0) 
        self.rect = self.image.get_rect(center=self.rect.center)

        # Updating movement
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



# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
#Image Loading from Andrew
img_dir1 = path.join(path.dirname(__file__), r'C:\GitHub\introToProgramming\introToProgrammingFinalProject\images')
#Image Loading 
player1_img = pg.image.load(path.join(img_dir1, "player_blue.png")).convert()
# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
bullets = pg.sprite.Group()
walls = pg.sprite.Group()


# instantiate classes
player = Player(0)

#From Mr. Cozort to instantiate multiple enemies
# add player to all sprites grousp

all_sprites.add(player, bullets)
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
                Player.shoot()
        if event.type == JOYBUTTONUP:
            pass
        if event.type == JOYAXISMOTION:
            print(event.joy)#######################USE AN IF STATEMENT TO SORT OUT INPUTS, DUPLICATE PLAYER CLASS WITH DIFFERENT VARIABLE NAMES################################################
            #Trigger is Considered an Axis
            if event.axis == 5:
                if event.value == 1:
                    print(event.value)
                    Player.shoot()

            #Sorts out which Joystick the Value is comming from 0 & 1 is left joystick axis while 2 & 3 is right
            if event.axis == 0 or event.axis == 1:
                JOYSTICK_Location_Left[event.axis] = event.value
            if event.axis == 2 or event.axis == 3:
                JOYSTICK_Location_Right[event.axis - 2] = event.value
        if event.type == JOYHATMOTION:
            pass
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
    
    ############ Update ##############
    # update all sprites
    all_sprites.update()
    all_platforms.update()


    #Player Looping Boundaries as well as Platform Hits        
    '''saving code for later jut in case I decide I need it 

        hits = pg.sprite.spritecollide(player, all_platforms, False)    
        if hits:
            player.rect.top = hits[0].rect.bottom
            player.vel.y = 1'''


  
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
    SHOT_TIMER += 1
pg.quit()
