from main_objects import platform_object, game_object, Player 
import sys
import pygame



def level_one(screen, platforms, floor, my_player):
    screen.fill((89, 201, 250)) 

    current_time = pygame.time.get_ticks()
    
    floor.draw(screen)
    my_player.draw(screen)
    my_player.movement()
    my_player.hitbox.x = my_player.x
    my_player.hitbox.y = my_player.y 
    

    for a_platform in platforms:
        a_platform.draw(screen)
        if my_player.collision_with_platform(a_platform) and my_player.fallingdown:
            my_player.onplatform = True
            my_player.fallingdown = False
            my_player.jump_height = 30 
            my_player.y = a_platform.y - my_player.height
            my_player.jumping = False
            my_player.jump_velocity = 0

    my_player.onplatform = my_player.check_if_on_platform(platforms)
    if not my_player.onplatform and my_player.y < 664:
        my_player.jump_height = 0
        my_player.jumping = True

    if my_player.y >= 664:
        my_player.jump_height = 30
        my_player.y = 664
        my_player.jumping = False