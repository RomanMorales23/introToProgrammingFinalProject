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
        print("SHOOT")
        pew = (Projectile(10,10))
        bullets.add(pew)
        all_sprites.add(pew)
        #Prevents firing for the first second
        '''if FRAME > 30:
            # Thanks Andrew for the Delay 
            if FRAME % 3 == 0:
                pew = (Projectile(10,10))
                bullets.add(pew)
                all_sprites.add(pew)  '''     
        
        
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




# init pygame and create a window
pg.init()
pg.mixer.init()
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

#From Mr. Cozort to instantiate multiple enemies
for i in range(30):
    m = Enemy(randint(0,WIDTH), randint(0,HEIGHT), 20, 20, (RandColor(),RandColor(),RandColor()), 1, random.uniform(0,360))
    all_sprites.add(m)
    enemies.add(m)
    Enemy.add(m)
# add player to all sprites grousp

all_sprites.add(player, bullets, enemies)
# add platform to all sprites group





# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == JOYBUTTONDOWN:
            print(event)
            if event.button == 0:
                Player.shoot()
        if event.type == JOYBUTTONUP:
            print(event)
        if event.type == JOYAXISMOTION:
            #Sorts out which Joystick the Value is comming from 0 & 1 is left joystick axis while 2 & 3 is right
            if event.axis == 0 or event.axis == 1:
                JOYSTICK_Location_Left[event.axis] = event.value
            if event.axis == 2 or event.axis == 3:
                print(event.axis)
                JOYSTICK_Location_Right[event.axis - 2] = event.value
        if event.type == JOYHATMOTION:
            print(event)
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
    if player.vel.y > 0:
        if player.pos.y > HEIGHT: 
            player.pos.y = 0
    elif player.vel.y < 0:
        if player.pos.y  < 0:
            player.pos.y = HEIGHT
    if player.vel.x > 0:
        if player.pos.x > WIDTH:
            player.pos.x = 0
    elif player.vel.x < 0:
        if player.pos.x < 0:
            player.pos.x = WIDTH        
        
        
        '''
        saving code for later jut in case I decide I need it 

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
pg.quit()
