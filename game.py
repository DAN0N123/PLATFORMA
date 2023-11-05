import pygame
import sys

pygame.init()

window_width = 1536
window_height = 864

screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("ŚWIRKI")

player_sprite = pygame.image.load("nobackgroundluffysprite.png")
testing = pygame.transform.scale(player_sprite, (100,100))

running = True
clock = pygame.time.Clock()

is_gravity = True

white = (255, 255, 255)
green = (83,141,78)
blue = (89, 201, 250)
red = (255,0,0)
black = (0,0,0)
yellow = (181,159,60)
gray = (80,80,80)


class game_object():
    def __init__(self, x, y, width, height, color, image = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.object = pygame.Rect(x,y,width,height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.object)

    

class Player():
    def __init__(self):
        self.height = 80
        self.width = 30
        self.speed = 3
        self.model = testing
        self.x = 768
        self.y = 664
        self.jumping = False
        self.jump_height = 20
        self.gravity = 1

    def draw(self, screen):
        screen.blit(self.model, (self.x, self.y))

    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            if self.x >= 3: 
                self.x -= self.speed
        
        if keys[pygame.K_d]:
            if self.x <= window_width - 103:
                self.x += self.speed
        
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.jump_velocity = -self.jump_height  # Start the jump with an upward velocity

        if self.jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity

            if self.y >= 664:  
                self.y = 664
                self.jumping = False
                self.jump_velocity = 0

        if self.y > 664:
            self.y = 664
            self.jumping = False
                
                
                    



# def anti_gravity(object, speed):
#     if object.y > 564:
#         object.y -= speed
#     else:
#         object.y = 564
    

my_player = Player()    
floor = game_object(0, 751, 1536, 200, yellow)

last_action_time = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((89, 201, 250)) 

    current_time = pygame.time.get_ticks()

    floor.draw(screen)
    my_player.draw(screen)
    my_player.movement()

    # if current_time - last_action_time >= 1000:
    

    clock.tick(144)
    pygame.display.flip()

    
    

pygame.quit()
sys.exit()