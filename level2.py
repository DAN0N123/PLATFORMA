import pygame
from main_objects import make_floor, Player, projectile, Button
import random
won = False
lost = False
projectiles_list = []
last_action_time = 0

window_width = 1536
window_height = 864

player = None

projectile_pool = [projectile(5, "zdjęcia/jedynka.png") for _ in range(20)]

def reset_level_2():
    global won
    global lost
    global projectile_pool
    won, lost = False, False
    for item in reversed(projectiles_list):
        item.update_angle()
        item.reset()
        projectile_pool.append(projectiles_list.pop(len(projectiles_list) - 1))

    player.reset_position()
    
    

def add_projectile():
    global projectiles_list
    global last_action_time

    new_projectile = projectile_pool.pop()
    new_projectile.reset() 
    projectiles_list.append(new_projectile)
    new_projectile.index = len(projectiles_list) - 1

def level_two(screen, current_time, my_player: Player):
    global projectiles_list
    global last_action_time
    global won 
    global lost
    global projectile_pool
    global player
    player = my_player

    if not won and not lost:
        screen.fill((89, 201, 250))
        my_player.movement(False)
        my_player.draw(screen)
        make_floor(screen)
        if current_time - last_action_time >= 300:
                add_projectile()
                last_action_time = current_time
        to_remove = []
        for a_projectile in projectiles_list:
            a_projectile.movement()
            a_projectile.update_hitbox()
            a_projectile.draw(screen)
            if a_projectile.check_collision(my_player.hitbox):
                lost = True
            if a_projectile.out_of_screen():
                to_remove.append(a_projectile.index)

        for index in reversed(to_remove):
            the_projectile = projectiles_list.pop(index)
            the_projectile.update_angle()
            projectile_pool.append(the_projectile)
            
        for index, item in enumerate(projectiles_list):
            item.index = index

def lost_screen(screen):       
    if lost:
        screen.fill((89,201,250))
        box_font = pygame.font.Font("arialbd.ttf", 70)
        button_font = pygame.font.Font("arialbd.ttf", 35)
        box_text = box_font.render("No i pizda", True, (255,0,0), (89, 201, 250))
        box_rect = box_text.get_rect(center = (768, 160))
        screen.blit(box_text, box_rect)
        button_width = 500
        button_height = 100
        restart_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Spróbuj ponownie", (251,251,251), button_font, (0,0,0), None, reset_level_2)
        button_outline = pygame.Rect((window_width - button_width) // 2 - 3, 497, button_width + 6, button_height + 6)
        pygame.draw.rect(screen, (0,0,0), button_outline)
        restart_button.draw(screen)
        return restart_button
    else:
        return None

        


        

