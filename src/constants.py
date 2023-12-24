import pygame
import enum

# Path
DOOR = '../Assets/door.png'
TILE = '../Assets/floor.png'
GOLD_TILE = '../Assets/floor_gold.png'
WUMPUS = '../Assets/wumpus.png'
GOLD = '../Assets/gold.png'
PIT = '../Assets/pit.png'
TERRAIN ='../Assets/terrain.png'
PLAYER_DOWN ='../Assets/agent_down.png'
PLAYER_UP ='../Assets/agent_up.png'
PLAYER_LEFT ='../Assets/agent_left.png'
PLAYER_RIGHT ='../Assets/agent_right.png'
ARROW_DOWN ='../Assets/arrow_down.png'
ARROW_UP ='../Assets/arrow_up.png'
ARROW_LEFT ='../Assets/arrow_left.png'
ARROW_RIGHT ='../Assets/arrow_right.png'
SCORE ='../Assets/score_icon.png'

# Window
SCREEN_WIDTH = 970
SCREEN_HEIGHT = 710
CAPTION = 'Wumpus World'

MAP_STATE_LIST = ['MAP_1', 'MAP_2', 'MAP_3', 'MAP_4', 'MAP_5', ]

# Map
MAP_LIST = ['../Input/map_1.txt',
            '../Input/map_2.txt',
            '../Input/map_3.txt',
            '../Input/map_4.txt',
            '../Input/map_5.txt']
MAP_NUM = len(MAP_LIST)

# Fonts
FONT_MRSMONSTER = '../Assets/Fonts/mrsmonster.ttf'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (170, 170, 170)
BRONZE = (75, 75, 75)
RED = (255, 0, 0)
BROWN = (218, 160, 109)
BRONZE = (205, 127, 50)


class Action(enum.Enum):
    LEFT = 1
    UP = 2
    DOWN = 3
    RIGHT = 4
    SHOOT = 5
    GRAB = 6
    CLIMB = 7

# state
RUNNING = 'running'
NOT_RUNNING = 'not_running'
SELECT_MAP = 'select_map'
HOME = 'home'
ABOUT_US = 'about_us'

# postion
TITLE_POS = pygame.Rect(235, 180, 500, 50)
MEMBER_1_POS = pygame.Rect(235, 270, 500, 30)
MEMBER_2_POS = pygame.Rect(235, 310, 500, 30)
MEMBER_3_POS = pygame.Rect(235, 350, 500, 30)
MEMBER_4_POS = pygame.Rect(235, 390, 500, 30)
MEMBER_5_POS = pygame.Rect(235, 430, 500, 30)
MEMBER_BACK_POS = pygame.Rect(235, 470, 500, 50)

PLAY_POS = pygame.Rect(235, 250, 500, 80)
ABOUT_US = pygame.Rect(235, 350, 500, 80)
EXIT_POS = pygame.Rect(235, 450, 500, 80)

LEVEL_1_POS = pygame.Rect(235, 200, 500, 50)
LEVEL_2_POS = pygame.Rect(235, 280, 500, 50)
LEVEL_3_POS = pygame.Rect(235, 360, 500, 50)
LEVEL_4_POS = pygame.Rect(235, 440, 500, 50)
LEVEL_5_POS = pygame.Rect(235, 520, 500, 50)
BACK_POS = pygame.Rect(235, 600, 500, 50)
