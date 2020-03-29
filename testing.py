from coords import *
import pyautogui
from script import CORNER, click


def getCoords(x, y):
    x = CORNER[0] + x
    y = CORNER[1] + y - 25
    return (x, y)
# we will use pixel matches color


def enemySpawn():
    enemy_hp = getCoords(*ENEMY_HEALTH_BAR)
    return pyautogui.pixelMatchesColor(*enemy_hp, HEALTH_BAR_RED)


def isBoss():
    # get the pixel of the crown
    # match it with yellow
    crown = getCoords(*CROWN_LOCATION)
    return pyautogui.pixelMatchesColor(*crown, CROWN_COLOR)


def refreshZone():
    click(*GO_BACK_ZONE)
    click(*ADVANCE_ZONE)


def main():
    while True:
        pyautogui.sleep(0.2)
        enemy_hp = getCoords(*ENEMY_HEALTH_BAR)
        # IMPORTANT: pixelMatchesColor is broken on python 3.8
        # we are running with python 3.7.5
        if (pyautogui.pixelMatchesColor(*enemy_hp, HEALTH_BAR_RED)):
            if (isBoss()):
                print('boss')
            else:
                refreshZone()


if __name__ == "__main__":
    main()
