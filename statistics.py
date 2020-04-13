""" Statistics module. """
import pyautogui
from helper import *
from coords import *
import pytesseract as ocr
from PIL import Image
from navigation import Navigation


class Statistics:
    @staticmethod
    def screenshot(name='game-screenshot.png'):
        """ Saves a screenshot of the game. """
        img = pyautogui.screenshot(
            region=(CORNER[0], CORNER[1], GAME_WIDTH, GAME_HEIGHT))
        img.save(name)

    @staticmethod
    def getEXP():
        """ Get current EXP from spend EXP menu. """
        Navigation.menu('exp')
        x, y = getCoords(EXP_REGION[0], EXP_REGION[1])
        img = pyautogui.screenshot(region=(x, y, 100, 20))
        # img.save('exp-screenshot.png')
        # print(ocr.image_to_string(img))
        try:
            text = ocr.image_to_string(img)
        except:
            print('could not read exp')
            return
        exp = ""
        for letter in text:
            if str.isdigit(letter):
                exp += letter
        # print(f"{exp} exp")
        try:
            return int(exp)
        except:
            print('could not return exp correctly')
            return -1
        # return exp
        # return f"{exp} exp"

    @staticmethod
    def getBoss():
        """ Get the next boss from Fight Boss menu. """
        x, y = getCoords(BOSS_NUMBER_REGION[0], BOSS_NUMBER_REGION[1])
        img = pyautogui.screenshot(region=(x, y, 80, 20))
        # img.save('exp-screenshot.png')
        # print(ocr.image_to_string(img))
        try:
            text = ocr.image_to_string(img)
        except:
            print('could not read boss number')
            return
        print(text)

    @staticmethod
    def getPP():
        """ Get the current pp amount from itopod. """
        # x, y
