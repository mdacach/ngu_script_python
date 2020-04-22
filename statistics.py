""" Statistics module. """
import pyautogui
import d3dshot
import cv2
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
        # print(image)
        # image = d.screenshot_to_disk(
        #     file_name="pp-screenshot.png", region=(x, y, x+100, y+30))
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

    @staticmethod
    def getTierKills():
        """ Get and return itopod tier remaining kills to AP.

        Must be in ITOPOD menu.
        """
        # ONLY WORDS FOR TIERS ABOVE 150
        click(*ITOPOD_CLICK_TOOLTIP)
        x, y = getCoords(
            ITOPOD_TIER_COUNT_REGION[0], ITOPOD_TIER_COUNT_REGION[1])
        d = d3dshot.create(capture_output='numpy')
        # image = d.screenshot_to_disk(
        # file_name = "itopod-tier.png", region = (x, y, x + 77, y + 18))
        print(f"x: {x} y: {y}")
        # image = d.screenshot(region=(x, y, x + 77, y + 18))
        image = d.screenshot()
        # print(f'image before: {image}')
        # image = image.resize((50, 35))
        image = cv2.resize(image, None, fx=1.5, fy=1.5,
                           interpolation=cv2.INTER_CUBIC)
        # image.save('itopod-ss.png')
        print(f'image after: {image}')
        try:
            text = ocr.image_to_string(image)
        except:
            print('could not read itopod tier count')
            text = 0
        count = ""
        for letter in text:
            if str.isdigit(letter):
                count += letter
        print(f'read {text}')
        try:
            return int(count)
        except:
            print('could not read itopod tier count properly. returning 40')
            return -1


# (511, 49) -> (537, 142)
# # region (77, 20)
