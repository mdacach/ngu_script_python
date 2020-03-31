""" Module for various features handling."""

from helper import *
from coords import *
import time


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
    zones = {'safe': 0,
             'tutorial': 1,
             'sewers': 2,
             'forest': 3,
             'cave': 4,
             'sky': 5,
             'hsb': 6,
             'grb': 7}

    @staticmethod
    def itopodFarm(floor='optimal'):
        click(*ADVENTURE)
        click(*ITOPOD_ENTER)
        if floor == 'optimal':
            click(*ITOPOD_OPTIMAL)
        click(*ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def itopodPush(floor='200'):
        """floor is a string representing the floor number"""
        click(*ADVENTURE)
        click(*ITOPOD_ENTER)
        click(*ITOPOD_MAX)
        click(*ITOPOD_END_INPUT)
        pyautogui.write(floor, interval=0.2)
        click(*ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def adventureZone(zone='latest'):
        click(*ADVENTURE)
        click(*GO_BACK_ZONE, button="right")   # start at 0
        if zone == 'latest':
            click(*ADVANCE_ZONE, button="right")
        else:
            times = Adventure.zones[zone]
            for _ in range(times):
                click(*ADVANCE_ZONE)

    @staticmethod
    def sendAttacks():
        pyautogui.press('y')
        pyautogui.press('t')
        pyautogui.press('r')
        pyautogui.press('e')
        pyautogui.press('w')

    @staticmethod
    def killTitan():  # for grb currently
        click(*ADVENTURE)
        click(*ADVANCE_ZONE, button="right")
        click(*ADVANCE_ZONE)
        pyautogui.press('q')
        # grb health bar color is not red
        enemy_hp = getCoords(*ENEMY_HEALTH_BAR)
        sleep(6)
        if not pyautogui.pixelMatchesColor(*enemy_hp, (255, 255, 255)):
            print('grb spawned')
            start = time.time()
            while not Adventure.isEnemyDead() or (time.time() - start)/60 < 3:
                Adventure.sendAttacks()
                sleep(0.1)
        pyautogui.press('q')

    @staticmethod
    def killMonsters(zone='latest', bossOnly=False, kills=20):
        Adventure.adventureZone(zone)
        pyautogui.press('q')  # idle mode
        counter = 0
        currentZone = zone
        while True:
            if currentZone == 'safe':
                Adventure.adventureZone(zone)
                currentZone = zone
            # print('checking spawn')
            if Adventure.enemySpawn():
                # print('spawned')
                if (not bossOnly):
                    Adventure.kill()
                    if Adventure.isPlayerLow():
                        Adventure.healHP()
                        currentZone = 'safe'
                    counter += 1
                    sleep(1)
                    pyautogui.press('d')  # heal
                else:
                    if Adventure.isBoss():
                        Adventure.kill()
                        if (Adventure.isPlayerLow()):
                            Adventure.healHP()
                            currentZone = 'safe'
                        counter += 1
                        sleep(1)
                        pyautogui.press('d')  # heal
                    else:
                        Adventure.refreshZone()
            else:
                sleep(0.1)  # wait a little
            if (counter > 0 and counter % kills == 0):
                pyautogui.press('q')  # after 15 fights
                return

    @staticmethod
    def kill():
        while not Adventure.isEnemyDead():
            Adventure.sendAttacks()
            sleep(0.1)
        # after this, player may be dead

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
        Adventure.adventureZone('safe')
        sleep(25)
        # click(*ADVANCE_ZONE, button="right")

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


class TimeMachine:
    @staticmethod
    def addEnergy():
        click(*TIME_MACHINE)
        click(*TM_ADD_ENERGY)

    @staticmethod
    def addMagic():
        click(*TIME_MACHINE)
        click(*TM_ADD_MAGIC)


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
