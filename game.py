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

    
class platform_object(game_object):                 
    def __init__(self, x, y, width, height, color, image=None):
        super().__init__(x, y, width, height, color, image)
    


    def draw(self, screen):
        super().draw(screen)


class Player():
    def __init__(self):
        self.onplatform = False
        self.height = 87
        self.width = 100
        self.speed = 3
        self.model = testing
        self.x = 768
        self.y = 664
        self.fallingdown = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.jumping = False
        self.jump_height = 30
        self.gravity = 1
        self.tempy = 0

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
            self.tempy = self.y
            self.jumping = True
            self.jump_velocity = -self.jump_height

        if self.jumping:
            if self.y <= self.tempy - 465:
                self.fallingdown = True
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity
            
            if self.y >= 664:
                self.fallingdown = False
                self.y = 664
                self.jumping = False
                self.jump_velocity = 0

    def collision_with_platform(self, platform: platform_object):
        if self.hitbox.colliderect(platform.object):
            return True
                
platforms = []     

    

my_player = Player()    
floor = game_object(0, 751, 1536, 200, yellow)
platforms.append(platform_object(1000, 440, 200, 20, black))
platforms.append(platform_object(200, 600, 300, 20, black))
last_action_time = 0
check = []


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((89, 201, 250)) 

    current_time = pygame.time.get_ticks()
    
    floor.draw(screen)
    my_player.draw(screen)
    my_player.movement()
    my_player.hitbox.x = my_player.x
    my_player.hitbox.y = my_player.y 


    for a_platform in platforms:
        a_platform.draw(screen)
        if my_player.collision_with_platform(a_platform) and my_player.fallingdown:
            my_player.y = a_platform.y - my_player.height
            my_player.jumping = False
            my_player.jump_velocity = 0
        elif my_player.y < 664 and not my_player.collision_with_platform(a_platform):
            my_player.jump_height = 0
            my_player.jumping = True
        if my_player.y >= 664:
            my_player.jump_height = 30
            my_player.y = 664
            my_player.jumping = False
    

    clock.tick(144)
    pygame.display.flip()

    
    

pygame.quit()
sys.exit()