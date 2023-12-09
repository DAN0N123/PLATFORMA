from main_objects import Note, Note_Box, Player, Button
import pygame
import random



test_note = Note(1)
init_jasper = pygame.image.load("zdjęcia/jasper.webp")
jasper = pygame.transform.scale(init_jasper, (300,200))
my_button = None
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

total_notes = 0
perfect_notes = 0
tries = 1
clicking1 = False
clicking2 = False
clicking3 = False
clicking4 = False

check = True
delta = None
def level_four(screen, keys, current_time, event = None):
    global last_action_time
    global radio_off
    global clicking1
    global clicking2
    global clicking3
    global clicking4
    global check
    global my_button
    screen.fill(background_color)
    if check:
        global delta
        delta = current_time
        check = False
    if current_time - delta < 125000:
        for i in range(0,4):
            x = ((1536 - 4 * (test_note.gap + test_note.width)) // 2 + (test_note.width // 2)) + ((test_note.gap + test_note.width)*i)
            note_boxes[i].x = x
            pygame.draw.line(screen, (251,251,251), (x, 0), (x, 864), 7)

        for i in note_boxes:
            i.draw(screen)
        
        if current_time - delta >= 700 and radio_off:
            pygame.mixer.music.load('DAWIDŚPIEWA.mp3') 
            pygame.mixer.music.play(loops=1)
            radio_off = False
        if current_time - delta < 114000:
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
        global perfect_notes
        if total_notes > 0:
            percentage_font = pygame.font.Font("arialbd.ttf", 45)
            percentage_text = percentage_font.render(f"{round((perfect_notes / total_notes) * 100, 2)} %", True, (251,251,251), background_color)
            percentage_rect = percentage_text.get_rect(center = (1250, 500))
            screen.blit(percentage_text, percentage_rect)
    else:
        end_screen(event, screen)
        return my_button

def reset_level_4():
    global total_notes
    global perfect_notes
    global tries
    global radio_off
    global delta
    global check
    total_notes = 0
    perfect_notes = 0
    tries += 1
    radio_off = True
    delta = None
    check = True

def end_screen(event, screen):
    global my_button
    pygame.mixer.music.stop()
    pygame.mixer.music.rewind()
    window_width = 1536
    if total_notes > 0:
        if (perfect_notes / total_notes) > 0.60:
            screen.blit(jasper, (1200, 100))
            screen.fill(background_color)
            box_font = pygame.font.Font("arialbd.ttf", 70)
            button_font = pygame.font.Font("arialbd.ttf", 35)
            box_text = box_font.render("Wygrana!", True, (255,0,0), background_color)
            box_rect = box_text.get_rect(center = (788, 160))
            screen.blit(box_text, box_rect)
            button_width = 500
            button_height = 100
            restart_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Przejdź dalej", (251,251,251), button_font, (0,0,0), 5, event)
            button_outline = pygame.Rect((window_width - button_width) // 2 - 3, 497, button_width + 6, button_height + 6)
            pygame.draw.rect(screen, (0,0,0), button_outline)
            restart_button.draw(screen)
            my_button = restart_button
        else:
            screen.blit(jasper, (1200, 100))
            screen.fill(background_color)
            box_font = pygame.font.Font("arialbd.ttf", 70)
            button_font = pygame.font.Font("arialbd.ttf", 35)
            box_text = box_font.render("Przegrałeś", True, (255,0,0), background_color)
            box_rect = box_text.get_rect(center = (788, 160))
            screen.blit(box_text, box_rect)
            button_width = 500
            button_height = 100
            restart_button = Button((window_width - button_width) // 2, 500, button_width, button_height, "Spróbuj ponownie", (251,251,251), button_font, (0,0,0), None, reset_level_4)
            button_outline = pygame.Rect((window_width - button_width) // 2 - 3, 497, button_width + 6, button_height + 6)
            pygame.draw.rect(screen, (0,0,0), button_outline)
            restart_button.draw(screen)
            my_button = restart_button

def check_note(button):
    global perfect_notes
    for index, note in enumerate(current_notes):
                if note.branch == (button - 1) and note.y in range(770, 780 + (120-note.height)):
                    if note.played == False:
                        perfect_notes += 1
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
                    note.played = True