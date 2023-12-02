import pygame
import sys
import math
import random

width = 1536
height = 864

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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.object)
        if self.image:
            screen.blit(self.image, (self.x,self.y))
 
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
        if True in keys:
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
                    if self.y <= self.tempy - 465:
                        self.fallingdown = True
                    self.y += self.jump_velocity
                    self.jump_velocity += self.gravity
                    
                    if self.y >= 664 and not self.aboveground:
                        self.fallingdown = False
                        self.y = 664
                        self.jumping = False
                        self.jump_velocity = 0
            
                
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
        
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def collision_with_platform(self, platform: game_object):
        if self.hitbox.colliderect(platform.object):
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
        # return self
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

    