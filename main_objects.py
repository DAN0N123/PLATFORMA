import pygame


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
                if self.on_click:
                    self.on_click(self.level)   
           
class Player():
    def __init__(self, sprite, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.onplatform = False
        self.height = 87
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

    def draw(self, screen):
        screen.blit(self.model, (self.x, self.y))

    def movement(self, force = None):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            if self.x >= 3: 
                self.x -= self.speed

        if keys[pygame.K_d]:
            if self.x <= self.window_width - 103:
                self.x += self.speed
        # if keys[pygame.K_SPACE] and not self.jumping or force == 'jump' and not self.jumping:
        #     self.tempy = self.y
        #     self.jumping = True
        #     self.jump_velocity = -self.jump_height

        if not self.jumping:
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
