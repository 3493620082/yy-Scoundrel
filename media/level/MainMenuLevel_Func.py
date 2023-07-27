# --coding=utf-8

import pygame

class MainMenuLevel_Func:
    def MainMenuStartNewJourney(self):
        pass
    def MainMenuReadThePast(self):
        pass
    def MainMenuGameSettings(self):
        pass
    def MainMenuListOfAuthors(self):
        pass
    def MainMenuExitTheQuacks(self):
        """
        退出江湖按钮绑定的事件函数
        :return: 无
        """
        self.quitGame(False)  # 此处调用的是gameFunc类中的退出游戏函数，参数值为False，意为不保存游戏