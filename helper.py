""" Helper functions. 

    Intializes by getting position of top-left corner of the game. 
"""

import pyautogui
# get the game corner coordinates
CORNER = None
print('searching for corner...')
while CORNER == None:
    CORNER = pyautogui.locateOnScreen('images/ingame-corner.png')
    if CORNER == None:
        print('could not find top-left corner')
print('success')
# our coordinates are shifted 25 px up because of steam border

# lower pyautogui.PAUSE constant for more efficiency
pyautogui.PAUSE = 0.01


def getCoords(x, y):
    """ Return coordinates relative to top-left corner. """
    return (CORNER[0] + x, CORNER[1] + y - 25)


def moveTo(x, y):
    """ Move mouse to coordinates x, y in-game. """
    x = CORNER[0] + x
    y = CORNER[1] + y - 25
    pyautogui.moveTo(x, y)


def rawMove(x, y):
    """ Move mouse to absolute coordinates x, y. """
    pyautogui.moveTo(x, y)


def rawClick(x, y, button="left"):
    """ Click on absolute coordinates x, y. """
    pyautogui.click(x, y, button=button)


def click(x, y, button="left"):
    """ Click on coordinates x, y relative to top-left corner. """
    moveTo(x, y)
    pyautogui.click(button=button)
    sleep(0.2)


def ctrlClick():
    """ Control click on current mouse position. """
    pyautogui.keyDown('ctrl')
    sleep(0.3)
    pyautogui.click()
    sleep(0.3)
    pyautogui.keyUp('ctrl')


def sleep(time):
    """ Sleeps for {time} amount of seconds. """
    pyautogui.sleep(time)
