import pyautogui
from helper import *
import pytesseract as ocr
from PIL import Image


class Statistics:
    @staticmethod
    def screenshot():
        img = pyautogui.screenshot(
            region=(CORNER[0], CORNER[1], GAME_WIDTH, GAME_HEIGHT))
        img.save('game-screenshot.png')
