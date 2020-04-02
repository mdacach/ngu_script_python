import pyautogui
from helper import *
from coords import *
import pytesseract as ocr
from PIL import Image


class Statistics:
    @staticmethod
    def screenshot():
        img = pyautogui.screenshot(
            region=(CORNER[0], CORNER[1], GAME_WIDTH, GAME_HEIGHT))
        img.save('game-screenshot.png')

    @staticmethod
    def getEXP():
        x, y = getCoords(EXP_REGION[0], EXP_REGION[1])
        img = pyautogui.screenshot(region=(x, y, 100, 20))
        # img.save('exp-screenshot.png')
        print(ocr.image_to_string(img))
