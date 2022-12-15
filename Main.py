'''
Citations: 


Rect Collision with better accuracy - https://www.youtube.com/watch?v=1_H7InPMjaY&ab_channel=ClearCode
Controller Input - DaFluffyPotateo on YT: https://www.youtube.com/watch?v=Hp0M8iExfDc&ab_channel=DaFluffyPotato
Pygame Docuementation - https://www.pygame.org/docs/
Various Commands - Mr. Cozort 
Misc Help - Andrew :|
'''

#Importing Misc. libraries and modules
import sys
import os
from os import path
import time

#Importing Pygame Libraries
import pygame as pg
from pygame.sprite import Sprite
from pygame.locals import *

#Importing Math Related Libraries for input and vector Calculations 
import math
import random

#Created Libraries
from Settings import *

#Name Reassignments
vec = pg.math.Vector2

#From M. Cozort  
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('Impact')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

###############################################Player###############################################
class Player(Sprite):
    def __init__(self, w, h, direction, player_num):
        Sprite.__init__(self)  
        self.player_num = player_num      
        self.image = pg.Surface((w, h))
        #Differentiates Images For Player 1 & 2
        if player_num ==1: 
            self.original_image = player1_img
            self.original_image = pg.transform.scale(player1_img, (w, h))
            self.pos = vec( 25, HEIGHT/2)
        if player_num == 2:
            self.original_image = player2_img
            self.original_image = pg.transform.scale(player2_img, (w, h))
            self.pos = vec(WIDTH - 25, HEIGHT/2)
        #Uses specified color key to sortout background of Sprite
        self.original_image.set_colorkey(COLORKEY)
        self.rect = self.original_image.get_rect()
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
        global SHOT_TIMER_1
        if SHOT_TIMER_1 > 5:
            if PLAYER1_DEAD == False:
                pew = (Projectile(BULLET_SIZE,BULLET_SIZE, 1)) 
                p1_bullets.add(pew)
                all_sprites.add(pew)  
                SHOT_TIMER_1 = 0
    def shoot2(): 
        global SHOT_TIMER_2
        if SHOT_TIMER_2 > 5:
            if PLAYER2_DEAD == False:
                pew = Projectile(BULLET_SIZE,BULLET_SIZE, 2)
                p2_bullets.add(pew)
                all_sprites.add(pew)
                SHOT_TIMER_2 = 0     
    #Update Function For Player
    def update(self):
        
        if self.player_num == 2:
            if pg.sprite.spritecollide(self, p1_bullets, True):
                global PLAYER2_DEAD
                PLAYER2_DEAD = True
                self.kill()
        if self.player_num == 1:
            if pg.sprite.spritecollide(self, p2_bullets, True):
                global PLAYER1_DEAD
                PLAYER1_DEAD = True
                self.kill()
     

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
###############################################Projectile###############################################
class Projectile(Sprite): 
    def __init__(self,w,h, player_num):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.player_num = player_num
        #Divides Porjectile Class by Player Number to seperate spawning and interaction

        if player_num == 1:
            #Sets bullet position to player position, but accounts for offset of gun barrel from center of player 
            self.rect.center = (player1.pos.x + math.cos(player1.direction + math.radians(90)) * 7, player1.pos.y - math.sin(player1.direction - math.radians(90)) * 7)
            self.pos = vec(self.rect.center)

            #Turns Cordinates of joystick into Direction for Player
            self.vel = vec(math.cos(player1.direction) * BULLET_SPEED,math.sin(player1.direction)* BULLET_SPEED)

        if player_num == 2:
            self.rect.center = (player2.pos.x + math.cos(player2.direction + math.radians(90)) * 7, player2.pos.y - math.sin(player2.direction - math.radians(90)) * 7)
            self.pos = vec(self.rect.center)

            #Turns Cordinates of joystick into Direction for Player
            self.vel = vec(math.cos(player2.direction) * BULLET_SPEED,math.sin(player2.direction)* BULLET_SPEED)

        self.TIME_ALIVE = 0
        #Resets Acceloration to 0 
        self.acc = (0,0)
   
    def update(self):

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

#Courtesy of Andrew and Edited by Me:
class Wall(Sprite):
    def __init__(self, x, y, iterations, health):
        Sprite.__init__(self)
        self.image = pg.Surface((WALL_SIZE, WALL_SIZE))
        self.image.fill(GREY)
        self.image = pg.transform.scale(Walls_Img, ((WALL_SIZE, WALL_SIZE)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.iterations = iterations
        self.health = health
    
    def update(self):
        prevx = self.x
        prevy = self.y
        if self.health <= 2:
            self.image = pg.transform.scale(Walls2_Img, (WALL_SIZE, WALL_SIZE))
        if self.health <= 1:
            self.image = pg.transform.scale(Walls3_Img, (WALL_SIZE, WALL_SIZE))
        if self.iterations == 1:
            for i in range(10):
                x = prevx + random.choice([-WALL_SIZE,0,WALL_SIZE])
                y = prevy + random.choice([-WALL_SIZE,0,WALL_SIZE])
                prevx = x
                prevy = y
                wall = Wall(x, y, 0, WALL_HEALTH)
                wall_list.append(wall)
                walls.add(wall)
                all_sprites.add(wall)
            self.kill()
        #Kills Bullets upon touching wall and Damages Wall
        if self.health <= 0:
            self.kill()
        if pg.sprite.spritecollide(self, p1_bullets, True) or pg.sprite.spritecollide(self, p2_bullets, True):
            self.health -= 1
        #Prevents Wall SPawning on Player
        if self.x < 250 or self.x > (WIDTH-250): 
            self.kill()





#Init pygame and create a window
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


#Image Loading from Game Tutorials
game_folder = os.path.dirname(__file__)
img_dir1 = os.path.join(game_folder, 'images')

#Image Loading (Andrew)
player1_img = pg.image.load(path.join(img_dir1, "player_blue.png")).convert()
player2_img = pg.image.load(path.join(img_dir1, "player_orange.png")).convert()
Tombstone = pg.image.load(path.join(img_dir1, "Tombstone.png")).convert()
Background = pg.image.load(path.join(img_dir1, "Background.png")).convert()
Walls_Img = pg.image.load(path.join(img_dir1, "Wall.png")).convert()
Walls2_Img = pg.image.load(path.join(img_dir1, "Wall2.png")).convert()
Walls3_Img = pg.image.load(path.join(img_dir1, "Wall3.png")).convert()

#Creating groups for all sprites
all_sprites = pg.sprite.Group()
p2_bullets = pg.sprite.Group()
walls = pg.sprite.Group()
p1_bullets = pg.sprite.Group()


#Instantiate classes
player1 = Player(PLAYER_WIDTH, PLAYER_HEIGHT, 0,1)
player2 = Player(PLAYER_WIDTH, PLAYER_HEIGHT, 180,2)
Shoort = Projectile(100,100,1)

#Ddd player to all sprites grousp
all_sprites.add(player1,player2)

#Walls Option and Spawning from Andrew
if WALLS == True:
    for i in range (AMOUNT_WALLS):
        x= random.randint(3, math.floor(WIDTH/WALL_SIZE)) * WALL_SIZE
        y= random.randint(0, math.floor(HEIGHT/WALL_SIZE)) * WALL_SIZE
        wall = Wall(x,y, 1, WALL_HEALTH)
        wall_list.append(wall)
        walls.add(wall)        
        all_sprites.add(wall) 


# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)
    #Displays FPS in caption of window
    pg.display.set_caption("FPS: " + str(int(clock.get_fps())))
    #From DaFluffyPotatoe:
    for event in pg.event.get():
        if event.type == JOYAXISMOTION:
            #Player 1  Controls
            if event.joy == 1:
                if event.axis == 5:
                    if event.value == 1:
                        Player.shoot1()
                if event.axis == 0 or event.axis == 1:
                    JOY1_Location_Left[event.axis] = event.value
                if event.axis == 2 or event.axis == 3:
                    JOY1_Location_Right[event.axis - 2] = event.value
            #Player 2 Controls
            if event.joy == 0:
                if event.axis == 5:
                    if event.value == 1:
                        Player.shoot2()
                if event.axis == 0 or event.axis == 1:
                    JOY2_Location_Left[event.axis] = event.value
                if event.axis == 2 or event.axis == 3:
                    JOY2_Location_Right[event.axis - 2] = event.value

        #Checks for Devices and lists in terminal
        if event.type == JOYDEVICEADDED:
            joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
            for joystick in joysticks:
                print(joystick.get_name())
        if event.type == JOYDEVICEREMOVED:
            joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]

        #Close Window on Keypress
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                sys.exit()
        #Check for closed window and stops RUNNING loop
        if event.type == pg.QUIT:
            running = False


    #Collision Detection for Walls vs Player
    hits1 = pg.sprite.spritecollide(player1, walls, False)
    hits2 = pg.sprite.spritecollide(player2, walls, False)
        #Player 1
    if hits1: 
        ''' 
            This collision section requies a duplication to prevent player sliding through
            wall if they were already touching another wall. This section checks collision 
            with UP TO 2 wallS, the maximum needed in my case.
        '''
        if abs(player1.rect.top - hits1[0].rect.bottom) < Collision_Tolerance: 
            player1.pos.y = hits1[0].rect.bottom + (abs(player1.rect.top-player1.pos.y)) - 2
            player1.vel.y = 0
        if abs(player1.rect.bottom - hits1[0].rect.top) < Collision_Tolerance: 
            player1.pos.y = hits1[0].rect.top - (abs(player1.rect.bottom-player1.pos.y)) + 2 
            player1.vel.y = 0
        if abs(player1.rect.right - hits1[0].rect.left) < Collision_Tolerance: 
            player1.pos.x = hits1[0].rect.left - (abs(player1.rect.right-player1.pos.x))
            player1.vel.x = 0
        if abs(player1.rect.left - hits1[0].rect.right) < Collision_Tolerance: 
            player1.pos.x = hits1[0].rect.right + (abs(player1.rect.left-player1.pos.x))
            player1.vel.x = 0

        try:
            if abs(player1.rect.top - hits1[1].rect.bottom) < Collision_Tolerance: 
                player1.pos.y = hits1[1].rect.bottom + (abs(player1.rect.top-player1.pos.y)) - 2
                player1.vel.y = 0
            if abs(player1.rect.bottom - hits1[1].rect.top) < Collision_Tolerance: 
                player1.pos.y = hits1[1].rect.top - (abs(player1.rect.bottom-player1.pos.y)) + 2
                player1.vel.y = 0
            if abs(player1.rect.right - hits1[1].rect.left) < Collision_Tolerance: 
                player1.pos.x = hits1[1].rect.left - (abs(player1.rect.right-player1.pos.x))
                player1.vel.x = 0
            if abs(player1.rect.left - hits1[1].rect.right) < Collision_Tolerance: 
                player1.pos.x = hits1[1].rect.right + (abs(player1.rect.left-player1.pos.x))
                player1.vel.x = 0
        except:
            pass #prevents crashing if player is only touching one wall
            
        #Player 2
    if hits2:
        if abs(player2.rect.top - hits2[0].rect.bottom) < Collision_Tolerance: 
            player2.pos.y = hits2[0].rect.bottom + (abs(player2.rect.top-player2.pos.y)) - 2
            player2.vel.y = 0
        if abs(player2.rect.bottom - hits2[0].rect.top) < Collision_Tolerance: 
            player2.pos.y = hits2[0].rect.top - (abs(player2.rect.bottom-player2.pos.y)) + 2 
            player2.vel.y = 0
        if abs(player2.rect.right - hits2[0].rect.left) < Collision_Tolerance: 
            player2.pos.x = hits2[0].rect.left - (abs(player2.rect.right-player2.pos.x))
            player2.vel.x = 0
        if abs(player2.rect.left - hits2[0].rect.right) < Collision_Tolerance: 
            player2.pos.x = hits2[0].rect.right + (abs(player2.rect.left-player2.pos.x))
            player2.vel.x = 0

        try:
            if abs(player2.rect.top - hits2[1].rect.bottom) < Collision_Tolerance: 
                player2.pos.y = hits2[1].rect.bottom + (abs(player2.rect.top-player2.pos.y)) - 2
                player2.vel.y = 0
            if abs(player2.rect.bottom - hits2[1].rect.top) < Collision_Tolerance: 
                player2.pos.y = hits2[1].rect.top - (abs(player2.rect.bottom-player2.pos.y)) + 2
                player2.vel.y = 0
            if abs(player2.rect.right - hits2[1].rect.left) < Collision_Tolerance: 
                player2.pos.x = hits2[1].rect.left - (abs(player2.rect.right-player2.pos.x))
                player2.vel.x = 0
            if abs(player2.rect.left - hits2[1].rect.right) < Collision_Tolerance: 
                player2.pos.x = hits2[1].rect.right + (abs(player2.rect.left-player2.pos.x))
                player2.vel.x = 0
        except:
            pass #prevents crashing if player is only touching one wall

    #Preparing Images 
    Scaled_Background = pg.transform.scale(Background, (WIDTH/2, HEIGHT))
    Scaled_Tombstone = pg.transform.scale(Tombstone, (35,35))
    Tombstone.set_colorkey(COLORKEY)
    
    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ########## Draw ################
    # draw the background screen
    screen.fill(GREY)
    # draw all sprites
    screen.blit(Scaled_Background, (0,0))
    screen.blit(Scaled_Background, (WIDTH/2, 0))
    all_sprites.draw(screen)
    p2_bullets.draw(screen)
    p1_bullets.draw(screen)
    
    
    
    #Drawing Tombstone & Text

    if PLAYER1_DEAD:
        screen.blit(Scaled_Tombstone, (player1.pos.x - 20,player1.pos.y - 10))
        draw_text("P1", 10, BLACK, player1.pos.x, player1.pos.y - 5)
        draw_text("Player 2 Wins!", 100, WHITE, WIDTH/2, HEIGHT/2)
    else:
       draw_text("P1", 10, WHITE, player1.pos.x, player1.pos.y - 30) 
    if PLAYER2_DEAD:
        screen.blit(Scaled_Tombstone, (player2.pos.x - 20,player2.pos.y - 10))
        draw_text("P2", 10, BLACK, player2.pos.x, player2.pos.y - 5)
        draw_text("Player 1 Wins!", 100, WHITE, WIDTH/2, HEIGHT/2)
    else:
        draw_text("P2", 10, WHITE, player2.pos.x, player2.pos.y - 30)
    
    draw_text(" Press ESC to close Window", 15, WHITE, 150, 5)
    # buffer - after drawing everything, flip display
    pg.display.flip()
    
    #Misc Counters 
    FRAME += 1
    SHOT_TIMER_1 += 1
    SHOT_TIMER_2 += 1
pg.quit()
