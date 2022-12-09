# game settings 
WIDTH = 1900
HEIGHT = 900
FPS = 60
# Game settings
PLAYER_GRAV = 0.0
PLAYER_FRIC = 0.5
PLAYER_TURN_RATE = 0.2 #radians
SPEED = 10
FRAME = 1
BULLET_SPEED = 20
BULLET_PEN = False
CAN_DIE = True
WALL_HEALTH = 3
BULLET_LIFESPAN = 150
#Player1 Control Mapping
JOY1_Location_Left = [0,0]
JOY1_Location_Right = [0,0]
#Player2 Contol Mapping
JOY2_Location_Left = [0,0]
JOY2_Location_Right = [0,0]
Max_Wall_Length = 5
WALLS = True
AMOUNT_WALLS = 60
#Savezone is the amount the character stay on the edge of the screen
SAFEZONE = 10
#Joystick Deadzone
DEADZONE = 0.01
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
COLORKEY = (20,20,20) #Used to Sort Out Backgrounds

#Global Variables
DEAD = 0
SCORE = 0
FRAME = 1
SHOT_TIMER_1 = 0
SHOT_TIMER_2 = 0
wall_list = []
PLAYER1_DEAD = False
PLAYER2_DEAD = False

