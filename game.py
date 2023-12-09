import pygame
import sys
import os
from main_objects import game_object,Player
from startscreen import start_screen
from level1 import level_one
from level2 import level_two, lost_screen, return_button
from level3 import level_three
from level4 import level_four
from level5 import level_five
from level6 import level_six
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
window_width = 1536
window_height = 864

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("ŚWIRKI")

running = True
clock = pygame.time.Clock()

my_button = None

is_gravity = True

white = (255, 255, 255)
green = (83,141,78)
blue = (89, 201, 250)
red = (255,0,0)
black = (0,0,0)
yellow = (181,159,60)
gray = (80,80,80)

#zdjęcia
player_sprite = pygame.image.load("zdjęcia/nobackgroundluffysprite.png")
player_sprite_scaled = pygame.transform.scale(player_sprite, (100,100))
start_image = pygame.image.load("zdjęcia/start.jpg")
start_image_scaled = pygame.transform.scale(start_image, (1536,864))


last_action_time = 0
which_level = 1

def setlevel(level):
    global which_level
    which_level = level
def center_screen():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((pygame.display.Info().current_w - window_width) // 2,
                                                     (pygame.display.Info().current_h - window_height) // 2)
def recreate_screen(window_width1, window_height1):
    global screen, width, height
    pygame.quit()

    width, height = window_width1, window_height1
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("ŚWIRKI")
    
    center_screen()

    pygame.init()
my_player = Player(player_sprite_scaled, window_width, window_height)
floor = game_object(0, 751, 1536, 200, yellow)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if my_button and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if my_button.rect.collidepoint(event.pos):
                my_button.handle_event(event)
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    match which_level:
        case 0:
            my_button = start_screen(screen,window_width, window_height, start_image, setlevel)
        case 1:
            my_button = level_one(screen, floor, my_player, setlevel)
        case 2:
            lost_screen(screen)
            level_two(screen, current_time, setlevel, my_player)
            my_button = return_button(setlevel)
        case 3:
            level_three(screen, setlevel, my_player)
        case 4:
            my_button = level_four(screen, keys, current_time, setlevel)
        case 5:
            level_five(screen, current_time, setlevel)
        case 6:
            if pygame.display.Info().current_w != 1000:
                recreate_screen(1000,1000)
            level_six(screen, current_time, keys, setlevel)
    clock.tick(75)
    pygame.display.flip()

    
pygame.quit()
sys.exit()