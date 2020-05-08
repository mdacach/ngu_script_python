""" Statistics module. """
from typing import Tuple
import time

import pyautogui

import coords 
from helper import *
import pytesseract as ocr
from PIL import Image
from navigation import Navigation


class Statistics:
    @staticmethod
    def getScreenshot(
        name: str = 'game-screenshot.png',
        save: bool = False,
        region: Tuple[int, int, int, int] = None
    ) -> Image:
        """ Capture/save a screenshot of the game. 

        Keyword arguments:  
        name -- file name if saving. (default game-screenshot.png).  
        save -- set to True if want to save to disk also (will take two screenshots).  
        region -- region to take screenshot. If none, will take screenshot of all game screen.  
        """
        if region:
            region = getRegion(*region)
        else:  # all game screen
            region = (CORNER[0], CORNER[1],
                      coords.GAME_WIDTH, coords.GAME_HEIGHT)
        # print(f'region: {region}')
        if save:
            pyautogui.screenshot("output/" + name, region=region)
        return pyautogui.screenshot(region=region)

    @staticmethod 
    def removeLetters(text: str) -> int:
        """ Remove letters from string for OCR.  
        
        Keyword arguments:  
        text -- the text to use.  
        """ 
        text = [x for x in text if x.isdigit()]
        return int("".join(text))

    @staticmethod
    def getEXP():
        """ Get and return current EXP from spend EXP menu. """
        Navigation.menu('exp')
        img = Statistics.getScreenshot(region=coords.EXP_REGION)
        text = ocr.image_to_string(img)
        return Statistics.removeLetters(text)


    @staticmethod
    def getBoss() -> int:
        """ Get and return the boss number from Fight Boss menu. """
        img = Statistics.getScreenshot(save=True, region=coords.BOSS_NUMBER_REGION)
        text = ocr.image_to_string(img)
        return Statistics.removeLetters(text)

    @staticmethod
    def getPP(): # TODO 
        """ Get and return the current pp amount from itopod.  """ 
        img = Statistics.getScreenshot(region=coords.ITOPOD_PP_REGION)
        text = ocr.image_to_string(img)
        return Statistics.removeLetters(text)

    @staticmethod
    def getTierKills(): # TODO 
        """ Get and return itopod tier remaining kills to AP.

        Must be in ITOPOD menu.
        """
        # ONLY WORDS FOR TIERS ABOVE 150
        click(*coords.ITOPOD_CLICK_TOOLTIP)
        img = Statistics.getScreenshot(region=coords.ITOPOD_TIER_COUNT_REGION)
        text = ocr.image_to_string(img)
        return Statistics.removeLetters(text)


if __name__ == '__main__':
    print(Statistics.getTierKills())
    # N = 1 
    # for i in range(N):
    #     start = time.time() 
    #     pyautogui.screenshot() 
    #     end = time.time() 
    # print(f'average time for pyautogui: {round((end - start)/N, 3)}')
    # for i in range(N):
    #     start = time.time() 
    #     with mss() as sct:
    #         sct.shot() 
    #     end = time.time() 
    # print(f'average time for mss: {round((end - start)/N, 3)}')


