import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/spaceship.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.alien_speed = 3
    def update(self):
        self.x += self.settings.alien_speed *self.settings.fleet_direction
        self.rect.x=self.x
        #我们使用属性 self.x 跟踪每个外星人的精确位置，这个属性可存储浮点数

    def check_edges(self):
        #如果外星人位于屏幕边缘，就返回TURE
        screen_rect = self.screen.get_rect()
        return (self.rect.right>=screen_rect.right) or (self.rect.left<=0)

