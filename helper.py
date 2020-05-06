""" Helper functions. 

    Intializes by getting position of top-left corner of the game. 
"""

from typing import List, Set, Dict, Tuple

# import d3dshot
import pyautogui

import constants

# get the game corner coordinates
CORNER = None
print('searching for corner...')
while CORNER == None:
    CORNER = pyautogui.locateOnScreen('images/ingame-corner.png')
    if CORNER == None:
        print('could not find top-left corner')
print('success')
# our coordinates are shifted 25 px up because of steam border

# normalize to standard int:
CORNER = list(map(int, CORNER))

# lower pyautogui.PAUSE constant
pyautogui.PAUSE = 0.01


def rawMove(x: int, y: int) -> None:
    """ Move mouse to absolute coordinates x, y. 

    This method does not use getCoords.
    """
    pyautogui.moveTo(x, y)


def rawClick(x: int, y: int, button: str = "left") -> None:
    """ Click on absolute coordinates x, y. 

    Keyword arguments:  
    button -- left or right.
    """
    pyautogui.click(x, y, button=button)


def sleep(time: int) -> None:
    """ Sleep for x amount of seconds. """
    pyautogui.sleep(time)


def getCoords(x: int, y: int) -> Tuple[int, int]:
    """ Return coordinates relative to top-left corner of the game. """

    # due to pyautogui and opencv interation, CORNER returns a box with numpy.int64 type numbers.
    # this breaks all other parts of the code and pyautogui itself.
    # as a workaround, I recast every coordinate as standard int.
    return (int(CORNER[0] + x), int(CORNER[1] + y - 25))


def getRegion(x: int, y: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
    """ Return coordinates for a region of the screen normalized by the game corner. """
    x, y = getCoords(x, y)
    return (int(x), int(y), int(x2), int(y2))


def moveTo(x: int, y: int) -> None:
    """ Move mouse to coordinates x, y relative to game. """
    x, y = getCoords(x, y)
    pyautogui.moveTo(x, y)


def click(x: int, y: int, button: str = "left", delay: str = "medium") -> None:
    """ Click on coordinates x, y relative to game. 

    Keyword arguments:  
    button -- left or right.  
    delay -- time to wait after click: fast, medium or long.  
    """
    moveTo(x, y)
    pyautogui.click(button=button)
    if delay == "fast":
        sleep(constants.FAST_SLEEP)
    elif delay == "medium":
        sleep(constants.MEDIUM_SLEEP)
    elif delay == "long":
        sleep(constants.LONG_SLEEP)


def ctrlClick() -> None:  # TODO add coordinates
    """ Control click on current mouse position. """
    pyautogui.keyDown('ctrl')
    sleep(0.3)
    pyautogui.click()
    sleep(0.3)
    pyautogui.keyUp('ctrl')


def press(letters: str, delay: int = 0) -> None:
    """ Send letters to window. 

    Keyword arguments:  
    delay -- optional delay between letters, in seconds.
    """
    for letter in letters:
        pyautogui.press(letter)
        if delay:
            pyautogui.sleep(delay)


def getScreenshot2():  # TODO
    """ Get and return screenshot of actual screen. 

    Uses d3dshot module instead of pyautogui. 
    """
    d = d3dshot.create()
    return d.screenshot()


def getScreenshot(region: Tuple[int, int, int, int] = None) -> None:
    """ Get screenshot of actual screen. 

    To be used with get pixel color when you want to get multiple pixels at the same time.
    """
    if region:
        x, y = getCoords(region[0], region[1])
        region = (x, y, region[2], region[3])
        return pyautogui.screenshot(region=region)

    return pyautogui.screenshot()


def getPixelColor(x: int, y: int, image=None) -> None:
    """ Get color of pixel at (x, y) (relative). 

    Keyword arguments:  
    image -- screenshot, if you want to get multiple pixels with the same image. 
    """
    pix = getCoords(x, y)
    if image:
        return image.getpixel(pix)
    return pyautogui.pixel(*pix)


if __name__ == '__main__':
    print(f'debugging: ')
    print(f'CORNER: {CORNER}')
    print(f'CORNER[0] = {CORNER[0]}')
    print(f'type: {type(CORNER[0])}')
    for x in CORNER:
        print(x)
    # print(f'should work: ')
    # pyautogui.pixelMatchesColor(100, 100, (255, 255, 255))
    # print(f'should not work: ')
    # pyautogui.pixelMatchesColor(*getCoords(100, 100), (255, 255, 255))
