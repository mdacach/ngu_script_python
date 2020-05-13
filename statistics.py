""" Statistics module. """
from typing import Tuple
import time

import pyautogui
import mss 

import coords 
from helper import *
import pytesseract as ocr
from PIL import Image
from navigation import Navigation
from features import * 


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
        with mss.mss() as sct:
            monitor = {}
            monitor["left"], monitor["top"], monitor["width"], monitor["height"] = region 
            img = sct.grab(monitor)
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX") # from mss docs 
            return img
        # TODO SAVE
        # # print(f'region: {region}')
        # if save:
        #     pyautogui.screenshot("output/" + name, region=region)
        # return pyautogui.screenshot(region=region)

    @staticmethod 
    def getPixelColor(x, y):
        """ Get and return pixel color at x, y. """ 
        img = Statistics.getScreenshot() 
        return img.getpixel((x, y-25)) # screenshot does not have steam border (~25pixels)

    @staticmethod 
    def checkPixelColor(x, y, color, threshold=5):
        """ Check if pixel x, y has color z. """ 
        # print(Statistics.getPixelColor(x, y), color)
        pix = Statistics.getPixelColor(x, y) 
        for c1, c2 in zip(pix, color):
            if abs(c1 - c2) > threshold: 
                return False 
        return True 

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
    print(Statistics.getScreenshot())
    
