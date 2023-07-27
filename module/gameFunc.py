# --coding=utf-8
import sys
import pygame
# 配置文件
from config import GAME_CONFIG as GM_CFG

class GameFuncClass:
    def newHWSurface(self, img_path, is_alpha, size=(0, 0)):
        """
        创建一个带有硬件加速的surface图片图像
        原理:因为pygame创建图片surface不能直接开启硬件加速，
            所以需要创建一个开启硬件加速的独立surface对象，
            然后将图片surface绘制到硬加surface上，
            使用时直接使用硬加surface即可，
            这样操作能显著提高绘制速度、游戏性能。
        :param img_path: str 需要加载的图片路径
        :param size: tuple 图像大小
        :param is_alpha: bool 是否开启alpha透明通道
        :return: 一个开启硬加的surface对象
        """
        try:
            if size == (0, 0):
                size = pygame.image.load(str(img_path)).get_size()
            temp_surface = pygame.transform.scale(pygame.image.load(str(img_path)), tuple(size))
            if is_alpha:
                complete_surface = pygame.Surface(tuple(size), flags=pygame.HWSURFACE).convert_alpha()
                complete_surface.fill((0, 0, 0, 0))
            else:
                complete_surface = pygame.Surface(tuple(size), flags=pygame.HWSURFACE).convert()
            complete_surface.blit(temp_surface, (0, 0))
            return complete_surface
        except Exception as e:
            # 如果找不到目标图片路径
            # 则返回一个代表报错的图像surface
            temp_surface = pygame.transform.scale(pygame.image.load(GM_CFG['CANNOT_FIND_IMG']), tuple(size))
            complete_surface = pygame.Surface(tuple(size), flags=pygame.HWSURFACE).convert()
            complete_surface.blit(temp_surface, (0, 0))
            return complete_surface

    def playMusic(self, music_path, music_volume, play_count=1):
        """
        音乐播放函数，可以设置播放的音乐、音量和次数
        :param music_path: str 需要加载的音乐路径
        :param music_volume: int float 音量大小
        :param play_count: int 播放次数，负数为循环播放
        :return: 无
        """
        try:
            pygame.mixer.music.load(str(music_path))  # 加载音乐
            pygame.mixer.music.set_volume(music_volume)  # 设置音量
            pygame.mixer.music.play(play_count)  # 播放次数
        except Exception as e:
            # 如果音乐路径错误导致找不到音乐文件
            # 则播放提醒音效
            pygame.mixer.music.load("media/sound/You Suffer.ogg")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    def changeLevelShow(self, level_key):
        """
        改变层显示键的函数
        原理：循环取出字典中的键，然后根据键来改变相应的值
        :param level_key: 需要改为或保留True值的level键的值
        :return: 无
        """
        try:
            for k in self.ALL_SHOW_DICT.keys():
                self.ALL_SHOW_DICT[k] = False
            self.ALL_SHOW_DICT[level_key] = True
        except KeyError as e:
            # 如果找不到相应key则不做出任何改变
            pass

    def changeLevelShowAndExecFunc(self, level_key, func_name):
        """
        改变层显示键并同时执行一些方法的的函数
        :param level_key: 需要改为或保留True值的level键的值
        :param func_name: 函数名，不加括号
        :return:
        """
        try:
            for k in self.ALL_SHOW_DICT.keys():
                self.ALL_SHOW_DICT[k] = False
            self.ALL_SHOW_DICT[level_key] = True
            func_name()
        except KeyError as e:
            # 如果找不到相应key则不做出任何改变
            pass

    def quitGame(self, is_save):
        """
        退出游戏并根据传参判断是否保存当前游戏存档
        :param is_save: bool 是否保存游戏存档
        :return: 无
        """
        if is_save:
            # 此处暂留位置以后用来编写保存游戏存档的代码
            pygame.quit()
            sys.exit()
        else:
            pygame.quit()
            sys.exit()

    def mouseCDController(self):
        """
        鼠标冷却控制器
        功能：当鼠标冷却为False时，每帧对计数器进行累加，直至设置文件中规定的cd值，才能将鼠标冷却改为True
        :return: 无
        """
        if self.MOUSE_CD_COUNT == GM_CFG['MOUSE_CLICK_CD']:
            self.MOUSE_CD = True
            self.MOUSE_CD_COUNT = 0
        else:
            self.MOUSE_CD_COUNT += 1

    def createSound(self, sound_path, sound_volume):
        """
        创建sound音效对象
        :param sound_path: str 音效文件路径
        :param sound_volume: int float 声音大小
        :return: 一个创建好的pygame.mixer.Sound()对象
        """
        try:
            temp_sound = pygame.mixer.Sound(str(sound_path))
            temp_sound.set_volume(sound_volume)
            return temp_sound
        except Exception as e:
            # 如果音乐路径错误导致找不到音乐文件, 则使用提醒音效
            temp_sound = pygame.mixer.Sound("media/sound/You Suffer.ogg")
            return temp_sound