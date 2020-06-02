""" Helper functions, including click, sleep, move. 
    
    Call Helper.init() at the start of every script to locate the left corner. 
"""

import time
from typing import List, Set, Dict, Tuple

import pyautogui

import constants

# get the game corner coordinates


class Helper:
    # global variable
    CORNER = None

    @staticmethod
    def init():

        print('searching for game left corner...')

        while Helper.CORNER == None:
            Helper.CORNER = pyautogui.locateOnScreen(
                'images/ingame-corner.png')
            if Helper.CORNER == None:
                print('could not find top-left corner, \nis the game fully visible?')

        print('success')
        # our coordinates are shifted 25 px up because of steam border

        # normalize to standard int:
        Helper.CORNER = list(map(int, Helper.CORNER))

        # lower pyautogui.PAUSE constant
        pyautogui.PAUSE = 0.01

    @staticmethod
    def printTime():
        print(time.strftime("%H:%M:%S", time.localtime()))

    @staticmethod
    def rawMove(x: int, y: int) -> None:
        """ Move mouse to absolute coordinates x, y. 

        This method does not use getCoords.
        """
        pyautogui.moveTo(x, y)

    @staticmethod
    def rawClick(x: int, y: int, button: str = "left") -> None:
        """ Click on absolute coordinates x, y. 

        Keyword arguments:  
        button -- left or right.
        """
        pyautogui.click(x, y, button=button)

    @staticmethod
    def sleep(time: int) -> None:
        """ Sleep for x amount of seconds. """
        pyautogui.sleep(time)

    @staticmethod
    def getCoords(x: int, y: int) -> Tuple[int, int]:
        """ Return coordinates relative to top-left corner of the game. """

        # due to pyautogui and opencv interation, CORNER returns a box with numpy.int64 type numbers.
        # this breaks all other parts of the code and pyautogui itself.
        # as a workaround, I recast every coordinate as standard int.
        return (int(Helper.CORNER[0] + x), int(Helper.CORNER[1] + y - 25))

    @staticmethod
    def getRegion(x: int, y: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
        """ Return coordinates for a region of the screen normalized by the game corner. """
        x, y = Helper.getCoords(x, y)
        return (int(x), int(y), int(x2), int(y2))

    @staticmethod
    def moveTo(x: int, y: int) -> None:
        """ Move mouse to coordinates x, y relative to game. """
        x, y = Helper.getCoords(x, y)
        pyautogui.moveTo(x, y)

    @staticmethod
    def click(x: int, y: int, button: str = "left", delay: str = "medium") -> None:
        """ Click on coordinates x, y relative to game. 

        Keyword arguments:  
        button -- left or right.  
        delay -- time to wait after click: fast, medium or long.  
        """
        Helper.moveTo(x, y)
        pyautogui.click(button=button)
        if delay == "fast":
            Helper.sleep(constants.FAST_SLEEP)
        elif delay == "medium":
            Helper.sleep(constants.MEDIUM_SLEEP)
        elif delay == "long":
            Helper.sleep(constants.LONG_SLEEP)

    @staticmethod
    def ctrlClick() -> None:  # TODO add coordinates
        """ Control click on current mouse position. """
        pyautogui.keyDown('ctrl')
        Helper.sleep(0.3)
        pyautogui.click()
        Helper.sleep(0.3)
        pyautogui.keyUp('ctrl')

    @staticmethod
    def press(letters: str, delay: float = 0) -> None:
        """ Send letters to window. 

        Keyword arguments:  
        delay -- optional delay between letters, in seconds.
        """
        for letter in letters:
            pyautogui.press(letter)
            if delay:
                pyautogui.sleep(delay)

    @staticmethod
    def write(letters: str, delay: float = 0):
        """ Write letters to window. """
        pyautogui.write(letters, interval=delay)
