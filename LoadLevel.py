# --coding=utf-8

import pygame
# level文件
from media.level.OpeningAnimationLevel import OpeningAnimationLevel
from media.level.OpeningVideoLevel import OpeningVideoLevel
from media.level.MainMenuLevel import MainMenuLevel

class LoadLevel(OpeningAnimationLevel,
                OpeningVideoLevel,
                MainMenuLevel):
    def LoadLevelElement(self):
        self.openingAnimationElement()  # 开场动画level
        self.openingVideoElement()
        self.mainMenuElement()

    def LoadLevelEvent(self):
        self.openingAnimationEvent()
        self.openingVideoEvent()
        self.mainMenuEvent()

    def LoadLevelRender(self):
        self.openingAnimationRender()
        self.openingVideoRender()
        self.mainMenuRender()