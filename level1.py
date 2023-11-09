from main_objects import platform_object, game_object, Player 
import sys
import pygame
import random

def create_platform(list_of_platforms: list, y):
    if len(list_of_platforms) < 3:
        x = random.randint(500,1036)
        yo = platform_object(x, y, 200, 20, (0,0,0))
        list_of_platforms.append(yo)


def level_one(screen, floor, my_player: Player, platforms: list):
    screen.fill((89, 201, 250)) 

    for i in range(-1,2):
        y = i * 300
        create_platform(platforms, y)

    floor.draw(screen)
    my_player.draw(screen)
    my_player.movement()
    my_player.hitbox.x = my_player.x
    my_player.hitbox.y = my_player.y 

    if my_player.aboveground and my_player.y + my_player.height >= 864:
        my_player.y = 20
        my_player.aboveground = False
        for i in range(-1,3):
            platforms.pop(0)
            if i < 3:
                y = i * 300
                create_platform(platforms, y)
        floor.color = (181,159,60)
    if my_player.y <= -10 - my_player.height:
        my_player.y = 844 - my_player.height
        my_player.fallingdown = True
        my_player.aboveground = True
        floor.color = (89, 201, 250)
        for i in range(-1,3):
            platforms.pop(0)
            y = i * 400
            create_platform(platforms, y)
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

    if my_player.y >= 664 and not my_player.aboveground:
        my_player.jump_height = 30
        my_player.y = 664
        my_player.jumping = False
    return platforms