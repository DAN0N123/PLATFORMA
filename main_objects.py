import pygame
import sys
import math
import random

width = 1536
height = 864

yellow = (246, 253, 2)
red = (218, 0, 19)
blue = (2, 67, 185)
green = (22, 206, 68)

def make_floor(screen):
    floor_image= pygame.image.load("zdjęcia/podłoga.png")
    floor_image_scaled = pygame.transform.scale(floor_image, (150,200))
    for i in range(0,11):
        screen.blit(floor_image_scaled, (150*i, 751))

def scale_image(image, res = tuple):
    scaled_image = pygame.transform.scale(image, res)
    return scaled_image
class game_object():
    def __init__(self, x, y, width, height, color, image = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        self.object = pygame.Rect(x,y,width,height)
        self.hitbox = pygame.Rect(x,y,width,5)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.object)
        if self.image:
            screen.blit(self.image, (self.x,self.y))

class Note():
    def __init__(self, which_branch):
        image_init = pygame.image.load("zdjęcia/notetesting.png")
        self.branch = which_branch
        self.width = 80
        self.height = 80
        self.gap = 100
        self.color = None
        self.x = ((1536 - 4 * (self.gap + self.width)) // 2) + ((self.gap + self.width)*self.branch)
        self.y = -self.height
        self.image = pygame.transform.scale(image_init, (self.width, self.height))
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.played = False
    def reset(self):
        self.y = -self.height
        self.played = False
    def draw(self, screen):
        match self.branch:
            case 0:
                self.color = green
            case 1:
                self.color = red
            case 2:
                self.color = yellow
            case 3:
                self.color = blue
        pygame.draw.circle(screen, self.color, (self.x + self.width // 2, self.y), self.width // 2)
    def falling(self):
        self.y += 5
class Note_Box():
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 60
        self.height = 100
        # (x,y,z) = self.color
        # self.filling_color = [x - 100, y - 100, z - 100]
        # for index, hex in enumerate(self.filling_color):
        #     if hex < 0:
        #         self.filling_color[index] = 0
        self.width = 10
        self.pulsating = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self, screen):
        if self.pulsating:
            # radius = ((self.radius *  2) - 10) // 2
            # pygame.draw.circle(screen, tuple(self.filling_color), (self.x, self.y), radius)
            self.width = 20
            self.radius = 70
        else:
            self.radius = 60
            self.width = 10
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.width)

class popup:
    def __init__(self, image, location, w_width, w_height):
        (width, height) =  image.get_size()
        self.location = location
        if location == 1:
            self.x = 20
            self.y = (w_height - height) // 2
        if location == 2:
            self.x = (w_width - width) // 2
            self.y = 20
        if location == 3:
            self.x = w_width  - width - 20
            self.y = (w_height - height) // 2
        if location == 4:
            self.x = (w_width  - width) // 2
            self.y = w_height - 20 - height
        self.image = image
        self.todraw = False
        self.starting_time = 0
        self.duration = 0
    def draw(self, screen):
        if self.todraw:
            screen.blit(self.image, (self.x, self.y))
    def check_time(self, current_time):
        if self.todraw and self.starting_time > 0 and current_time - self.starting_time >= self.duration:
            self.todraw = False
            self.starting_time = 0

        


class Button:
    def __init__(self, x, y, width, height, text, color, font, text_color, level, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = font
        self.text_color = text_color
        self.on_click = on_click
        self.level = level

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font_surface = self.font.render(self.text, True, self.text_color)
        text_rect = font_surface.get_rect(center=self.rect.center)
        screen.blit(font_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click and self.level:
                    self.on_click(self.level)
                elif self.on_click and not self.level:
                    self.on_click()   
           
class Player():
    def __init__(self, sprite, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.onplatform = False
        self.height = 91
        self.width = 100
        self.speed = 8
        self.model = sprite
        self.x = 768
        self.y = 664
        self.fallingdown = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.jumping = False
        self.jump_height = 30
        self.gravity = 1
        self.tempy = 0
        self.aboveground = False
        self.rank = 0
        self.check = 0
        self.currentrank = None
        self.canjump = True
        self.autojump = False
        self.walkingleft = False
        self.walkingright = False
        self.walkingup = False
        self.walkingdown = False
        self.wallright = False
        self.wallup = False
        self.wallleft = False
        self.walldown = False
        self.twoDmovement = False
    def draw(self, screen):
        screen.blit(self.model, (self.x, self.y))
    def reset_position(self):
        self.x = 768
        self.y = 664
        self.fallingdown = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.jumping = False
        self.jump_height = 30
    def movement(self):
        keys = pygame.key.get_pressed()
        if self.twoDmovement and True in keys:
            if keys[pygame.K_a]:
                if not self.wallleft:
                    if self.x >= self.speed: 
                        self.x -= self.speed
                        self.walkingleft = True
            if keys[pygame.K_d]:
                if not self.wallright:
                    if self.x <= self.window_width - self.width - 8:
                        self.x += self.speed
                        self.walkingright = True
                
            if keys[pygame.K_w]:
                if not self.wallup:
                    if self.y >= self.speed:
                        self.y -= self.speed
                        self.walkingup = True
            if keys[pygame.K_s]:
                if not self.walldown:
                    if self.y <= self.window_height - self.height - self.speed:
                        self.y += self.speed
                        self.walkingdown = True
        else:
            self.walkingup = False
            self.walkingdown = False
            self.walkingleft = False
            self.walkingright = False

        if not self.twoDmovement:
            if keys[pygame.K_a]:
                if self.x >= self.speed: 
                    self.x -= self.speed
                    self.walkingleft = True
            if keys[pygame.K_d]:
                if self.x <= self.window_width - self.width - 8:
                    self.x += self.speed
                    self.walkingright = True
        
        if self.canjump:
            if self.autojump:
                if not self.jumping:
                    self.tempy = self.y
                    self.jumping = True
                    self.jump_velocity = -self.jump_height
            else:
                if keys[pygame.K_SPACE] and not self.jumping:
                    self.tempy = self.y
                    self.jumping = True
                    self.jump_velocity = -self.jump_height   
            if self.jumping:
                self.y += self.jump_velocity
                self.jump_velocity += self.gravity
                if self.y <= self.tempy - 465:
                    self.fallingdown = True
                    self.jump_velocity += self.gravity
                if self.y >= 664 and not self.aboveground:
                    self.fallingdown = False
                    self.y = 664
                    self.jumping = False
                    self.jump_velocity = 0

        self.hitbox.x = self.x
        self.hitbox.y = self.y
    def collision_with_platform(self, platform_hitbox):
        if self.hitbox.colliderect(platform_hitbox):
            return True
        
    def rankup(self, ktore_levele):
        if self.currentrank:
            if self.hitbox.colliderect(self.currentrank):
                self.currentrank = None
                ktore_levele.pop(0)
                self.rank += 1
        return ktore_levele
        
    def check_if_on_platform(self,platform_list):
        for i in platform_list:
            if not self.fallingdown and self.hitbox.x > i.object.x - self.width and self.hitbox.x < i.object.x + i.object.width:
                return True
        return False
    
    def show_rank(self, ranks_list, screen):
        rank = ranks_list[self.rank]
        screen.blit(rank, (100, 100))

class projectile():
    def __init__(self, speed, image_path):
        self.x = width // 2 - 30
        self.y = 120
        self.inital_x = self.x
        self.inital_y = self.y
        self.speed = speed
        self.index = None
        self.hitbox_vertical = pygame.Rect(self.x + 45, self.y + 10, 30, 80)
        self.hitbox_diagonal = pygame.Rect(self.x, self.y, 30,25)
        self.angle = random.randint(43,137)
        self.anglerad = math.radians(self.angle)
        self.velocity_x = self.speed * math.cos(self.anglerad)
        self.velocity_y = self.speed * math.sin(self.anglerad)
        image1 = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image1, (100,100))
    def update_hitbox(self):
        self.hitbox_vertical.x = self.x + 45
        self.hitbox_vertical.y = self.y + 10
        self.hitbox_diagonal.x = self.x + 20
        self.hitbox_diagonal.y = self.y + 25
    def update_angle(self):
        self.angle =  random.randint(43,137)
        self.anglerad = math.radians(self.angle)
        self.velocity_x = self.speed * math.cos(self.anglerad)
        self.velocity_y = self.speed * math.sin(self.anglerad)
    def check_collision(self, player_hitbox: pygame.Rect):
        if self.hitbox_diagonal.colliderect(player_hitbox) or self.hitbox_vertical.colliderect(player_hitbox):
            return True
    def movement(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.x = int(self.x)
        self.y = int(self.y)
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))
        # pygame.draw.rect(screen, (0,0,0), self.hitbox_vertical)
        # pygame.draw.rect(screen, (0,0,0), self.hitbox_diagonal)
    def reset(self):
        self.x = self.inital_x
        self.y = self.inital_y

    def out_of_screen(self):
        if self.x not in range(0, width) or self.y not in range(0, height):
            return True
        else:
            return False

    