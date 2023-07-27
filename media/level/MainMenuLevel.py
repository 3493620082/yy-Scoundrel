# --coding=utf-8

import pygame
import random
# 游戏文件
from config import WINDOW_CONFIG as WIN_CFG  # 游戏窗口配置文件
from config import GAME_CONFIG as GM_CFG  # 游戏内容配置文件
from config import FONT_CONFIG as FT_CFG  # 游戏字体配置文件
from module.gameFunc import GameFuncClass as GMF  # GMF:游戏函数类
# 附属类文件
from media.level.MainMenuLevel_Func import MainMenuLevel_Func

class MainMenuLevel(GMF, MainMenuLevel_Func):
    def mainMenuElement(self):
        self.ALL_SHOW_DICT['MainMenu'] = False  # 添加游戏主界面层的显示键值对
        # 背景图片
        bg_file = "./media/image/background/" + random.choice(GM_CFG['MainMenu_BG_LIST'])  # 随机抽选背景图片
        self.mainMenu_bg = self.mainMenuImageSpecialScaleFunc(bg_file)  # 背景图片surface
        self.mainMenu_bg_rect = self.mainMenu_bg.get_rect()  # 获取rect
        self.mainMenu_bg_rect.center = WIN_CFG['CENTER_SIZE']  # 设置背景居中
        # 按钮选项
        self.mainMenu_textBtn_LIST = []  # 创建一个列表用来存放所有按钮(便于操作)
        mainMenu_textBtn_FONT = pygame.font.Font(FT_CFG['LI_SHU'], 50)  # 字体
        mainMenu_textBtn_COLOR = (0, 0, 0)  # 字体颜色
        mainMenu_textBtn_COLOR_ACT = (255, 255, 255)  # 选中字体时的颜色
        mainMenu_textBtn_literals = ["开始新历程", "读取过往", "游戏设置", "贡献者名单", "退出江湖"]  # literals: 文字
        x = WIN_CFG['FULL_SIZE'][0] * 0.1  # 按钮位置的x轴
        y = 0  # 第一个按钮的y轴
        spacing = 100  # 坐标间隔
        # 使用for循环创建文字的surface图像
        '''
                    Font().render()方法
                    参数1：str 具体文字，例如：开始游戏
                    参数2：bool 是否平滑(抗锯齿)
                    参数3：tuple 字体颜色，一个rgb元组，例如黑色(0, 0, 0)
                    参数4：tuple 字体背景颜色，当为None时候背景透明
                '''
        for literals in mainMenu_textBtn_literals:
            self.mainMenu_textBtn_LIST.append({
                'literals' : literals,  # 对应的文字
                'btn_surface' : mainMenu_textBtn_FONT.render(literals, True, mainMenu_textBtn_COLOR, None),  # surface图像
                'activity_surface' : mainMenu_textBtn_FONT.render(literals, True, mainMenu_textBtn_COLOR_ACT, None),  # 被选中时的字体颜色
                'activity' : False,  # 选中状态判断变量
            })
        for textBtn in self.mainMenu_textBtn_LIST:
            # 因为在上一个for循环中无法直接使用surface来获取rect，所以需要在结束后在开启一个for循环来创建rect对象以及设置位置
            textBtn['btn_rect'] = textBtn['btn_surface'].get_rect()  # 获取rect
            y += textBtn['btn_rect'].height + spacing
        y -= 130
        y = WIN_CFG['FULL_SIZE'][1] / 2 - y / 2
        for textBtn in self.mainMenu_textBtn_LIST:  # 给每个rect对象分别设置坐标
            index = self.mainMenu_textBtn_LIST.index(textBtn)
            if index == 0:
                textBtn['btn_rect'].x, textBtn['btn_rect'].y = x, y
            else:
                last_btn = self.mainMenu_textBtn_LIST[index - 1]['btn_rect']
                textBtn['btn_rect'].x, textBtn['btn_rect'].y = x, last_btn.y + last_btn.height + spacing
        # 按钮所绑定的事件
        mainMenu_textBtn_func = [self.MainMenuStartNewJourney,  # 开始新历程
                                 self.MainMenuReadThePast,      # 读取过往
                                 self.MainMenuGameSettings,     # 游戏设置
                                 self.MainMenuListOfAuthors,    # 贡献者名单
                                 self.MainMenuExitTheQuacks]    # 退出江湖
        for textBtn in self.mainMenu_textBtn_LIST:
            index = self.mainMenu_textBtn_LIST.index(textBtn)
            textBtn['Event'] = mainMenu_textBtn_func[index]
        # 按钮ui图像
        btn_ui_path = "./media/image/ui_img/"
        self.mainMenu_shuimo_btn_ui_20 = self.newHWSurface(btn_ui_path + "shuimo_btn_ui_alpha_20.png", True)
        self.mainMenu_shuimo_btn_ui_50 = self.newHWSurface(btn_ui_path + "shuimo_btn_ui_alpha_50.png", True)
        # 版本号图像
        self.mainMenu_version = pygame.font.Font(FT_CFG['LI_SHU'], 15).render(WIN_CFG['VERSION'], True, (0, 0, 0), None)
        self.mainMenu_version_rect = self.mainMenu_version.get_rect()
        self.mainMenu_version_rect.x = WIN_CFG['FULL_SIZE'][0] - self.mainMenu_version_rect.w
        self.mainMenu_version_rect.y = WIN_CFG['FULL_SIZE'][1] - self.mainMenu_version_rect.h
        # 按钮点击音效
        sound_path = "./media/sound/btn_hit.ogg"
        self.mainMenu_textBtn_click_sound = self.createSound(sound_path, 0.5)

    def mainMenuEvent(self):
        if self.ALL_SHOW_DICT['MainMenu']:
            for textBtn in self.mainMenu_textBtn_LIST:
                textBtn['activity'] = False
                if textBtn['btn_rect'].collidepoint(self.mouse_pos):  # 判断鼠标是否在按钮rect上方
                    textBtn['activity'] = True  # 更改选中状态为True
                    if self.mouse_pressed[0] and self.MOUSE_CD:  # 如果此时按下了鼠标左键则代表点击了按钮
                        self.mainMenu_textBtn_click_sound.play()  # 播放点击音效
                        self.MOUSE_CD = False  # 将鼠标冷却改为False
                        textBtn['Event']()  # 执行对应的事件函数
                # break  # 直接结束循环，因为鼠标不可能同时选中两个rect，后面的rect也就没必要判断了
                # 注释掉break的原因是我们需要将，除了被选中按钮以外的其它按钮都改为False，变为未选中状态

    def mainMenuRender(self):
        if self.ALL_SHOW_DICT['MainMenu']:
            self.SCREEN.blit(self.mainMenu_bg, self.mainMenu_bg_rect)  # 背景图片
            for textBtn in self.mainMenu_textBtn_LIST:  # 使用for循环将所有的surface都绘制出来
                if textBtn['activity']:  # 如果当前rect为选中状态则绘制选中surface
                    self.SCREEN.blit(self.mainMenu_shuimo_btn_ui_50, (textBtn['btn_rect'][0], textBtn['btn_rect'][1] - 10))
                    self.SCREEN.blit(textBtn['activity_surface'], textBtn['btn_rect'])
                else:
                    self.SCREEN.blit(self.mainMenu_shuimo_btn_ui_20, (textBtn['btn_rect'][0], textBtn['btn_rect'][1] - 10))
                    self.SCREEN.blit(textBtn['btn_surface'], textBtn['btn_rect'])
            self.SCREEN.blit(self.mainMenu_version, self.mainMenu_version_rect)  # 版本号图像

    def mainMenuImageSpecialScaleFunc(self, img_file):
        """
        将大尺寸图片更改至与屏幕分辨率相近的尺寸
        算法：
            1.以屏幕高度为标准，例如900px
            2.屏幕高度数据÷原图高度=比例值，例如900/1564≈0.575
            3.原图surface长宽×比例值=实际所需长宽，例如1564*0.575≈900,3520*0.575≈2024
            4.使用计算得到的实际所需长宽直接创建surface图像即可
        :param img_file: str 图片路径
        :return: surface 更改尺寸后的surface图像
        """
        try:
            source_size = pygame.image.load(str(img_file)).get_size()
            proportion = WIN_CFG['FULL_SIZE'][1] / source_size[1]
            proportion = round(proportion, 4)  # 截取比例后的4位小数
            width, height = source_size[0] * proportion, source_size[1] * proportion
            return self.newHWSurface(str(img_file), False, (width, height))
        except Exception as e:
            # 如果找不到图片返回提示图片
            return self.newHWSurface(str(GM_CFG['CANNOT_FIND_IMG']), False, WIN_CFG['FULL_SIZE'])