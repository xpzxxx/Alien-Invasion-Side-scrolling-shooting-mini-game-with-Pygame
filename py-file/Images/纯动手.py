import sys
import pygame
pygame.init()
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((400,300))
speed =4
bullet_speed =8
last_shot_time=0
bullet_cooldown = 200# 毫秒！！
#screen 是一个surface变量
pygame.display.set_caption('中央火箭游戏')
clock = pygame.time.Clock()

rocket_image = pygame.image.load('ship.bmp')
rocket_rect = rocket_image.get_rect()
rocket_rect.center = (200,250)
bullets=[]
class Bullet:
    def __init__(self,x,y):
        self.rect= pygame.Rect(0,0,3,15)
        self.rect.midbottom = (x,y)
    def update(self):
        self.rect.y -=bullet_speed
    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.rect)
        #pygame.draw.rect(screen, color, rect) 用于绘制 基本图形（如矩形）
while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #elif event.type == pygame.KEYDOWN:
            #这里是单下点击触发，避免了按住每秒连发60次
            # if event.key == pygame.K_SPACE:
            #     new_bullet = Bullet(rocket_rect.centerx,rocket_rect.top)
            #     bullets.append(new_bullet)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and current_time - last_shot_time > bullet_cooldown:
        #增加冷却限制射速
        new_bullet = Bullet(rocket_rect.centerx,rocket_rect.top+10)
        bullets.append(new_bullet)
        last_shot_time =current_time
    if keys[pygame.K_q]:
        sys.exit()
    if keys[pygame.K_RIGHT] and rocket_rect.right < screen_width:
        rocket_rect.x +=speed
    if keys[pygame.K_LEFT] and rocket_rect.left >0:
        rocket_rect.x -=speed
    if keys[pygame.K_UP] and rocket_rect.top >0:
        rocket_rect.y -=speed
    if keys[pygame.K_DOWN] and rocket_rect.bottom< screen_height:
        rocket_rect.y +=speed
    for bullet in bullets[:]:
        #为了在下方删除列表中的元素，这里遍历的是列表的副本 即【:】符号
        bullet.update()
        if bullet.rect.bottom<0:
            bullets.remove(bullet)


    screen.fill((255,255,255))
    screen.blit(rocket_image, rocket_rect)
    for bullet in bullets:
        bullet.draw(screen)
    #在screen这个surface中加入image 和 矩形
    pygame.display.flip()
    clock.tick(60)
