""" Module for various features handling."""

from helper import *
from coords import *


class BasicTraining:
    def basicTraining(self):
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
    def fightBosses(self):
        click(*FIGHT_BOSS)
        click(*NUKE)
        for _ in range(5):  # wait for boss to die
            pyautogui.sleep(2)
            click(*FIGHT)


class Adventure:
    def adventureZone(self):
        click(*ADVENTURE)
        click(*ADVANCE_ZONE, button="right")

    def farmZone(self, time):
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


class Augmentation:
    def augmentation(self, upgrade=False):
        click(*AUGMENTATION)
        if upgrade:
            click(*AUG1_UPGRADE)
        else:
            click(*AUG1)


class Inventory:
    def mergeItem(self, x, y):
        moveTo(x, y)
        pyautogui.press('d')

    def boostItem(self, x, y):
        moveTo(x, y)
        pyautogui.press('a')

    def boostAndMergeEquips(self):
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

        for i in range(12):  # boost and merge front row
            x = SLOT1[0] + INV_DIFF * i
            y = SLOT1[1]
            Inventory.mergeItem(x, y)
            Inventory.boostItem(x, y)

        click(*CUBE, button="right")  # boost infinity cube


class MoneyPit:
    def moneyPit(self):
        click(*MONEY_PIT)
        click(*FEED_ME)
        click(*FEED_YEAH)


class Rebirth:
    def rebirth(self):
        click(*REBIRTH_MENU)
        sleep(5)  # to see if it's crashing
        click(*REBIRTH_BUTTON)
        click(*REBIRTH_CONFIRMATION)


class Misc:
    def reclaimEnergy(self):
        click(*BASIC_TRAINING)
        pyautogui.press('r')
