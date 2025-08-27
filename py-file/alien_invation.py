import sys
import pygame
from setting import Settings
from ship import Ship
from scoreboard import Scoreboard
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button

class AlienInvasion:
    #初始化函数
    def __init__(self):
        pygame.init()
        self.last_bullet_time=0
        self.clock = pygame.time.Clock()
        self.settings=Settings()#创建一个settings的实例对象
        self.settings.screen_width = 1000
        self.settings.screen_height = 600
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        #创建一个显示窗口
        pygame.display.set_caption('Alien Invasion')
        self.ship=Ship(self)
        #self.bg_color =(230,230,230)
        #三个数字分别代表RGB三色，红,绿,蓝. 呈现灰色
        self.ship=Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.game_active = False
    #启动游戏后的函数
        #创建 Play 按钮
        self.play_button = Button(self,'Play')
    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_aliens()
            self._update_bullets()
            self._update_screen()
                # print(len(self.bullets))
            #每次循环都绘制屏幕
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                if current_time - self.last_bullet_time>=self.settings.cooldown:
                    self._fire_bullet()
                    self.last_bullet_time = current_time

            pygame.display.flip()
            self.clock.tick(60)#确保这个while循环每秒运行60次！
            #让最近绘制的屏幕可见，每次执行while循环时都会绘制一个空屏幕
    def showifo(self):
        print(f'waves: {self.settings.waves},score: {self.stats.score},ship speed:{self.settings.alien_speed},shootingrate: {1000 / self.settings.cooldown}')


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *=-1
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type== pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:#松开按键键
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    def _check_play_button(self,mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.game_active:
                self.settings.initialize_dynamic_settings()
                self.showifo()
                self.stats.reset_stats()
                self.game_active = True
                self.bullets.empty()
                self.aliens.empty()
                self._create_fleet()
                self.ship.center_ship()
                pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.showifo()
            sys.exit()
        # elif event.key==pygame.K_SPACE:
        #     self._fire_bullet()
        elif event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _ship_hit(self):
        #将ship_ left减1
        #晴空外形繁荣列表和子弹列表
        self.bullets.empty()
        self.aliens.empty()
        if self.stats.ship_left>0:
            self.stats.ship_left -=1
            # 创建新的外星舰队
            self._create_fleet()
            # 将飞船放在中央
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >=self.settings.screen_height:
                self._ship_hit()
                break
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        self._check_aliens_bottom()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
    def _create_alien(self, x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        current_x,current_y = alien_width,alien_height
        while current_y < (self.settings.screen_height - 3* alien_height):
            current_x = alien_width
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width
            current_y += 2 * alien_height
        #添加一行外星人之后，重制抵消并且递增y值

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #显示得分
        self.sb.show_score()
        #如果游戏处于非活动状态，就绘制 Play 按钮
        if not self.game_active:
            self.play_button.draw_button()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 每当有子弹和外星人的 rect 重叠时，groupcollide() 就在返回的字典中添加一个键值对。
        # 两个值为 True 的实参告诉 Pygame 在发生碰撞时删除对应的子弹和外星人。
        if collisions:
            self.stats.score +=self.settings.alien_points
            self.sb.prep_score()
            self.sb.prep_wave()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.showifo()


    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullet_allowed:
            new_bullet = Bullet(self)
        #创建一个子弹，并且将它加入编组bullete
            self.bullets.add(new_bullet)
            #检查bullet和alines的rect是否重叠在一起

if __name__ =='__main__':
    ai = AlienInvasion()
    ai.run_game()


