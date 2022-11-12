#My final Maine File
# content from kids can code: http://kidscancode.org/blog/
'''
Innovation:
- Change Controls into a direction and magnitude style (Complete)
- Change the Character into a assymetrical character (triangle) in orderr to allow 
better control by player (Complete)
- Make the boundaries looping for Enemies and PLayer, but not bullets to keep 
bullet count down (Complete)
- Create a shoot function to fire rectangles using the player current position and 
direction  (Complete)
- Make collisions between bullet and enemies (Complete)
- Create Death Function to kill player if enemie touches (Complete)
Goals: 
    Kill all the enemies
    Don't Die
Rules: 
    W- Forward (in what direction player is facing)
    A and D- Rotate Player
    SPACe (Hold)- Shoots projectiles to kill enemies
    Touching a enemie kills you
Feedback: 
    Score Count
    Death Popup
Freedom:
    Movement
    Shooting
    Looping Boundaries
'''
# import libraries and modules
from os import kill
from pickle import FALSE, TRUE
import pygame as pg
import math
from pygame.sprite import Sprite
import random
from random import randint
#reassigns name to Vector2
vec = pg.math.Vector2
# game settings 
WIDTH = 1280
HEIGHT = 720
FPS = 30
# player settings
PLAYER_GRAV = 0.0
PLAYER_FRIC = 0.01
PLAYER_TURN_RATE = 0.2 #radians
SPEED = 1
FRAME = 1
BULLET_SPEED = 20
SCORE = 0
BULLET_PEN = FALSE
DEAD = 0
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#From Mr. Cozort  
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('Impact')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)
def RandColor():
    return random.randint(0,255)
###############################################Class Player###############################################
class Player(Sprite):
    def __init__(self,direction):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 20), pg.SRCALPHA)
        self.image.fill(BLACK)
        self.original_image = self.image
        self.rect = pg.draw.polygon(self.image, (WHITE), ((0, 0), (0, 20), (50, 
10)))
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = math.radians(direction)
    #Controls altered to use a direction and magnitude instead of individual x and y inputs 
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.direction -= PLAYER_TURN_RATE
        if keys[pg.K_d]:
            self.direction += PLAYER_TURN_RATE
        if keys[pg.K_w]:
            #Alters x and y acceloration coefficients based on the direcitonal angle  to simulate an acceleration at said angle
           self.acc.y = SPEED * math.sin(self.direction)
           self.acc.x = SPEED * math.cos(self.direction)
        if keys[pg.K_SPACE]:
            # Thanks Andrew for the Delay 
            if FRAME % 5 == 0:
                pew = (Projectile(10,10))
                bullets.add(pew)
                all_sprites.add(pew)
                
     
    def update(self):
        if pg.sprite.spritecollide(self, enemies, FALSE):
            print("DEATH")
            self.kill()
            global DEAD
            DEAD = 1
        #Rotates the sprite according to the direction control
        self.image = pg.transform.rotate(self.original_image, -self.direction 
*57.2958)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        #Resets Acceloration to zero so it does not become additive
        self.acc = vec(0,0)
        
        #considering implementing a collision later on...
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
        self.vel = vec(math.cos(player.direction) * 
BULLET_SPEED,math.sin(player.direction)* BULLET_SPEED)
        self.acc = vec(0,0)
   
    def update(self):
        
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
    m = Enemy(randint(0,WIDTH), randint(0,HEIGHT), 20, 20, 
(RandColor(),RandColor(),RandColor()), 1, random.uniform(0,360))
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
        if player.pos.y < 0:
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
if player.pos.x > WIDTH:
    player.pos.x = 0
elif player.vel.x < 0:
    if player.pos.x < 0:
        player.pos.x = WIDTH        