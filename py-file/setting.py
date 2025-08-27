class Settings:
    #储存外星人入侵中所有设置
    def __init__(self):
        #初始化游戏的设置
        self.screen_width=840
        self.screen_height = 560
        self.bg_color = (230,230,230)
        self.ship_speed = 8
        self.bullet_speed=16.0
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 10
        self.alien_speed=4
        self.fleet_drop_speed =10
        #fleet_direton 为1的时候表示向右，为-1表示向左
        self.fleet_direction=1
        self.ship_limit =2
        #以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        self.cooldown = 125
        self.cooldown_max=17
        self.max_bullet_width = 30
        self.max_bullet_height = 90
        self.waves = 1
    def initialize_dynamic_settings(self):
        self.ship_speed = 4
        self.buttlet_speed =8
        self.alien_speed = 2.5
        # fleet_direction 为 1 表示向右，为-1 表示向左
        self.fleet_direction =1
        self.cooldown=125
        self.bullet_width = 5
        self.bullet_height = 15
        self.alien_points = 75
        self.waves = 1
    def increase_speed(self):
        if self.waves<=20:
            self.ship_speed *=self.speedup_scale
            self.bullet_speed *=self.speedup_scale
            self.alien_speed *= self.speedup_scale
        elif self.waves>=35:
            self.ship_speed *= self.speedup_scale
        self.alien_points +=50
        self.waves +=1

        if self.cooldown > self.cooldown_max:
            self.cooldown/=1.1
            self.bullet_height += 5
        else:
            if self.waves<=16:
                self.bullet_width+=1
            elif self.waves>16:
                self.bullet_width+=5