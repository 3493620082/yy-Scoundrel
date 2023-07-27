# --coding=utf-8

import os
import pygame
# 游戏文件
from config import WINDOW_CONFIG as WIN_CFG  # 游戏窗口配置文件
from config import GAME_CONFIG as GM_CFG  # 游戏内容配置文件
from module.gameFunc import GameFuncClass as GMF  # GMF:游戏函数类

class OpeningAnimationLevel(GMF):
    def openingAnimationElement(self):
        self.ALL_SHOW_DICT['OpeningAnimation'] = False  # 添加开场动画层的显示键值对
        self.logos_list = []  # 用来存放各个logo图像的列表
        self.logos_list_is_none = False  # 判断列表是否为空的变量
        for logo_file in os.listdir(GM_CFG['LOGO_FILE_PATH']):  # 获取logo文件夹下所有文件名并循环取出进行操作
            if logo_file[-4:] == ".jpg" or logo_file[-4:] == ".png":  # 如果文件后缀名为图片格式则取出进行下一步操作
                img_file = GM_CFG['LOGO_FILE_PATH'] + logo_file
                self.logos_list.append({
                    'logo_surface' : self.newHWSurface(img_file, True),
                    'alpha_value' : 0,
                    'show' : False,
                    'is_done' : False
                })
        if len(self.logos_list) != 0:  # 如果列表不为空则继续
            self.logo_bg = pygame.Surface(WIN_CFG['FULL_SIZE'], flags=pygame.HWSURFACE).convert()  # 背景图片surface
            self.logo_bg.fill((0, 0, 0))  # 填充背景颜色
            # 对列表中的logo字典进行操作
            for logo in self.logos_list:
                logo['logo_rect'] = logo['logo_surface'].get_rect()  # 获取rect
                logo['logo_rect'].center = WIN_CFG['CENTER_SIZE']  # 设置rect屏幕居中
                logo['logo_surface'].set_alpha(logo['alpha_value'])  # 设置透明度
            self.logos_list_maxIndex = len(self.logos_list) - 1  # 获取列表的最大索引
            self.logos_list[0]['show'] = True  # 将第一个logo图像的显示值改为True
            self.openingAnimation_count = 0  # 计数器
            self.openingAnimation_logo_action_stage = 0  # 动画的当前动作阶段变量
            # music_path = "media/music/All For Love.mp3"  # 音乐路径
            # self.playMusic(music_path, 0.2, 1)  # 播放音乐
        else:  # 如果列表为空则改变logos_list_is_none变量的值
            self.logos_list_is_none = True
        # 改变显示变量的值
        self.changeLevelShow('OpeningAnimation')

    def openingAnimationEvent(self):
        if self.ALL_SHOW_DICT['OpeningAnimation']:
            if self.logos_list_is_none:
                # 如果值为True则直接跳转到开场动画层, 不再接着执行本层的代码
                self.changeLevelShowAndExecFunc('OpeningVideo', self.goToOpeningVideoLevelFunc)  # 跳转到开场视频层
            self.openingAnimationActionController()
            for event in self.key_event:  # 窗口关闭事件检测
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # 按下esc退出游戏
                        self.quitGame(False)

    def openingAnimationRender(self):
        if self.ALL_SHOW_DICT['OpeningAnimation']:
            self.SCREEN.blit(self.logo_bg, (0, 0))  # 首先绘制背景图片
            for logo in self.logos_list:
                self.SCREEN.blit(logo['logo_surface'], logo['logo_rect'])

    def openingAnimationActionController(self):
        """
        开场动画层的动作控制器函数
        待总结...
        :return: 无
        """
        for logo_dict in self.logos_list:
            if logo_dict['is_done']:
                if self.logos_list.index(logo_dict) == self.logos_list_maxIndex:  # 如果当前logo_dict是最后一个logo则结束开场动画层跳转到其它层
                    self.changeLevelShowAndExecFunc('OpeningVideo', self.goToOpeningVideoLevelFunc)  # 跳转到开场视频层
                    break
                continue
            if logo_dict['show']:
                if self.openingAnimation_logo_action_stage == 0:
                    logo_dict['alpha_value'] += 1
                    if logo_dict['alpha_value'] == 255:
                        self.openingAnimation_logo_action_stage = 1
                    logo_dict['logo_surface'].set_alpha(logo_dict['alpha_value'])
                elif self.openingAnimation_logo_action_stage == 1:
                    self.openingAnimation_count += 1
                    if self.openingAnimation_count == 180:
                        self.openingAnimation_count = 0
                        self.openingAnimation_logo_action_stage = 2
                elif self.openingAnimation_logo_action_stage == 2:
                    logo_dict['alpha_value'] -= 1
                    if logo_dict['alpha_value'] == 0:
                        self.openingAnimation_logo_action_stage = 0
                        logo_dict['show'] = False
                        logo_dict['is_done'] = True
                        # 获取下一位元素的索引
                        now_logo_index = self.logos_list.index(logo_dict)
                        # 如果当前索引就是最后一个索引则不再执行下面的代码
                        if now_logo_index == self.logos_list_maxIndex:
                            break
                        # 改变下一个logo_dict的show的值
                        self.logos_list[now_logo_index + 1]['show'] = True
                    logo_dict['logo_surface'].set_alpha(logo_dict['alpha_value'])

    def goToOpeningVideoLevelFunc(self):
        """
        去往OpeningVideo层时需要执行的函数
        :return: 无
        """
        # 改变
        # 改变背景音乐
        bgm_file = "./media/video/Scoundrel CG bgm.mp3"
        self.playMusic(bgm_file, 0.2, 1)