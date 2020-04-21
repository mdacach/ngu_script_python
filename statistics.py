""" Statistics module. """
import pyautogui
import d3dshot
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
        """ Get the current pp amount from itopod. 

        Uses d3dshot for screenshot. 
        """
        Navigation.menu('adventure')
        click(*ITOPOD_PERKS)
        x, y = getCoords(ITOPOD_PP_REGION[0], ITOPOD_PP_REGION[1])
        d = d3dshot.create()
        image = d.screenshot(region=(x, y, x+100, y+30))
        print(image)
        image = d.screenshot_to_disk(
            file_name="pp-screenshot.png", region=(x, y, x+100, y+30))
        try:
            text = ocr.image_to_string(image)
        except:
            print('could not read pp')
            text = 0
        pp = ""
        for letter in text:
            if str.isdigit(letter):
                pp += letter
        # print(f"{exp} exp")
        print(f'read {text}')
        try:
            return int(pp)
        except:
            print('could not return pp correctly')
            return -1
        # return exp
        # return f"{exp} exp"
