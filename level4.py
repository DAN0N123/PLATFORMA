from main_objects import Note, Note_Box, Player, Button
import pygame
import random

pygame.init()
window_width = 1536
window_height = 864
test_note = Note(1)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("ŚWIRKI")
player_sprite = pygame.image.load("zdjęcia/nobackgroundluffysprite.png")
player_sprite_scaled = pygame.transform.scale(player_sprite, (100,100))
my_player = Player(player_sprite_scaled, window_width, window_height)    

init_jasper = pygame.image.load("zdjęcia/jasper.webp")
jasper = pygame.transform.scale(init_jasper, (300,200))

radio_off = True

yellow = (246, 253, 2)
red = (218, 0, 19)
blue = (2, 67, 185)
green = (22, 206, 68)


background_color = (13, 17, 23)
running = True
clock = pygame.time.Clock()

pool_one = [Note(0) for _ in range(10)]
pool_two = [Note(1) for _ in range(10)]
pool_three = [Note(2) for _ in range(10)]
pool_four = [Note(3) for _ in range(10)]

last_action_time = 0
current_notes = []

note_box_y = 780
note_boxes = [Note_Box(green, 0, note_box_y), Note_Box(red, 0, note_box_y), Note_Box(yellow, 0, note_box_y), Note_Box(blue, 0, note_box_y)]

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.load('DAWIDŚPIEWA.mp3')  

total_notes = 0
perfect_notes = 0
def level_four(screen, my_player, event = None):
    global last_action_time
    global last_action_time2
    global radio_off
    screen.fill(background_color)
    current_time = pygame.time.get_ticks()
    if current_time < 125000:
        for i in range(0,4):
            x = ((1536 - 4 * (test_note.gap + test_note.width)) // 2 + (test_note.width // 2)) + ((test_note.gap + test_note.width)*i)
            note_boxes[i].x = x
            pygame.draw.line(screen, (251,251,251), (x, 0), (x, 864), 7)

        for i in note_boxes:
            i.draw(screen)
        
        if current_time >= 700 and radio_off:
            pygame.mixer.music.play(loops=1)
            radio_off = False
        if current_time < 114000:
            if current_time - last_action_time >= 339:
                global total_notes
                branch = random.randint(0,4)
                match branch:
                    case 0:
                        temp_note = pool_one.pop()
                        current_notes.append(temp_note)
                        total_notes += 1
                    case 1:
                        temp_note = pool_two.pop()
                        current_notes.append(temp_note)
                        total_notes += 1
                    case 2:
                        temp_note = pool_three.pop()
                        current_notes.append(temp_note)
                        total_notes += 1
                    case 3:
                        temp_note = pool_four.pop()
                        current_notes.append(temp_note)
                        total_notes += 1
                last_action_time = current_time
        for note in current_notes:
            note.falling()
            note.draw(screen)
        for index, note in enumerate(current_notes):
            if note.y > 864:
                # if note.played == False:
                    #play sound
                temp_note = current_notes.pop(index)
                temp_note.reset()
                branch = temp_note.branch
                match branch:
                    case 0:
                        pool_one.append(temp_note)
                    case 1:
                        pool_two.append(temp_note)
                    case 2:
                        pool_three.append(temp_note)
                    case 3:
                        pool_four.append(temp_note)
        global perfect_notes
        if total_notes > 0:
            percentage_font = pygame.font.Font("arialbd.ttf", 45)
            percentage_text = percentage_font.render(f"{round((perfect_notes / total_notes) * 100, 2)} %", True, (251,251,251), background_color)
            percentage_rect = percentage_text.get_rect(center = (1250, 500))
            print(total_notes, perfect_notes)
            screen.blit(percentage_text, percentage_rect)
    else:
        screen.blit(jasper, (1200, 100))
        screen.fill(background_color)
        box_font = pygame.font.Font("arialbd.ttf", 70)
        button_font = pygame.font.Font("arialbd.ttf", 35)
        box_text = box_font.render("Koniec", True, (255,0,0), background_color)
        box_rect = box_text.get_rect(center = (788, 160))
        screen.blit(box_text, box_rect)
        button_width = 500
        button_height = 100
        restart_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Przejdź dalej", (251,251,251), button_font, (0,0,0), None, event)
        button_outline = pygame.Rect((window_width - button_width) // 2 - 3, 497, button_width + 6, button_height + 6)
        pygame.draw.rect(screen, (0,0,0), button_outline)
        restart_button.draw(screen)
    

def check_note(button):
    global perfect_notes
    match button:
        case 1:
            for i in current_notes:
                if i.branch == 0 and i.y in range(770, 780 + (120-i.height)):
                    if i.played == False:
                        perfect_notes += 1
                    i.played = True
        case 2:
            for i in current_notes:
                if i.branch == 1 and i.y in range(770, 780 + (120-i.height)):
                    if i.played == False:
                        perfect_notes += 1
                    i.played = True
        case 3:
            for i in current_notes:
                if i.branch == 2 and i.y in range(770, 780 + (120-i.height)):
                    if i.played == False:
                        perfect_notes += 1
                    i.played = True
        case 4:
            for i in current_notes:
                if i.branch == 3 and i.y in range(770, 780 + (120-i.height)):
                    if i.played == False:
                        perfect_notes += 1
                    i.played = True
        
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
        
        
       
        
    
    if keys[pygame.K_1] and not clicking2 and not clicking3 and not clicking4:
        clicking1 = True
        check_note(1)
        note_boxes[0].pulsating = True
    else:
        clicking1 = False
        note_boxes[0].pulsating = False

    if keys[pygame.K_2] and not clicking1 and not clicking3 and not clicking4:
        clicking2 = True
        check_note(2)
        note_boxes[1].pulsating = True
    else:
        clicking2 = False
        note_boxes[1].pulsating = False

    if keys[pygame.K_3] and not clicking2 and not clicking1 and not clicking4:
        clicking3 = True
        check_note(3)
        note_boxes[2].pulsating = True
    else:
        clicking3 = False
        note_boxes[2].pulsating = False

    if keys[pygame.K_4] and not clicking1 and not clicking2 and not clicking3:
        clicking4 = True
        check_note(4)
        note_boxes[3].pulsating = True
    else:
        clicking4 = False
        note_boxes[3].pulsating = False
    level_four(screen, my_player)
    clock.tick(75)
    pygame.display.flip()