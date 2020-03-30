""" Module for various features handling."""

from helper import *
from coords import *


class BasicTraining:
    @staticmethod
    def basicTraining():
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


class FightBosses:
    @staticmethod
    def fightBosses():
        click(*FIGHT_BOSS)
        click(*NUKE)
        for _ in range(5):  # wait for boss to die
            pyautogui.sleep(2)
            click(*FIGHT)


class Adventure:
    @staticmethod
    def adventureZone():
        click(*ADVENTURE)
        click(*ADVANCE_ZONE, button="right")

    @staticmethod
    def farmZone(time):
        Adventure.adventureZone()
        sleep(0.5)
        pyautogui.press('q')
        sleep(0.5)
        for i in range(time):
            pyautogui.press('y')
            pyautogui.press('t')
            pyautogui.press('r')
            pyautogui.press('e')
            pyautogui.press('w')
            pyautogui.sleep(1)
        sleep(0.5)
        pyautogui.press('q')
        sleep(0.5)

    @staticmethod
    def sendAttacks():
        pyautogui.press('y')
        pyautogui.press('t')
        pyautogui.press('r')
        pyautogui.press('e')
        pyautogui.press('w')

    @staticmethod
    def killMonsters(bossOnly=False, kills=20):
        click(*ADVENTURE)
        click(*ADVANCE_ZONE, button="right")
        pyautogui.press('q')  # idle mode
        counter = 0
        while True:
            # print('checking spawn')
            if Adventure.enemySpawn():
                # print('spawned')
                if (not bossOnly):
                    while (not Adventure.isEnemyDead()):
                        # print('attacking')
                        if (Adventure.isPlayerLow()):
                            Adventure.healHP()
                        Adventure.sendAttacks()
                        sleep(0.1)
                    counter += 1
                    pyautogui.press('d')  # heal
                else:
                    if isBoss():
                        while (not Adventure.isEnemyDead()):
                            # print('attacking')
                            if (Adventure.isPlayerLow()):
                                Adventure.healHP()
                            Adventure.sendAttacks()
                            sleep(0.1)
                        counter += 1
                        pyautogui.press('d')  # heal
                    else:
                        Adventure.refreshZone()
            else:
                sleep(0.1)
            if (counter > 0 and counter % kills == 0):  # after 15 fights
                return

    @staticmethod
    def isEnemyDead():
        border = getCoords(*ENEMY_HEALTH_BAR_BORDER)
        if (pyautogui.pixelMatchesColor(*border, (255, 255, 255))):
            # print('dead')
            return True
        else:
            return False
            # print('not dead')

    @staticmethod
    def isPlayerLow():
        border = getCoords(*MY_HEALTH_BAR)
        if (pyautogui.pixelMatchesColor(*border, (255, 255, 255))):
            return True
        else:
            return False

    @staticmethod
    def healHP():
        click(*GO_BACK_ZONE, button="right")
        sleep(10)
        click(*ADVANCE_ZONE, button="right")

    @staticmethod
    def enemySpawn():
        enemy_hp = getCoords(*ENEMY_HEALTH_BAR_BORDER)
        return pyautogui.pixelMatchesColor(*enemy_hp, HEALTH_BAR_RED)

    @staticmethod
    def reclaimEnergy():
        click(*BASIC_TRAINING)
        pyautogui.press('r')  # should reclaim energy

    @staticmethod
    def isBoss():
        # get the pixel of the crown
        # match it with yellow
        crown = getCoords(*CROWN_LOCATION)
        return pyautogui.pixelMatchesColor(*crown, CROWN_COLOR)

    @staticmethod
    def refreshZone():
        click(*GO_BACK_ZONE)
        click(*ADVANCE_ZONE)


class Augmentation:
    @staticmethod
    def augmentation(upgrade=False):
        click(*AUGMENTATION)
        if upgrade:
            click(*AUG1_UPGRADE)
        else:
            click(*AUG1)


class Inventory:
    @staticmethod
    def mergeItem(x, y):
        moveTo(x, y)
        pyautogui.press('d')

    @staticmethod
    def boostItem(x, y):
        moveTo(x, y)
        pyautogui.press('a')

    @staticmethod
    def boostAndMergeEquips():
        click(*INVENTORY)

        Inventory.mergeItem(*HEAD)
        Inventory.mergeItem(*CHEST)
        Inventory.mergeItem(*LEGS)
        Inventory.mergeItem(*BOOTS)
        Inventory.mergeItem(*WEAPON)
        Inventory.mergeItem(*ACC1)
        Inventory.mergeItem(*ACC2)
        Inventory.boostItem(*HEAD)
        Inventory.boostItem(*CHEST)
        Inventory.boostItem(*LEGS)
        Inventory.boostItem(*BOOTS)
        Inventory.boostItem(*WEAPON)
        Inventory.boostItem(*ACC1)
        Inventory.boostItem(*ACC2)

        for i in range(12):  # boost and merge front row
            x = SLOT1[0] + INV_DIFF * i
            y = SLOT1[1]
            Inventory.mergeItem(x, y)
            Inventory.boostItem(x, y)

        click(*CUBE, button="right")  # boost infinity cube


class MoneyPit:
    @staticmethod
    def moneyPit():
        click(*MONEY_PIT)
        click(*FEED_ME)
        click(*FEED_YEAH)


class Rebirth:
    @staticmethod
    def rebirth():
        click(*REBIRTH_MENU)
        sleep(5)  # to see if it's crashing
        click(*REBIRTH_BUTTON)
        click(*REBIRTH_CONFIRMATION)


class Misc:
    @staticmethod
    def reclaimEnergy():
        click(*BASIC_TRAINING)
        pyautogui.press('r')
