import pygame
class Ship:
    def __init__(self,ai_game):
        '初始化飞船的位置'
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        #家在飞船图片并且获取其外接矩形
        self.image = pygame.image.load('Images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom=self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right=False
        self.moving_left = False
    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            #self.rect.right 返回飞船外接矩形的右边缘的 x 坐标
            self.x+= self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x-= self.settings.ship_speed
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        #指定位置绘制飞船
        self.screen.blit(self.image,self.rect)
