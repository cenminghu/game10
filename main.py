import random
import pygame
from pygame.locals import *


# 窗体的高度和宽度
WIDTH = 1200
HEIGHT = 600


# 创建豌豆类
class Peas:
    def __init__(self):
        self.image = pygame.image.load("./res/peas.jfif")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image_rect = self.image.get_rect()
        self.image_rect.top = 150
        self.image_rect.left = 230
        # 设置豌豆是否上下移动
        self.is_move_down = False
        self.is_move_up = False
        self.is_shout = False

    def display(self):
        """显示豌豆在页面上"""
        screen.blit(self.image, self.image_rect)

    def move_up(self):
        if self.image_rect.top > 150:
            self.image_rect.move_ip(0, -25)
        for z in Zombie.zombie_list:
            if self.image_rect.colliderect(z.image_rect):
                pygame.quit()
                exit()

    def move_down(self):
        if self.image_rect.top < 500:
            self.image_rect.move_ip(0, +25)
        for z in Zombie.zombie_list:
            if self.image_rect.colliderect(z.image_rect):
                pygame.quit()
                exit()

    def shout_bullet(self):
        # 创建炮弹对象
        bullet = Bullet(self)
        # 保存创建好的炮弹对象
        Bullet.bullet_list.append(bullet)


# 僵尸类
class Zombie:
    # 保存多个僵尸
    zombie_list = []
    inerval = 0

    def __init__(self):
        self.image = pygame.image.load("./res/僵尸.jfif")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image_rect = self.image.get_rect()
        self.image_rect.top = random.randint(150, HEIGHT - 100)
        self.image_rect.left = WIDTH - 50

    def display(self):
        """显示僵尸"""
        screen.blit(self.image, self.image_rect)

    def move(self):
        """僵尸移动"""
        for b in Bullet.bullet_list:
            print(b.image_rect)
            if self.image_rect.colliderect(b.image_rect):
                Bullet.bullet_list.remove(b)
                Zombie.zombie_list.remove(self)
                break
        self.image_rect.move_ip(-10, 0)
        if self.image_rect.left <= 100:
            Zombie.zombie_list.remove(self)
        if self.image_rect.colliderect(peas.image_rect):
            pygame.quit()
            exit()


# 炮弹对象
class Bullet:
    bullet_list = []
    interval = 0

    def __init__(self, pea):
        self.image = pygame.image.load("./res/豆子.jpg")

        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image_rect = self.image.get_rect()
        print("炮弹大小：",self.image_rect)
        self.image_rect.top = pea.image_rect.top
        self.image_rect.left = pea.image_rect.left + 50

    def display(self):
        # for bullet in Bullet.bullet_list:
        screen.blit(bullet.image,bullet.image_rect)

    def move(self):
        for z in Zombie.zombie_list:
            if self.image_rect.colliderect(z.image_rect):
                Bullet.bullet_list.remove(self)
                Zombie.zombie_list.remove(z)
                break
        self.image_rect.move_ip(30, 0)
        # 如果炮弹越界，需要删除
        if self.image_rect.left > WIDTH - 40:
            Bullet.bullet_list.remove(self)


def key_control():
    """事件监听函数"""
    for event in pygame.event.get():
        # 事件判断
        if event.type == QUIT:
            pygame.quit()
            exit()
        # 按下键盘事件的监听
        elif event.type == KEYDOWN:
            # 判断具体按下的键
            if event.key == K_UP:
                peas.is_move_up = True
            elif event.key == K_DOWN:
                peas.is_move_down = True
            elif event.key == K_SPACE:
                peas.is_shout = True

        elif event.type == KEYUP:
            if event.key == K_UP:
                peas.is_move_up = False
            elif event.key == K_DOWN:
                peas.is_move_down = False
            elif event.key == K_SPACE:
                peas.is_shout = False


if __name__ == '__main__':
    # 显示窗体
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # 背景图
    backgrount_image = pygame.image.load("./res/background.jfif")
    # 改变图片大小
    backgrount_image = pygame.transform.scale(backgrount_image,(WIDTH,HEIGHT))
    backgrount_image_rect = backgrount_image.get_rect()

    clock = pygame.time.Clock()
    # 创建豌豆对象
    peas = Peas()
    while True:
        # 设置窗体背景图片
        screen.fill((0,0,0))
        screen.blit(backgrount_image, backgrount_image_rect)
        # 对事件的处理
        key_control()
        # 显示豌豆
        peas.display()

        if peas.is_move_up:
            peas.move_up()
        if peas.is_move_down:
            peas.move_down()

        # 发射炮弹
        Bullet.interval += 1
        if peas.is_shout and Bullet.interval >= 5:
            Bullet.interval = 0
            peas.shout_bullet()
            print("发射炮弹")

        # 创建僵尸对象，并保存
        Zombie.inerval += 1
        if Zombie.inerval >= 10:
            Zombie.inerval = 0
            zombie = Zombie()
            Zombie.zombie_list.append(zombie)

        # 显示所有炮弹
        for bullet in Bullet.bullet_list:
            bullet.display()
            bullet.move()

        # 显示所有僵尸
        for zombie in Zombie.zombie_list:
            zombie.display()
            # 僵尸移动
            zombie.move()

        # 屏幕刷新的频率
        clock.tick(10)
        pygame.display.update()


