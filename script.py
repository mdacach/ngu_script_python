import pyautogui
from coords import *

# get corner pixel
CORNER = pyautogui.locateOnScreen("ingame-corner.png")


def click(coords, button="left"):
    x = CORNER[0] + coords[0]
    y = CORNER[1] + coords[1] - 25
    pyautogui.click(x, y, button=button)
    pyautogui.sleep(0.5)


def main():
    pyautogui.PAUSE = 0.01
    pyautogui.sleep(1.5)
    while True:
        for i in range(3):
            handleTraining()
            fightBosses()
            farmAdventure()
            handleEquips()
            for i in range(3):
                countdown(30)
                handleTraining()
            adventure(180)
            handleTraining()
            fightBosses()
            adventure(180)
        handleTraining()
        handleAugments()
        adventure(180)
        handleEquips()
        countdown(30)
        adventure(180)
        handleEquips()
        fightBosses()
        rebirth()


def rebirth():
    click(REBIRTH_MENU)
    pyautogui.sleep(20)
    click(REBIRTH_BUTTON)
    click(REBIRTH_CONFIRMATION)
    print("rebirth")


def adventure(time):
    farmAdventure()
    pyautogui.press('q')
    for i in range(time):
        pyautogui.press('y')
        pyautogui.press('t')
        pyautogui.press('r')
        pyautogui.press('e')
        pyautogui.press('w')
        pyautogui.sleep(1)
    pyautogui.press('q')


def countdown(time):
    pyautogui.sleep(time/3)
    print('sleeping...')
    pyautogui.sleep(time/3)
    print('sleeping ',  time/3)
    pyautogui.sleep(time/3)


def handleTraining():
    click(BASIC_TRAINING)
    click(ATK1)
    click(DEF1)
    click(ATK2)
    click(DEF2)
    click(ATK3)
    click(DEF3)
    click(ATK4)
    click(DEF4)
    click(DEF5)
    click(ATK5)


def handleAugments():
    click(AUGMENTATION)
    click(AUG1)


def fightBosses():
    click(FIGHT_BOSS)
    click(NUKE)
    for i in range(5):
        pyautogui.sleep(2)
        click(FIGHT)


def farmAdventure():
    click(ADVENTURE)
    click(ADVANCE_ZONE, button="right")


def handleEquips():
    click(INVENTORY)
    mergeItem(*HEAD)
    mergeItem(*CHEST)
    mergeItem(*LEGS)
    mergeItem(*BOOTS)
    mergeItem(*WEAPON)
    mergeItem(*ACC1)
    mergeItem(*ACC2)
    boostItem(*HEAD)
    boostItem(*CHEST)
    boostItem(*LEGS)
    boostItem(*BOOTS)
    boostItem(*WEAPON)
    boostItem(*ACC1)
    boostItem(*ACC2)

    x = SLOT1[0]
    y = SLOT1[1]

    for i in range(12):
        for j in range(3):
            mergeItem(x + INV_DIFF * i, y + INV_DIFF * j)
            boostItem(x + INV_DIFF * i, y + INV_DIFF * j)


def mergeItem(x, y):
    global CORNER
    pyautogui.moveTo(CORNER[0] + x, CORNER[1] + y - 25)
    pyautogui.press('d')


def boostItem(x, y):
    global CORNER
    pyautogui.moveTo(CORNER[0] + x, CORNER[1] + y - 25)
    pyautogui.press('a')


if __name__ == "__main__":
    main()
