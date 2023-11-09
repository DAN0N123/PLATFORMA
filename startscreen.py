from main_objects import Button
import pygame

def start_screen(screen, window_width, window_height, start_image, setlevel: callable):
    button_width = 300
    button_height = 145
    x = (window_width - button_width) // 2
    y = (window_height - button_height) // 2
    my_font = pygame.font.Font('arialbd.ttf', 40)
    my_button = Button(x, y, button_width, button_height, "Rozpocznij grę", (255,255,255), my_font, (0,0,0), 1, setlevel)
    outline = pygame.Rect(x - 3, y - 3, button_width + 6, button_height + 6)
    screen.blit(start_image, (0,0))
    outline = pygame.Rect(x - 3, y - 3, button_width + 6, button_height + 6)
    pygame.draw.rect(screen, (0,0,0), outline)
    my_button.draw(screen)
    return my_button
    
