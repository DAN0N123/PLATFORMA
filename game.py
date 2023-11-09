import pygame
import sys
from main_objects import game_object, platform_object, Player, Button
from startscreen import start_screen
from level1 import level_one


pygame.init()

window_width = 1536
window_height = 864

screen = pygame.display.set_mode((window_width,window_height))
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
player_sprite = pygame.image.load("nobackgroundluffysprite.png")
player_sprite_scaled = pygame.transform.scale(player_sprite, (100,100))
start_image = pygame.image.load("start.jpg")
start_image_scaled = pygame.transform.scale(start_image, (1536,864))

which_level = 0
last_action_time = 0


def setlevel(level):
    global which_level
    which_level = level


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

    if current_time - last_action_time >= 800:
        force = 'jump'
        my_player.movement(force)
        last_action_time = current_time

    match which_level:
        case 0:
            my_button = start_screen(screen,window_width, window_height, start_image, setlevel)
        case 1:
            from level1 import platform_object
            platforms = []
            platforms.append(platform_object(1000, 440, 200, 20, black))
            platforms.append(platform_object(200, 600, 300, 20, black))
            level_one(screen, platforms, floor, my_player)
    
    clock.tick(120)
    pygame.display.flip()

    
pygame.quit()
sys.exit()