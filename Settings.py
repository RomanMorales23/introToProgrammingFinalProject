from screeninfo import get_monitors 
import math
for m in get_monitors():
    print("Monitor Width: " + str(m.width))
    print("Monitor Height: " + str(m.height))
# Window settings 
WIDTH = m.width
HEIGHT = m.height
FPS = 60
# Game settings
PLAYER_GRAV = 0.0
PLAYER_FRIC = 0.5
PLAYER_TURN_RATE = 0.2 #radians
FRAME = 1
BULLET_SPEED = 20
BULLET_PEN = False
CAN_DIE = True
WALL_HEALTH = 3
BULLET_LIFESPAN = 150

#Decimals are percentge of screen widths to allow sprites to scale approprietly with Screen Size
PLAYER_HEIGHT = math.ceil(2*0.0116666 *WIDTH * 0.9)
PLAYER_WIDTH = math.ceil(2*0.0233333 *HEIGHT * 0.9)
WALL_SIZE = math.ceil(0.028888888 * WIDTH)
BULLET_SIZE = math.ceil(0.00255555 * HEIGHT)
SPEED = (0.011 * HEIGHT)
BULLET_SPEED = (0.0222 * HEIGHT)
#Wall Settings
Max_Wall_Length = 5
WALLS = True
AMOUNT_WALLS = 50
#Savezone is the amount the character stay on the edge of the screen
SAFEZONE = 10
#Joystick Deadzone to prevent drifting and the stick tention bouncing it to the otherside
DEADZONE = 0.1
#Wall tolerance for Collisoin
Collision_Tolerance = 10

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (169,169,169)
YELLOW = (255, 255, 0)
COLORKEY = (181,230,29) #Used to Sort Out Backgrounds

#Global Variables
DEAD = 0
SCORE = 0
FRAME = 1
SHOT_TIMER_1 = 0
SHOT_TIMER_2 = 0
wall_list = []
PLAYER1_DEAD = False
PLAYER2_DEAD = False

#Player1 Control Mapping
JOY1_Location_Left = [0,0]
JOY1_Location_Right = [0,0]
#Player2 Contol Mapping
JOY2_Location_Left = [0,0]
JOY2_Location_Right = [0,0]




