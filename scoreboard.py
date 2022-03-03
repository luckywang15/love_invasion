import pygame.font
from pygame.sprite import Group

from arrow import Arrow

class Scoreboard():
    '''显示得分信息的类'''

    def __init__(self, ai_settings, screen, stats):
        '''初始化显示得分涉及的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #准备包含最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_arrows()

    def prep_score(self):
        '''得分转换为一幅渲染的图像'''
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        #将得分放在屏幕左上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        '''在屏幕上显示爱神之弓和得分'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #绘制爱神之弓
        self.arrows.draw(self.screen)

    def prep_high_score(self):
        '''将最高分转换为渲染的图像'''
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        #将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        '''将等级转换为渲染的图像'''
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        #将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_arrows(self):
        '''显示还余下多少艘爱神之弓'''
        self.arrows = Group()
        for arrow_number in range(self.stats.arrows_left):
            arrow = Arrow(self.ai_settings, self.screen)
            arrow.rect.x = 10 + arrow_number * arrow.rect.width
            arrow.rect.y = 10
            self.arrows.add(arrow)
