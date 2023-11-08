import pygame


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
    def __init__(self, sprite, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.onplatform = False
        self.height = 87
        self.width = 100
        self.speed = 3
        self.model = sprite
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
            if self.x <= self.window_width - 103:
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
    def check_if_on_platform(self,platform_list):
        for i in platform_list:
            if not self.fallingdown and self.hitbox.x > i.object.x - self.width and self.hitbox.x < i.object.x + i.object.width:
                return True
        return False