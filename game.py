import pygame
import sys
from main_objects import game_object, platform_object, Player
from level1 import level_one

pygame.init()

window_width = 1536
window_height = 864

screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("ŚWIRKI")



running = True
clock = pygame.time.Clock()

is_gravity = True

white = (255, 255, 255)
green = (83,141,78)
blue = (89, 201, 250)
red = (255,0,0)
black = (0,0,0)
yellow = (181,159,60)
gray = (80,80,80)

player_sprite = pygame.image.load("nobackgroundluffysprite.png")
player_sprite_scaled = pygame.transform.scale(player_sprite, (100,100))

which_level = 1
last_action_time = 0

my_player = Player(player_sprite_scaled, window_width, window_height)    
floor = game_object(0, 751, 1536, 200, yellow)

if which_level == 1:
    from level1 import platform_object
    platforms = []
    platforms.append(platform_object(1000, 440, 200, 20, black))
    platforms.append(platform_object(200, 600, 300, 20, black))




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    match which_level:
        
        case 1:
            level_one(screen, platforms, floor, my_player)
    
    clock.tick(144)
    pygame.display.flip()

    
pygame.quit()
sys.exit()