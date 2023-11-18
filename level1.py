from main_objects import game_object, Player, scale_image 
import sys
import pygame
import random


level = 1
#zdjęcia
floor_image= pygame.image.load("zdjęcia/podłoga.png")
floor_image_scaled = pygame.transform.scale(floor_image, (150,200))

platform_image = pygame.image.load("zdjęcia/platforma.png")
platform_image_scaled = pygame.transform.scale(platform_image, (200,40))

rangi = []
bronze_image = pygame.image.load("zdjęcia/bronze.webp")
silver_image = pygame.image.load("zdjęcia/silver.webp")
gold_image = pygame.image.load("zdjęcia/gold.webp")
platinum_image = pygame.image.load("zdjęcia/platyna.webp")
diamond_image = pygame.image.load("zdjęcia/diament.webp")
champ_image = pygame.image.load("zdjęcia/champ.webp")
gc_image = pygame.image.load("zdjęcia/gc.webp")
ssl_image = pygame.image.load("zdjęcia/ssl.webp")
rangi.append(bronze_image)
rangi.append(silver_image)
rangi.append(gold_image)
rangi.append(platinum_image)
rangi.append(diamond_image)
rangi.append(champ_image)
rangi.append(gc_image)
rangi.append(ssl_image)

for index, item in enumerate(rangi):
    scaled = scale_image(item, (100,100))
    rangi.pop(index)
    rangi.insert(index,scaled)

def new_rank(screen, ranks, current_level, platforms):
    if current_level % 5 == 0:
        ranga = ranks[current_level // 5 - 1]
        middle_platform_index = current_level * 3 - 2
        height = platforms[middle_platform_index].height
        width = platforms[middle_platform_index].width
        x = platforms[middle_platform_index].x + ((width - 100) // 2)
        y = platforms[middle_platform_index].y
        
        screen.blit(ranga, (x,y - 100))

def create_platform():
    platforms = []
    for i in range(0,200):
        x = random.randint(500,1036)
        y = 100
        yo = game_object(x, y, 200, 20, (0,0,0), platform_image_scaled)
        platforms.append(yo)
        for i in range(1,3):
                y = i * 350
                x = random.randint(500,1036)
                yo = game_object(x, y, 200, 20, (0,0,0), platform_image_scaled)
                platforms.append(yo)
    return platforms

def make_floor(screen, floor_image):
    for i in range(0,11):
        screen.blit(floor_image, (150*i, 751))

platforms = create_platform()
def level_one(screen, floor, my_player: Player):
    global level
    global platforms
    screen.fill((89, 201, 250)) 
    
    new_rank(screen, rangi, level, platforms)

    floor.draw(screen)
    my_player.draw(screen)
    my_player.movement()
    my_player.hitbox.x = my_player.x
    my_player.hitbox.y = my_player.y 
    if level != 1:
        my_player.aboveground = True
        floor.color = (89, 201, 250)
    else:
        my_player.aboveground = False
        floor.color = (181,159,60)
        make_floor(screen, floor_image_scaled)

    if my_player.aboveground and my_player.y + my_player.height >= 864:
        my_player.y = 20
        level -= 1
        
    if my_player.y <= -10 - my_player.height:
        my_player.y = 844 - my_player.height
        my_player.fallingdown = True
        level += 1

    start = level * 3 - 3
    end = level * 3
    for a_platform in platforms[start:end]:
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
    