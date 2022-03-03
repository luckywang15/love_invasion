class Settings():
    """存储《爱心入侵》设置的所有类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        #爱神之弓设置
        # self.arrow_speed_factor = 3
        self.arrow_limit = 3

        #子弹设置
        # self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 6

        # 爱心设置
        # self.love_speed_factor = 1
        self.fleet_drop_speed = 10


        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        #爱心点数提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.arrow_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.love_speed_factor = 1

        # self_direction为1表示向右移，-1表示向左移
        self.fleet_direction = 1

        #计分
        self.love_points = 50

    def increase_speed(self):
        '''提高速度的设置和爱心点数'''
        self.arrow_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.love_speed_factor *= self.speedup_scale

        self.love_points = int(self.love_points * self.score_scale)
