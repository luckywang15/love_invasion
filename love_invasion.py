import pygame
from arrow import Arrow
from love import Love
import game_functions as gf
from settings import Settings
from game_stats import GameStats
from scoreboard import  Scoreboard
from button import Button
from pygame.sprite import Group

def run_game():
    #初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Love Invasion")

    #创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    #创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #创建一艘爱神之弓、一个子弹编组和一个爱心编组
    arrow = Arrow(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    loves = Group()

    #创建爱心群
    gf.create_fleet(ai_settings, screen, arrow, loves)

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, arrow, loves, bullets)
        if stats.game_active:
            arrow.update()
            gf.update_bullets(ai_settings, screen, stats, sb, arrow, loves, bullets)
            gf.update_loves(ai_settings, screen, stats, sb, arrow, loves, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, arrow, loves, bullets, play_button)

run_game()