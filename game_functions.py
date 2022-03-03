import sys
import pygame
from bullet import Bullet
from love import Love
from time import sleep

def check_keydown_events(event, ai_settings, screen, arrow, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        arrow.moving_right = True
    elif event.key == pygame.K_LEFT:
        arrow.moving_left = True
    elif event.key == pygame.K_UP:
        arrow.moving_up = True
    elif event.key == pygame.K_DOWN:
        arrow.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, arrow, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, arrow, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, arrow)
        bullets.add(new_bullet)

def check_keyup_events(event, arrow):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        arrow.moving_right = False
    elif event.key == pygame.K_LEFT:
        arrow.moving_left = False
    elif event.key == pygame.K_UP:
        arrow.moving_up = False
    elif event.key == pygame.K_DOWN:
        arrow.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, arrow, loves, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, arrow, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, arrow)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, arrow, loves, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, arrow, loves, bullets, mouse_x, mouse_y):
    '''在玩家单击Play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()

        #隐藏光标
        pygame.mouse.set_visible(False)

        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_arrows()

        #清空爱心列表和子弹列表
        loves.empty()
        bullets.empty()

        #创建一群新的爱心，并让爱神之弓居中
        create_fleet(ai_settings, screen, arrow, loves)
        arrow.center_arrow()

def update(self):
    """根据移动标志调整爱神之弓的位置"""
    if self.moving_right:
        self.rect.centerx += 1
    if self.moving_left:
        self.rect.centerx -= 1

def update_screen(ai_settings, screen, stats, sb, arrow, loves, bullets, play_button):
    """更新屏幕上的图像， 并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    #在爱神之弓和爱心后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    arrow.blitme()
    loves.draw(screen)

    #显示得分
    sb.show_score()

    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, arrow, loves, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_love_collisions(ai_settings, screen, stats, sb, arrow, loves, bullets)


def check_bullet_love_collisions(ai_settings, screen, stats, sb, arrow, loves, bullets):
    # 检查是否有子弹击中了爱心
    # 如果击中，删除相应子弹和爱心
    collisions = pygame.sprite.groupcollide(bullets, loves, True, True)

    if collisions:
        for loves in collisions.values():
            stats.score += ai_settings.love_points * len(loves)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(loves) == 0:
        # 如果整群爱心都被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, arrow, loves)


def get_number_love_x(ai_settings, love_width):
    '''计算每行可容纳多少个爱心'''
    available_space_x = ai_settings.screen_width - 2 * love_width
    number_loves_x = int(available_space_x / (2 * love_width))
    return number_loves_x

def get_number_rows(ai_settings, arrow_height, love_height):
    available_space_y = (ai_settings.screen_height - (3 * love_height) - arrow_height)
    number_rows = int(available_space_y / (2 * love_height))
    return number_rows

def create_love(ai_settings, screen, loves, love_number, row_number):
    '''创建一个爱心并将其放在当前行'''
    love = Love(ai_settings, screen)
    love_width = love.rect.width
    love.x = love_width + 2 * love_width * love_number
    love.rect.x = love.x
    love.rect.y = love.rect.height + 2 * love.rect.height * row_number
    loves.add(love)

def create_fleet(ai_settings, screen, arrow, loves):
    """创建爱心群"""
    #创建一个爱心，并计算一行可容纳多少个爱心
    #爱心间距为爱心宽度
    love = Love(ai_settings, screen)
    number_loves_x = get_number_love_x(ai_settings, love.rect.width)
    number_rows = get_number_rows(ai_settings, arrow.rect.height, love.rect.height)

    #创建爱心群
    for row_number in range(number_rows):
        for love_number in range(number_loves_x):
            #创建一行爱心并将其加入当前行
            create_love(ai_settings, screen, loves, love_number, row_number)

def check_fleet_edges(ai_settings, loves):
    '''有爱心到达边缘时采取相应措施'''
    for love in loves.sprites():
        if love.check_edges():
            change_fleet_direction(ai_settings, loves)
            break

def change_fleet_direction(ai_settings, loves):
    '''将整群爱心下移，并改变它们的方向'''
    for love in loves.sprites():
        love.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def arrow_hit(ai_settings, screen, stats, sb, arrow, loves, bullets):
    '''响应被爱心撞到的爱神之弓'''
    if stats.arrows_left > 0:
        #将arrows_left减1
        stats.arrows_left -= 1

        #更新记分牌
        sb.prep_arrows()

        #清空爱心列表和子弹列表
        loves.empty()
        bullets.empty()

        #创建一群新的爱心，并将爱神之弓放到屏幕底端中央
        create_fleet(ai_settings, screen, arrow, loves)
        arrow.center_arrow()
        arrow.bottom_arrow()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_loves(ai_settings, screen, stats, sb, arrow, loves, bullets):
    '''检查是否有爱心位于屏幕边缘，并更新爱心群中所有爱心的位置'''
    check_fleet_edges(ai_settings, loves)
    loves.update()

    #检测爱心和爱神之弓之间的碰撞
    if pygame.sprite.spritecollideany(arrow, loves):
        arrow_hit(ai_settings, screen, stats, sb, arrow, loves, bullets)

    #检查是否有爱心到达屏幕底端
    check_loves_bottom(ai_settings, screen, stats, sb, arrow, loves, bullets)

def check_loves_bottom(ai_settings, screen, stats, sb , arrow, loves, bullets):
    '''检查是否有爱心到达了屏幕底端'''
    screen_rect = screen.get_rect()
    for love in loves.sprites():
        if love.rect.bottom >= screen_rect.bottom:
            #像爱神之弓被撞一样处理
            arrow_hit(ai_settings, screen, stats, sb, arrow, loves, bullets)
            break

def check_high_score(stats, sb):
    '''检查是否诞生了新的最高得分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()