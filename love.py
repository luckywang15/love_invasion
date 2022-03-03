import pygame
from pygame.sprite import Sprite
class Love(Sprite):
    """表示单个爱心的类"""

    def __init__(self, ai_settings, screen):
        """初始化爱心并设置其起始位置"""
        super(Love, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载爱心图像，并设置其rect属性
        self.image = pygame.image.load('images/love.bmp')
        self.rect = self.image.get_rect()

        #每个爱心最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储爱心的准确位置
        self.x = float(self.rect.x)



    def blitme(self):
        """在指定位置绘制爱心"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        '''如果爱心位于屏幕边缘，就返回True'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        '''向右移动爱心'''
        self.x += (self.ai_settings.love_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x