import pygame

maślana_sprite = pygame.image.load("zdjęcia/nobackgroundluffysprite.png")
maślana_sprite_scaled = pygame.transform.scale(maślana_sprite, (250,250))
dialogue_box =  pygame.image.load("zdjęcia/dialoguebox.png")
dialogue_box_scaled = pygame.transform.scale(dialogue_box, (500,500))
dziewczynki_sprite_scaled = pygame.transform.scale(maślana_sprite, (150,150))

redlight = pygame.image.load("zdjęcia/redlight.png")
yellowlight = pygame.image.load("zdjęcia/yellowlight.png")
greenlight = pygame.image.load("zdjęcia/greenlight.png")


white = (255, 255, 255)
green = (83,141,78)
blue = (89, 201, 250)
red = (255,0,0)
black = (0,0,0)
yellow = (181,159,60)
gray = (80,80,80)
last_action_time_typing = 0
check = True
delta = None
started = False
photo = 0
def check(screen):
    screen.fill((251,251,251))
    x = 100
    y = 600
    screen.blit(maślana_sprite_scaled, (x, y))
    screen.blit(dialogue_box_scaled, (x + 250, y - 300))
    screen.blit(dziewczynki_sprite_scaled, (1300, 50))
def countdown(screen, current_time):
    screen.fill((251,251,251))
    global check
    global photo
    global last_action_time_typing
    global delta
    global started
    photos = [redlight, yellowlight, greenlight]
    current_photo = photos[photo]
    if check:
        pygame.mixer.music.load('dźwięk.mp3') 
        pygame.mixer.music.play(loops=1)
        delta = current_time
        check = False
    
    if (current_time - delta) - last_action_time_typing >= 1000:
        if photo < 2:
            pygame.mixer.music.load('dźwięk.mp3') 
            pygame.mixer.music.play(loops=1)
            photo += 1
            last_action_time_typing = current_time - delta
        else:
            pygame.mixer.music.load('dźwięk2.mp3') 
            pygame.mixer.music.play(loops=1)
            started = True

    
    font = pygame.font.Font("arialbd.ttf", 40)
    get_ready_text = font.render("Przygotuj się", True, black)
    get_ready_text_rect = get_ready_text.get_rect()
    get_ready_text_rect.center = (768, 70)
    screen.blit(get_ready_text, get_ready_text_rect)
    print(photos[0].get_size())
    screen.blit(current_photo, (448,150))
def typing(screen, current_time):
    global started
    if not started:
        countdown(screen, current_time)


def level_five(screen, current_time, event = None):
    typing(screen, current_time)


