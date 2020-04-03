""" Helper functions. """

import pyautogui
# get the game corner coordinates
CORNER = None
print('searching for corner...')
while CORNER == None:
    CORNER = pyautogui.locateOnScreen('ingame-corner.png')
print('success')
# our coordinates are shifted 25 px up because of steam border

# lower pyautogui.PAUSE constant for more efficiency
pyautogui.PAUSE = 0.01


def getCoords(x, y):
    return (CORNER[0] + x, CORNER[1] + y - 25)


def moveTo(x, y):
    x = CORNER[0] + x
    y = CORNER[1] + y - 25
    pyautogui.moveTo(x, y)


def rawMove(x, y):
    pyautogui.moveTo(x, y)


def rawClick(x, y, button="left"):
    pyautogui.click(x, y, button=button)


def click(x, y, button="left"):
    moveTo(x, y)
    pyautogui.click(button=button)
    sleep(0.2)


def sleep(time):
    pyautogui.sleep(time)
