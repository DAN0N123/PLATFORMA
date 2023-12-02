from main_objects import game_object, Player, scale_image, Button, make_floor
import sys
import pygame
import random


level = 1
window_width = 1536
window_height = 864


#zdjęcia


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


def new_rank(screen, ranks, current_level, platforms, ktore_levele):
        if current_level in ktore_levele and current_level <= 140:
            ranga = ranks[current_level // 20]
            middle_platform_index = current_level * 3 - 2
            width = platforms[middle_platform_index].width
            x = platforms[middle_platform_index].x + ((width - 100) // 2)
            y = platforms[middle_platform_index].y - 100
            pickup_rect = pygame.Rect(x,y, 100, 100)
            screen.blit(ranga, pickup_rect)
            return pickup_rect
        


def create_platform():
    platforms = []
    for i in range(0,140):
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



platforms = create_platform()
ktore_levele = [20,40,60,80,100,120,140]

def level_one(screen,floor, my_player, event):
    global level
    global platforms
    global ktore_levele
    my_player.autojump = True
    if my_player.rank != 7: 
        screen.fill((89, 201, 250)) 
        floor.draw(screen)
        my_player.movement()
        my_player.hitbox.x = my_player.x
        my_player.hitbox.y = my_player.y 
        my_player.currentrank = new_rank(screen, rangi, level, platforms, ktore_levele)

        ktore_levele = my_player.rankup(ktore_levele)
        my_player.show_rank(rangi, screen)

        if level != 1:
            my_player.aboveground = True
            floor.color = (89, 201, 250)
        else:
            my_player.aboveground = False
            floor.color = (181,159,60)
            make_floor(screen)

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
        my_player.draw(screen)

        my_player.onplatform = my_player.check_if_on_platform(platforms)

        if not my_player.onplatform and my_player.y < 664:
            my_player.jump_height = 0
            my_player.jumping = True

        if my_player.y >= 664 and not my_player.aboveground:
            my_player.jump_height = 30
            my_player.y = 664
            my_player.jumping = False
    else:
        screen.fill((89, 201, 250)) 
        box_font = pygame.font.Font("arialbd.ttf", 45)
        box_text = box_font.render("Witek zdobył SSl! Możesz przejść do następnego poziomu.", True, (0,0,0), (89, 201, 250))
        box_rect = box_text.get_rect(center = (768, 80))
        ssl_rect = pygame.Rect((window_width - 316) // 2, 125, 100,100)
        screen.blit(box_text, box_rect)
        screen.blit(ssl_image, ssl_rect)
        button_width = 300
        button_height = 100
        level_1_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Przejdź dalej", (251,251,251), box_font, (0,0,0), 2, event)
        button_outline = pygame.Rect((window_width - button_width) // 2 - 3, 497, button_width + 6, button_height + 6)
        pygame.draw.rect(screen, (0,0,0), button_outline)
        level_1_button.draw(screen)
        return level_1_button
            
