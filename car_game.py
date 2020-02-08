import pygame
import sys
import time
import random
from pygame.locals import *

# 设置背景颜色和线条颜色
SCREEN_COLOR = (0, 0, 0)
LINE_COLOR = (0, 0, 255)
# 设置背景框大小
SIZE = WIDTH, HEIGHT = 400, 640

# 期望的FPS
DEFAULT_FPS = 60
DEFAULT_DELAY = 1.0 / DEFAULT_FPS - 0.002


def collide(r1, r2):
    '''
    判断矩形是否相撞
    :param r1:
    :param r2:
    :return:
    '''
    if r1.x + r1.width / 2 != r2.x + r2.width / 2:
        return False
    if r1.y > r2.y + r2.height:
        return False
    if r1.y + r1.height < r2.y:
        return False
    return True


class Stone:
    def __init__(self, window):
        self.window = window
        self.reset()

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += 5
        if self.y > HEIGHT:
            self.reset()

    def reset(self):
        self.img = pygame.image.load("img/stone.png")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        min = (WIDTH - 40) / 6 + 20 - self.width / 2
        max = (WIDTH - 40) * 5 / 6 + 20 - self.width / 2
        self.x = random.randrange(min, max + (WIDTH - 40) / 3, (WIDTH - 40) / 3)
        self.y = random.randrange(-self.height * 15, 0, self.height * 5)


class PlayerCar:
    def __init__(self, windonw):
        self.window = windonw
        self.img = pygame.image.load("img/car.png")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = (WIDTH - self.width) / 2
        self.y = HEIGHT - self.height
        self.__around = 120
        self.__bound = 5

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move_left(self):
        self.x -= self.__around
        if self.x < (WIDTH - 40) / 6 + 20 - self.width / 2:
            self.x = (WIDTH - 40) / 6 + 20 - self.width / 2

    def move_right(self):
        self.x += self.__around
        if self.x > (WIDTH - 40) * 5 / 6 + 20 - self.width / 2:
            self.x = (WIDTH - 40) * 5 / 6 + 20 - self.width / 2

    def move_up(self):
        self.y -= self.__bound
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += self.__bound
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height


if __name__ == "__main__":
    # pygame 初始化
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("黑马汽车避障")
    # 加载汽车
    player = PlayerCar(screen)
    # 加载石头
    stone_list = []
    for _ in range(5):
        stone = Stone(screen)
        stone_list.append(stone)
    fps = 0
    score = 0
    font = pygame.font.Font("font/happy.ttf", 30)
    font_finish = pygame.font.Font("font/happy.ttf", 60)

    is_over = False

    while True:
        start = time.time()
        # 填充背景色
        screen.fill(SCREEN_COLOR)
        fps_text = font.render("FPS:%d" % fps, True, (0x22, 0xff, 0x22))
        screen.blit(fps_text, (280, 10))
        score_text = font.render("得分:%d" % score, True, (0xff, 0x22, 0x22))
        screen.blit(score_text, (40, 10))

        finish_text1 = font_finish.render("游戏结束", True, (0xaa, 0, 0))
        finish_text2 = font_finish.render("最后得分", True, (0xaa, 0xbb, 0x22))
        finish_score = font_finish.render("%d" % score, True, ((0, 0xee, 0)))
        ft_width = finish_text1.get_width()
        ft_height = finish_text2.get_height()
        ft_x = (WIDTH - ft_width) / 2
        ft_y = (HEIGHT - ft_height) / 2 - 50
        score1_x = ft_x
        score1_y = ft_y + 200
        score_width = finish_score.get_width()
        score2_x = (WIDTH - score_width) / 2
        score2_y = score1_y + 80

        # 画不抗锯齿的一条直线
        pygame.draw.aaline(screen, LINE_COLOR, (20, 0), (20, 640), 1)
        pygame.draw.aaline(screen, LINE_COLOR, (140, 0), (140, 640), 1)
        pygame.draw.aaline(screen, LINE_COLOR, (260, 0), (260, 640), 1)
        pygame.draw.aaline(screen, LINE_COLOR, (380, 0), (380, 640), 1)
        if is_over:
            screen.blit(finish_text1, (ft_x, ft_y))
            screen.blit(finish_text2, (score1_x, score1_y))
            screen.blit(finish_score, (score2_x, score2_y))
        if not is_over:

            # 显示汽车
            player.display()

            # 显示石头
            for i in range(1, len(stone_list)):
                if stone_list[i - 1].y == stone_list[i].y:
                    stone_list[i].y = stone_list[i-1].y - stone_list[i].height*3
                stone_list[i].display()
                stone_list[i].move()

                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                stone_rect = pygame.Rect(stone_list[i].x, stone_list[i].y, stone_list[i].width, stone_list[i].height)
                if collide(player_rect, stone_rect):
                    # 玩家赛车阵亡
                    is_over = True
                if stone_list[i].y == HEIGHT:
                    score += 10

        # 刷新图像
        pygame.display.flip()
        for event in pygame.event.get():
            # 查找关闭窗口事件
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.move_left()
                if event.key == K_RIGHT:
                    player.move_right()
                if event.key == K_RETURN and is_over:
                    for stone in stone_list:
                        stone.reset()
                    score = 0
                    is_over = False

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            player.move_up()
        if keys[K_DOWN]:
            player.move_down()

        # 结束时间
        end = time.time()
        # 逻辑耗时
        cost = end - start
        if cost < DEFAULT_DELAY:
            sleep = DEFAULT_DELAY - cost
        else:
            sleep = 0
        # 睡眠
        time.sleep(sleep)
        end = time.time()
        fps = 1.0 / (end - start)
        # print(fps)
