# --coding=utf-8

import pygame
import sys
# 游戏文件
from config import WINDOW_CONFIG as WIN_CFG  # 游戏窗口配置文件
from LoadLevel import LoadLevel  # 层载入文件
from module.gameFunc import GameFuncClass  # 游戏辅助函数类

class Game(LoadLevel, GameFuncClass):
    def __init__(self):
        pygame.init()  # 初始化pygame库
        self.SCREEN = pygame.display.set_mode(WIN_CFG['FULL_SIZE'], flags=pygame.HWSURFACE | pygame.FULLSCREEN | pygame.DOUBLEBUF)  # 游戏窗口
        pygame.display.set_caption(WIN_CFG['GAME_NAME'])  # 游戏名(窗口名)
        pygame.display.set_icon(pygame.image.load(WIN_CFG['ICON_PATH']))  # 窗口图标(需要有路径)
        pygame.mouse.set_visible(False)  # 隐藏鼠标，改用一个鼠标图像替换
        pygame.mixer.init()  # 初始化声音模块
        self.mouse = self.newHWSurface(WIN_CFG['MOUSE_PATH'], True)  # 创建鼠标图像
        self.CLOCK = pygame.time.Clock()  # 实例化一个时钟类用来控制帧率等操作
        self.ALL_SHOW_DICT = {}  # 创建一个字典根据键值对来控制level的显示
        self.MOUSE_CD = True  # 鼠标冷却变量
        self.MOUSE_CD_COUNT = 0  # 鼠标冷却变量的计数器
        self.LoadLevelElement()
        self.FPS_font = pygame.font.SysFont('microsoftyahei', 15, False, False)
        self.run()

    def run(self):
        # 游戏循环
        while True:
            # 设置帧率
            self.CLOCK.tick(WIN_CFG['FPS'])
            # print('%.2f' % self.CLOCK.get_fps())  # 在控制台输出当前帧率，精确两位小数
            # 游戏事件
            self.mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
            self.mouse_pressed = pygame.mouse.get_pressed()  # 获取鼠标按键状态
            self.key_pressed = pygame.key.get_pressed()  # 获取连续键盘事件
            self.key_event = pygame.event.get()  # 获取一次性键盘事件
            if not self.MOUSE_CD:  # 如果鼠标冷却为False则执行鼠标冷却控制器
                self.mouseCDController()
            self.LoadLevelEvent()  # 游戏事件
            # 游戏绘制
            self.SCREEN.fill((0, 0, 0))  # 绘制纯黑背景
            self.LoadLevelRender()  # 游戏内容绘制
            self.SCREEN.blit(self.FPS_font.render(str(self.CLOCK.get_fps())[0:2], True, (255, 0, 0), None), (0, 0))  # 绘制帧率
            self.SCREEN.blit(self.mouse, self.mouse_pos)  # 绘制鼠标图像
            # 画面刷新
            pygame.display.flip()

if __name__ == '__main__':
    Game()