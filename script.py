import pyautogui
from coords import *
import time  # keep track of rebirth time

# get corner pixel
CORNER = pyautogui.locateOnScreen("ingame-corner.png")


# - 25 to account for ingame corner pixel
def moveTo(x, y):
    x = CORNER[0] + x
    y = CORNER[1] + y - 25
    pyautogui.moveTo


def click(x, y, button="left"):
    x = CORNER[0] + x
    y = CORNER[1] + y - 25
    pyautogui.click(x, y, button=button)
    pyautogui.sleep(0.5)


def main():
    pyautogui.PAUSE = 0.01
    print('*******************')
    print('initializing the script')
    pyautogui.sleep(1.5)
    counter = 0
    while True:
        start = time.time()
        print('*******************')
        print('start')

        print('basic loop 3 times')
        for i in range(3):
            handleTraining()
            fightBosses()
            farmAdventure()
            handleEquips()
            print('handle training 3 times')
            for i in range(3):
                pyautogui.sleep(30)
                handleTraining()
            adventure(180)
            handleTraining()
            fightBosses()
            adventure(180)
        print('final part')
        handleTraining()
        handleAugments()
        adventure(180)
        handleEquips()
        fightBosses()
        rebirth()
        end = time.time()
        print(f'rebirth {counter} time: {end - start}')
        counter += 1

        print('*******************')
        print()


def rebirth():
    click(*REBIRTH_MENU)
    pyautogui.sleep(20)
    print("going to rebirth")
    click(*REBIRTH_BUTTON)
    click(*REBIRTH_CONFIRMATION)
    print("rebirth")


def saveScreenshot():
    img = pyautogui.screenshot()
    img.save(r'rebirth-screen.png')


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


def handleTraining():
    click(*BASIC_TRAINING)
    click(*ATK1)
    click(*DEF1)
    click(*ATK2)
    click(*DEF2)
    click(*ATK3)
    click(*DEF3)
    click(*ATK4)
    click(*DEF4)
    click(*DEF5)
    click(*ATK5)


def handleAugments():
    click(*AUGMENTATION)
    click(*AUG1)


def fightBosses():
    click(*FIGHT_BOSS)
    click(*NUKE)
    for i in range(5):
        pyautogui.sleep(2)
        click(*FIGHT)


def farmAdventure():
    click(*ADVENTURE)
    click(*ADVANCE_ZONE, button="right")


def handleEquips():
    click(*INVENTORY)
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
