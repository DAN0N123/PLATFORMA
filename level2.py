import pygame
from main_objects import make_floor, Player, projectile, Button
won = False
lost = False
projectiles_list = []
last_action_time1 = 0
last_action_time2 = 0
time = 45

button = None
window_width = 1536
window_height = 864

player = None

played_sound = False
projectile_pool = [projectile(5, "zdjęcia/jedynka.png") for _ in range(20)]

def reset_level_2():
    global won
    global lost
    global projectile_pool
    global time
    won, lost = False, False
    for item in reversed(projectiles_list):
        item.update_angle()
        item.reset()
        projectile_pool.append(projectiles_list.pop(len(projectiles_list) - 1))
    time = 45
    player.reset_position()
    
    

def add_projectile():
    global projectiles_list
    global last_action_time2

    new_projectile = projectile_pool.pop()
    new_projectile.reset() 
    projectiles_list.append(new_projectile)
    new_projectile.index = len(projectiles_list) - 1
init_reset = False
def level_two(screen, current_tick, event, my_player: Player):
    global init_reset
    global projectiles_list
    global last_action_time1
    global last_action_time2
    global won 
    global lost
    global projectile_pool
    global player
    global time
    player = my_player
    player.canjump = True
    player.autojump = False
    player.jump_height = 20
    if current_tick - last_action_time1 >= 1000:
            time -= 1
            if time == 0:
                 won = True
            last_action_time1 = current_tick
    if not init_reset:
        player.reset_position()
        init_reset = True
    if not won and not lost:
        screen.fill((89, 201, 250))
        clock_font = pygame.font.Font("arialbd.ttf", 45)
        clock_text = clock_font.render(f"Do końca lekcji: {str(time)}", True, (0,0,0))
        clock_rect = clock_text.get_rect(center = (240, 60))
        screen.blit(clock_text, clock_rect)

        gonda = pygame.image.load("zdjęcia/gonda2.png")
        gonda_resized = pygame.transform.scale(gonda, (200,200))
        gonda_rect = gonda_resized.get_rect(center = (768, 90))
        screen.blit(gonda_resized, gonda_rect)

        my_player.movement()
        my_player.draw(screen)
        make_floor(screen)
        if current_tick - last_action_time2 >= 300:
                add_projectile()
                last_action_time2 = current_tick
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
    if won:
        global played_sound
        if not played_sound:
            pygame.mixer.music.load('win.wav')  
            pygame.mixer.music.play(loops=1)
            played_sound = True
        screen.fill((89, 201, 250)) 
        sala = pygame.image.load("zdjęcia/sala.jpg")
        sala_resized = pygame.transform.scale(sala, (1536,864))
        screen.blit(sala_resized, (0,0))
        box_font = pygame.font.Font("arialbd.ttf", 45)
        box_text = box_font.render("", True, (0,0,0), (255,255,255))

        outline_rect = pygame.Rect((0,0, box_text.get_width() + 6, box_text.get_height() + 6))
        outline_rect.center = (768,150)
        pygame.draw.rect(screen, (0,0,0), outline_rect)

        box_rect = box_text.get_rect(center=(768, 150))
        screen.blit(box_text, box_rect)
        button_width = 300
        button_height = 100
        level_2_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Przejdź dalej", (251,251,251), box_font, (0,0,0), 3, event)
        button_outline = pygame.Rect((window_width - button_width) // 2 - 3, 497, button_width + 6, button_height + 6)
        pygame.draw.rect(screen, (0,0,0), button_outline)
        level_2_button.draw(screen)
        return level_2_button

def lost_screen(screen):     
    if lost:
        screen.fill((89,201,250))
        box_font = pygame.font.Font("arialbd.ttf", 70)
        button_font = pygame.font.Font("arialbd.ttf", 35)
        box_text = box_font.render("No i pizda", True, (255,0,0), (89, 201, 250))
        box_rect = box_text.get_rect(center = (788, 160))
        screen.blit(box_text, box_rect)
        button_width = 500
        button_height = 100
        restart_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Spróbuj ponownie", (251,251,251), button_font, (0,0,0), None, reset_level_2)
        button_outline = pygame.Rect((window_width - button_width) // 2 - 3, 497, button_width + 6, button_height + 6)
        pygame.draw.rect(screen, (0,0,0), button_outline)
        restart_button.draw(screen)
        return restart_button

def return_button(event):
     button_width = 500
     button_height = 100
     button_font = pygame.font.Font("arialbd.ttf", 45)
     if lost:
        restart_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Spróbuj ponownie", (251,251,251), button_font, (0,0,0), None, reset_level_2)
        return restart_button
     if won:
        level_2_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Przejdź dalej", (251,251,251), button_font, (0,0,0), 4, event)
        return level_2_button



        


        

