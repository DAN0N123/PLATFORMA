import pygame
import random
import os
from main_objects import popup

mświerczyński_sprite = pygame.image.load("zdjęcia/nobackgroundluffysprite.png")
mświerczyński_sprite_scaled = pygame.transform.scale(mświerczyński_sprite, (250,250))
piątkowcy_sprite_scaled = pygame.transform.scale(mświerczyński_sprite, (100,100))
last_action_time = 0
last_action_time2 = 0
how_often = 1000

delta = None
check = True
window_width1 = 1000
window_height1 = 1000
photos = [popup(piątkowcy_sprite_scaled, 1, 1000, 1000), popup(piątkowcy_sprite_scaled, 2, 1000, 1000), popup(piątkowcy_sprite_scaled, 3, 1000, 1000), popup(piątkowcy_sprite_scaled, 4, 1000, 1000)]

init_window_width = 1536
init_window_height = 864

def level_six(screen, current_time, keys, event):
    global how_often, photos, last_action_time, last_action_time2, delta, check
    if how_often > 400:
        screen.fill((251,251,251))
        (tempx,tempy) = mświerczyński_sprite_scaled.get_size()
        screen.blit(mświerczyński_sprite_scaled, ((window_width1 - tempx) // 2, (window_height1 - tempy) // 2))
        if check:
            delta = current_time
            check = False
        available_photos = [1,2,3,4]
        if (current_time - delta) - last_action_time >= how_often:
            if len(available_photos) > 0:
                location = random.choice(available_photos)
                (tempx,tempy) = piątkowcy_sprite_scaled.get_size()
                photos[location - 1].todraw = True
                photos[location - 1].starting_time = current_time
                photos[location - 1].duration = how_often + (how_often // 2)
                available_photos.pop(location - 1)
            last_action_time = current_time - delta
        if (current_time - delta) - last_action_time2 >= 1000:
            how_often -= 25
            last_action_time2 = current_time - delta
        for index, image in enumerate(photos):
            image.draw(screen)
            image.check_time(current_time)
            if not image.todraw:
                available_photos.insert(index, index + 1)
        if keys[pygame.K_LEFT]:
            if photos[0].todraw:
                photos[0].todraw = False
                pygame.mixer.music.load("piąteczka.mp3")
                pygame.mixer.music.play(loops=1)
        if keys[pygame.K_UP]:
            if photos[1].todraw:
                photos[1].todraw = False
                pygame.mixer.music.load("piąteczka.mp3")
                pygame.mixer.music.play(loops=1)
        if keys[pygame.K_RIGHT]:
            if photos[2].todraw:
                photos[2].todraw = False
                pygame.mixer.music.load("piąteczka.mp3")
                pygame.mixer.music.play(loops=1)
        if keys[pygame.K_DOWN]:
            if photos[3].todraw:
                photos[3].todraw = False
                pygame.mixer.music.load("piąteczka.mp3")
                pygame.mixer.music.play(loops=1)
            



    
