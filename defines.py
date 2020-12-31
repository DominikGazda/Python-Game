import pygame,os
from score import *

#initialize game
pygame.init()
score = Score()


#colors defines
LIGHTBLUE = pygame.Color(255,255,255,128)
RED = pygame.Color(255, 0, 0, 0)
WHITE = pygame.Color(255, 255, 255, 255)
BLACK = pygame.Color(0, 0, 0, 0)
GRAY = pygame.Color(200,200,200,200)

#create screen
os.environ['SDL_VIDEO_CENTERED'] = '1'    # centrowanie okna
FPS = 30
SIZESCREEN = WIDTH, HEIGHT = 1366, 740
screen = pygame.display.set_mode(SIZESCREEN, pygame.DOUBLEBUF, 32)
hidden = pygame.Surface((SIZESCREEN))
hidden.fill((255,255,255))
hidden.set_alpha(0)
#Background
background = pygame.image.load('png/background.png')
background = pygame.transform.scale(background,(1366,740))

#Manu Background

bg_layer1 = pygame.image.load('menu_img/bg_layer1.png')
bg_layer1 = pygame.transform.scale(bg_layer1,(1366,740))
bg_layer2 = pygame.image.load('menu_img/bg_layer2.png')
bg_layer2 = pygame.transform.scale(bg_layer2,(1366,740))
bg_layer3 = pygame.image.load('menu_img/bg_layer3.png')
bg_layer3 = pygame.transform.scale(bg_layer3,(1366,740))
bg_layer4 = pygame.image.load('menu_img/bg_layer4.png')
bg_layer4 = pygame.transform.scale(bg_layer4,(1366,740))
bg_layer5 = pygame.image.load('menu_img/bg_layer5.png')
bg_layer5 = pygame.transform.scale(bg_layer5,(1366,740))

controls_bg = pygame.image.load('png/CONTROLS.png')
controls_bg = pygame.transform.scale(controls_bg,(900,300))

panel = pygame.image.load('menu_img/panel.png')
panel = pygame.transform.scale(panel,(900,260))

#Menu font
menu_font = pygame.font.SysFont('ARIAL BOLD', 100, 28)
screens_font = pygame.font.SysFont('ARIAL BOLD', 70, 20)

#Title and Icon
pygame.display.set_caption("Giereczka")
icon = pygame.image.load('png/icon_isaac.png')
pygame.display.set_icon(icon)


#Wczytywanie grafiki
file_names = sorted(os.listdir('png'))
BACKGROUND = pygame.image.load(os.path.join('png', 'background.png')).convert()
for file_name in file_names:
    image_name = file_name[:-4]
    if '_L' in image_name or '_R' in image_name:
        image_name = image_name.upper()
    else:
        image_name = image_name.upper()
    if 'PLAYER_' in image_name:
        image_name = image_name.replace('PLAYER_', '').upper()
    globals().__setitem__(image_name, pygame.image.load(
        os.path.join('png', file_name)).convert_alpha(BACKGROUND))


#grafika postaci
ISAAC_DOWN = pygame.image.load('png/isaac_front.png')

#ISAAC_R = pygame.image.load('png/ISAAC_R.png')
ISSAC_L = pygame.image.load('png/ISAAC_L.png')
ISAAC_UP = pygame.image.load('png/ISAAC_UP.png')
IMAGES_R = [ISAAC_R1, ISAAC_R2, ISAAC_R3, ISAAC_R4]
IMAGES_L = [ISAAC_L1, ISAAC_L2, ISAAC_L3, ISAAC_L4]
IMAGES_D = [ISAAC_D1, ISAAC_D2, ISAAC_D3, ISAAC_D4]
IMAGES_U = [ISAAC_U1, ISAAC_U2, ISAAC_U3, ISAAC_U4]
ISAAC_dead = pygame.image.load('png/player_dead.png')

#grafika przedmiotów
BASIC_BULLET = pygame.image.load('png/BASICBULLET.png')
STONE_BULLET = pygame.image.load('png/STONE_BULLET.png')
HEART = pygame.image.load('png/HEART.png')
HEART_PICKED = pygame.image.load('png/HEART_PICKED.png')

STRONG_CARD = pygame.image.load('png/STRONGCARD.png')
STRONG_CARD_PICKED = pygame.image.load('png/STRONGCARDPICKED.png')
DOORS_KEY_PICKED = pygame.image.load('png/DOORSKEYPICKED.png')
DOORS_UP = pygame.image.load('png/DOOR_UP.png')
DOORS_DOWN = pygame.image.load('png/DOOR_DOWN.png')
DOORS_UP_OPEN = pygame.image.load('png/DOOR_UP_OPEN.png')
DOORS_DOWN_OPEN = pygame.image.load('png/DOOR_DOWN_OPEN.png')
BOSS_DOORS = pygame.image.load('png/BOSS_DOORS.png')
BOSS_DOORS_OPEN = pygame.image.load('png/BOSS_DOORS_OPEN.png')
BOOS_DOORS_DOWN = pygame.image.load('png/BOSS_DOORS_DOWN.png')

POOP = [POOP_1, POOP_2, POOP_3, POOP_4, POOP_5]
POOP_1 = POOP[0]
POOP_6 = pygame.image.load('png/POOP_6.png')
#grafika przeciwnika
RED_START = RED_D1
RED_R = [RED_R1, RED_R2, RED_R3, RED_R4]
RED_L = [RED_L1, RED_L2, RED_L3, RED_L4]
RED_D = [RED_D1, RED_D2, RED_D3, RED_D4]
RED_U = [RED_U1, RED_U2, RED_U3, RED_U4]
RED_DEADL = RED_DEADL
RED_DEADR = RED_DEADR

DEVIL_START = DEVIL_D1
DEVIL_R = [DEVIL_R1, DEVIL_R2, DEVIL_R3, DEVIL_R4, DEVIL_R5]
DEVIL_L = [DEVIL_L1, DEVIL_L2, DEVIL_L3, DEVIL_L4, DEVIL_L5]
DEVIL_D = [DEVIL_D1, DEVIL_D2, DEVIL_D3, DEVIL_D4, DEVIL_D5]
DEVIL_U = [DEVIL_U1, DEVIL_U2, DEVIL_U3, DEVIL_U4, DEVIL_U5]
DEVIL_DEADL = DEVIL_DEADL
DEVIL_DEADR = DEVIL_DEADR

BOSS_START = BOSS_D1
BOSS_R = [BOSS_R1, BOSS_R2, BOSS_R3, BOSS_R3]
BOSS_L = [BOSS_L1, BOSS_L2, BOSS_L3, BOSS_L3]
BOSS_D = [BOSS_D1, BOSS_D2, BOSS_D3, BOSS_D3]
BOSS_U = [BOSS_U1, BOSS_U2, BOSS_U3, BOSS_U3]
BOSS_DEAD =  pygame.image.load('png/BOSS_DEAD.png')

#grafika kolców
SPIKES = [SPIKES_1, SPIKES_2, SPIKES_3, SPIKES_4, SPIKES_5]

#grafika skały
ROCK = pygame.image.load('png/ROCK.png')
#klucz do drzwi
DOOR_KEY = pygame.image.load('png/DOOR_KEY.png')

#bomba i wybuch
BOMB = pygame.image.load('png/BOMB_1.png')
EXPLOSION = [BOMB_2, BOMB_3, BOMB_4, BOOM_11, BOOM_22, BOOM_33, BOOM_44, BOOM_55]
BOMB_PICKED = pygame.image.load('png/BOMB_PICKED.png')

#Tower
TOWER = pygame.image.load('png/TOWER_1.png')

#hitbox defines
hitbox = pygame.image.load('png/hitbox2.png')
hitbox = pygame.transform.scale(hitbox, (40, 40))
hitbox_sprite = pygame.sprite.Sprite()
hitbox_sprite.image = hitbox
hitbox_sprite.rect = hitbox_sprite.image.get_rect()

