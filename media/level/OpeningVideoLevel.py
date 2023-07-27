# --coding=utf-8

# 模块
import pygame
import cv2
import numpy as np
import random
# 游戏文件
from config import WINDOW_CONFIG as WIN_CFG  # 游戏窗口配置文件
from config import GAME_CONFIG as GM_CFG  # 游戏内容配置文件
from module.gameFunc import GameFuncClass as GMF  # GMF:游戏函数类

class OpeningVideoLevel(GMF):
    def openingVideoElement(self):
        self.ALL_SHOW_DICT['OpeningVideo'] = False
        video_file = "./media/video/Scoundrel CG.mp4"
        self.video_cap = cv2.VideoCapture(video_file)  # 使用cv2读取视频
        self.video_play_count = 0  # 计数器
        self.video_play_done = False  # 视频是否播放完毕

    def openingVideoEvent(self):
        if self.ALL_SHOW_DICT['OpeningVideo']:
            for event in self.key_event:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.fadeout(2000)  # 2000毫秒音乐淡出时间
                        self.changeLevelShowAndExecFunc('MainMenu', self.goToMainMenuLevelFunc)
            if not self.video_play_done:
                # 如果视频没有播放完毕则继续控制器操作
                # 反之则停止控制器继续操作
                self.openingVideoPlayController()
            else:
                # 如果视频播放完毕则暂停音乐
                pygame.mixer.music.fadeout(2000)  # 2000毫秒音乐淡出时间
                # 跳转到下一个MainMenu层
                self.changeLevelShowAndExecFunc('MainMenu', self.goToMainMenuLevelFunc)
            for event in self.key_event:  # 窗口关闭事件检测
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # 按下esc退出游戏
                        self.quitGame(False)

    def openingVideoRender(self):
        if self.ALL_SHOW_DICT['OpeningVideo']:
            self.SCREEN.blit(self.frame, (0, 0))

    def openingVideoPlayController(self):
        """
        视频播放控制器函数
        注意！！！   注意！！！   注意！！！  注意！！！   注意！！！   注意！！！  注意！！！   注意！！！   注意！！！
            经测试证明，视频播放帧率与显卡性能关联很大，无论是核显还是独立显卡，如果想要游戏帧率稳定运行，尽量关闭一些不必要的显卡使用程序。
            实验经历：一次作者开发游戏的时候，同时开着模拟器在玩着游戏
                    然后在测试游戏的时候发现播放视频时帧率始终固定在40帧左右(额定是60帧)
                    后来关掉模拟器再进行测试时，播放视频的时候帧率提升到了50帧
                    明显提高了许多
            tips: 其实作者的电脑是核显，性能不太行，所以可能在游戏测试的时候会略逊一些，不过这也让我深刻的认识到游戏优化的重要性，我会尽力优化游戏性能的，非常感谢大家的游玩
        :return: 无
        """
        if self.video_play_count == 0:
            self.ret, self.frame = self.video_cap.read()
            if self.ret:
                '''
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.frame = cv2.transpose(self.frame)
                self.frame = pygame.surfarray.make_surface(self.frame)
                self.frame = pygame.transform.scale(self.frame, (1600, 900))
                '''
                self.frame = pygame.transform.scale(pygame.surfarray.make_surface(cv2.transpose(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))), WIN_CFG['FULL_SIZE'])
                self.video_play_count = 1
            else:
                self.frame = pygame.Surface(WIN_CFG['FULL_SIZE'], flags=pygame.HWSURFACE).convert()
                self.frame.fill((0, 0, 0))
                self.video_play_done = True
        elif self.video_play_count == 1:
            self.video_play_count = 0

    def goToMainMenuLevelFunc(self):
        """
        去往MainMenu层时执行的代码
        :return: 无
        """
        # 改变背景音乐
        bgm_file = "./media/music/" + random.choice(GM_CFG['MainMenu_BGM_LIST'])  # 随机挑选一首背景音乐
        self.playMusic(bgm_file, 0.2, -1)