""" Helper functions. 

    Intializes by getting position of top-left corner of the game. 
"""

import pyautogui
import d3dshot
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


def sleep(time):
    """ Sleeps for {time} amount of seconds. """
    pyautogui.sleep(time)


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


def click(x, y, button="left", delay="medium"):
    """ Click on coordinates x, y relative to top-left corner. 

    Keyword arguments:  
    button -- button to click. {left, right}  
    delay -- time to wait after click {fast, medium}.  
    """
    moveTo(x, y)
    pyautogui.click(button=button)
    if delay == "medium":
        sleep(0.3)
    elif delay == "fast":
        sleep(0.1)


def ctrlClick():
    """ Control click on current mouse position. """
    pyautogui.keyDown('ctrl')
    sleep(0.3)
    pyautogui.click()
    sleep(0.3)
    pyautogui.keyUp('ctrl')


def press(letters, delay=0):
    """ Send letters to window. 

    Keyword arguments:  
    delay -- optional delay between letters, in seconds.
    """
    for letter in letters:
        pyautogui.press(letter)
        if delay:
            pyautogui.sleep(delay)


def getScreenshot2():
    """ Get and return screenshot of actual screen. 

    Uses d3dshot module instead of pyautogui. 
    """
    d = d3dshot.create()
    return d.screenshot()


def getScreenshot(region=None):
    """ Get screenshot of actual screen. 

    To be used with get pixel color when you want to get multiple pixels at the same time.
    """
    if region:
        x, y = getCoords(region[0], region[1])
        region = (x, y, region[2], region[3])
        return pyautogui.screenshot(region=region)

    return pyautogui.screenshot()


def getPixelColor(x, y, image=None):
    """ Get color of pixel at (x, y) (relative). 

    Keyword arguments:  
    image -- screenshot, if you want to get multiple pixels. """
    pix = getCoords(x, y)
    if image:
        return image.getpixel(pix)
    return pyautogui.pixel(*pix)
