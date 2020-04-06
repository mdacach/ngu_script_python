""" Module for various features handling."""

from helper import *
from coords import *
import time


class BasicTraining:
    """ Basic training handling. """
    @staticmethod
    def basicTraining():
        """ Right clicks on add energy to ATK1.

            Requires training auto advance to be bought.
        """
        click(*BASIC_TRAINING)
        click(*BASIC_TRAINING_ADD, button="right")  # training auto advance


class FightBosses:
    """ Fighthing bosses handling. """
    @staticmethod
    def nuke():
        """ Clicks Nuke in Fight Boss menu. """
        click(*FIGHT_BOSS)
        click(*NUKE)

    @staticmethod
    def fightBosses():
        """ Clicks Nuke and then Fight Boss for 10 more seconds. """
        click(*FIGHT_BOSS)
        click(*NUKE)
        for _ in range(5):  # wait for boss to die
            pyautogui.sleep(2)
            click(*FIGHT)


class Adventure:
    """ Features to handle adventure progression. """
    zones = {'safe': 0,
             'tutorial': 1,
             'sewers': 2,
             'forest': 3,
             'cave': 4,
             'sky': 5,
             'hsb': 6,
             'grb': 7,
             'clock': 8,
             'gct': 9,
             '2d': 10,
             'ab': 11,
             'jake': 12,
             'avsp': 13}

    @staticmethod
    def turnIdleOn():
        """ Enables Idle mode. """
        if (not Adventure.isIdle()):
            pyautogui.press('q')

    @staticmethod
    def turnIdleOff():
        """ Disables Idle mode. """
        if (Adventure.isIdle()):
            pyautogui.press('q')

    @staticmethod
    def showZones():
        """ Prints the adventure zones to the screen. """
        z = ""
        for zone in Adventure.zones:
            z += zone + " "
        print(z)

    @staticmethod
    def isIdle():
        """ Returns true if Idle Mode is enabled, false otherwise. """
        pix = getCoords(*IS_IDLE)
        return pyautogui.pixelMatchesColor(*pix, IS_IDLE_COLOR)

    @staticmethod
    def itopodFarm(floor='optimal'):
        """ Enters ITOPOD in {floor} floor.

        Keyword arguments
        floor -- floor to stay on.
        """
        click(*ADVENTURE)
        click(*ITOPOD_ENTER)
        if floor == 'optimal':
            click(*ITOPOD_OPTIMAL)
        else:
            click(*ITOPOD_START_INPUT)
            pyautogui.write(floor, interval=0.2)
            click(*ITOPOD_END_INPUT)
            pyautogui.write(floor, interval=0.2)
        click(*ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def itopodPush(floor='200'):
        """ Enters ITOPOD with starting floor MAX and ending floor {floor}.

        Keyword arguments
        floor -- ending floor to farm.
        """
        click(*ADVENTURE)
        click(*ITOPOD_ENTER)
        click(*ITOPOD_MAX)
        click(*ITOPOD_END_INPUT)
        pyautogui.write(floor, interval=0.2)
        click(*ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def adventureZone(zone='latest'):
        """ Navigates to adventure zone {zone}.

        Keyword arguments
        zone -- zone to go to, by name specified in showZones.
        """
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
        """ Cycles through attacks in adventure mode. """
        pyautogui.press('y')
        pyautogui.press('t')
        # pyautogui.press('r')
        pyautogui.press('e')
        pyautogui.press('w')

    @staticmethod
    def killTitan():  # REWORK
        """ Go to latest zone and attempts to kill the titan.
         """
        click(*ADVENTURE)
        click(*ADVANCE_ZONE, button="right")
        click(*ADVANCE_ZONE)
        # pyautogui.press('q')
        Adventure.turnIdleOff()
        # grb health bar color is not red
        enemy_hp = getCoords(*ENEMY_HEALTH_BAR)
        sleep(6)
        if not pyautogui.pixelMatchesColor(*enemy_hp, (255, 255, 255)):
            print('titan spawned')
            start = time.time()
            while not Adventure.isEnemyDead() or (time.time() - start)/60 < 3:
                Adventure.sendAttacks()
                sleep(0.1)
        # pyautogui.press('q')
        Adventure.turnIdleOn()

    @staticmethod
    def killMonsters(zone='latest', bossOnly=False, kills=20):  # REWORK
        """ kills {kills} monsters in {zone} and returns"""
        Adventure.adventureZone(zone)
        # pyautogui.press('q')  # idle mode
        Adventure.turnIdleOff()
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
                # pyautogui.press('q')  # after 15 fights
                Adventure.turnIdleOn()
                return

    @staticmethod
    def kill():
        """ Kills the current enemy. """
        while not Adventure.isEnemyDead():
            Adventure.sendAttacks()
            sleep(0.1)
        # after this, player may be dead

    @staticmethod
    def isEnemyDead():
        """ Returns True if current enemy is dead, false otherwise. """
        border = getCoords(*ENEMY_HEALTH_BAR_BORDER)
        # check if border of enemy health bar is white
        if (pyautogui.pixelMatchesColor(*border, (255, 255, 255))):
            # print('dead')
            return True
        else:
            return False
            # print('not dead')

    @staticmethod
    def isPlayerLow():
        """ Returns True if player life is below 30%. """
        border = getCoords(*MY_HEALTH_BAR)
        if (pyautogui.pixelMatchesColor(*border, (255, 255, 255))):
            return True
        else:
            return False

    @staticmethod
    def healHP():
        """ Heal HP in the Safe Zone. """
        Adventure.adventureZone('safe')
        sleep(25)
        # click(*ADVANCE_ZONE, button="right")

    @staticmethod
    def enemySpawn():
        """ Returns True if enemy in adventure zone is spawned. """
        enemy_hp = getCoords(*ENEMY_HEALTH_BAR_BORDER)
        return pyautogui.pixelMatchesColor(*enemy_hp, HEALTH_BAR_RED)

    @staticmethod
    def isBoss():
        """ Returns True if current enemy is a Boss. """
        # get the pixel of the crown
        # match it with yellow
        crown = getCoords(*CROWN_LOCATION)
        return pyautogui.pixelMatchesColor(*crown, CROWN_COLOR)

    @staticmethod
    def refreshZone():
        """ Go to another zone and back. """
        click(*GO_BACK_ZONE)
        click(*ADVANCE_ZONE)


class Augmentation:
    @staticmethod
    def augmentation(aug=1, upgrade=False):
        """ Allocates energy to augmentation.

        Keyword arguments
        aug -- augmentation number, 1 is Danger Scissors.
        upgrade -- if True, will allocate energy to aug update instead.
        """
        click(*AUGMENTATION)
        if upgrade:
            x, y = AUG1_UPGRADE[0], AUG1_UPGRADE[1] + (aug - 1) * AUG_DIFF
        else:
            x, y = AUG1[0], AUG1[1] + (aug - 1) * AUG_DIFF
        click(x, y)


class Inventory:
    @staticmethod
    def mergeItem(x, y):
        """ Attemps to merge to item at x, y (relative). """
        moveTo(x, y)
        sleep(MEDIUM_SLEEP)
        pyautogui.press('d')

    @staticmethod
    def boostItem(x, y):
        """ Attempts to boost item at x, y (relative). """
        moveTo(x, y)
        sleep(MEDIUM_SLEEP)
        pyautogui.press('a')

    @staticmethod
    def boostAndMergeEquipped():
        """ Wrapper function to boost and merge all equipped items. """
        click(*INVENTORY)
        Inventory.mergeItem(*WEAPON)
        Inventory.boostItem(*WEAPON)
        Inventory.mergeItem(*ACC1)
        Inventory.boostItem(*ACC1)
        Inventory.mergeItem(*ACC2)
        Inventory.boostItem(*ACC2)
        Inventory.mergeItem(*ACC3)
        Inventory.boostItem(*ACC3)
        Inventory.mergeItem(*HEAD)
        Inventory.boostItem(*HEAD)
        Inventory.mergeItem(*CHEST)
        Inventory.boostItem(*CHEST)
        Inventory.mergeItem(*LEGS)
        Inventory.boostItem(*LEGS)
        Inventory.mergeItem(*BOOTS)
        Inventory.boostItem(*BOOTS)

    @staticmethod
    def boostCube():
        """ Boost infinity cube. """
        click(*INVENTORY)
        click(*CUBE, button="right")

    @staticmethod
    def boostInventory(slots=36):
        """ Boost first {slots} slots of inventory. 

        Keyword arguments 
        slots -- number of slots to boost. 
        """
        num = 0
        x0 = SLOT1[0]
        y0 = SLOT1[1]
        i = 0
        j = 0
        while num < slots:
            if (i >= 12):
                i = 0
                j += 1
            x = x0 + INV_DIFF * i
            y = y0 + INV_DIFF * j
            i += 1
            Inventory.boostItem(x, y)
            num += 1

    @staticmethod
    def mergeInventory(slots=36):
        """ Merge first {slots} slots of inventory. 

        Keyword arguments 
        slots -- number of slots to merge. 
        """

        num = 0
        x0 = SLOT1[0]
        y0 = SLOT1[1]
        i = 0
        j = 0
        while num < slots:
            if (i >= 12):
                i = 0
                j += 1
            x = x0 + INV_DIFF * i
            y = y0 + INV_DIFF * j
            i += 1
            Inventory.mergeItem(x, y)
            num += 1

    @staticmethod
    def boostAndMergeEquips():
        """ Wrapper function to boost and merge all equipment slots and the three first rows of inventory. """
        click(*INVENTORY)

        Inventory.mergeItem(*WEAPON)
        Inventory.boostItem(*WEAPON)
        Inventory.mergeItem(*ACC1)
        Inventory.boostItem(*ACC1)
        Inventory.mergeItem(*ACC2)
        Inventory.boostItem(*ACC2)
        Inventory.mergeItem(*ACC3)
        Inventory.boostItem(*ACC3)
        Inventory.mergeItem(*HEAD)
        Inventory.boostItem(*HEAD)
        Inventory.mergeItem(*CHEST)
        Inventory.boostItem(*CHEST)
        Inventory.mergeItem(*LEGS)
        Inventory.boostItem(*LEGS)
        Inventory.mergeItem(*BOOTS)
        Inventory.boostItem(*BOOTS)

        Inventory.boostItem(SLOT1[0], SLOT1[1])
        Inventory.boostItem(SLOT1[0] + INV_DIFF, SLOT1[1])

        click(*CUBE, button="right")

        for col in range(3):
            for row in range(12):  # boost and merge front row
                x = SLOT1[0] + INV_DIFF * row
                y = SLOT1[1] + INV_DIFF * col
                Inventory.mergeItem(x, y)
                Inventory.boostItem(x, y)

          # boost infinity cube

    @staticmethod
    def trashItems():
        """ Wrapper function to trash items at rows 4 and 5. """
        click(*INVENTORY)
        for col in range(3, 5):
            for row in range(12):
                x = SLOT1[0] + INV_DIFF * row
                y = SLOT1[1] + INV_DIFF * col
                Inventory.trashItem(x, y)

    @staticmethod
    def trashItem(x, y):
        """ Trashes item at x, y (relative). """
        moveTo(x, y)
        sleep(0.1)
        pyautogui.keyDown('ctrl')
        sleep(0.1)
        pyautogui.click()
        sleep(0.1)
        pyautogui.keyUp('ctrl')

    @staticmethod
    def transformPendants():
        """ Wrapper function to transform all maxed pendants. """
        locations = Inventory.locatePendants()
        for loc in locations:
            center = pyautogui.center(loc)
            rawMove(*center)  # show tooltip
            sleep(0.1)
            if Inventory.checkTransformable():
                ctrlClick()
                # print('control click')

    @staticmethod
    def locatePendants():
        """ Returns a generator of the (absolute) locations of all pendants. """
        click(*INVENTORY)
        region = (CORNER[0], CORNER[1], GAME_WIDTH, GAME_HEIGHT)
        locations = pyautogui.locateAllOnScreen('pendant.png', region=region)
        # for loc in locations:
        #     center = pyautogui.center(loc)
        #     rawMove(*center)
        return locations

    @staticmethod
    def checkTransformable():
        """ Check if item being highlighted is transformable. """
        region = (CORNER[0], CORNER[1], GAME_WIDTH, GAME_HEIGHT)
        if pyautogui.locateOnScreen('transformable.png', region=region) != None:
            return True
        return False


class TimeMachine:
    @staticmethod
    def addEnergy():
        """ Adds energy to Time Machine. """
        click(*TIME_MACHINE)
        click(*TM_ADD_ENERGY)
        click(CORNER[0], CORNER[1])

    @staticmethod
    def addMagic():
        """ Adds magic to Time Machine. """
        click(*TIME_MACHINE)
        click(*TM_ADD_MAGIC)


class BloodMagic:
    @staticmethod
    def addMagic(magic=1, cap=False):
        """ Adds magic to Blood Magic. 

        Keyword arguments 
        magic -- magic number, starts at 1. 
        cap -- if True, will try to cap magic instead. 
        """
        click(*BLOOD_MAGIC)
        if cap:
            x, y = BM1_CAP[0], BM1_CAP[1] + (magic - 1) * BM_DIFF
        else:
            x, y = BM1_ADD[0], BM1_ADD[1] + (magic - 1) * BM_DIFF
        click(x, y)


class MoneyPit:
    @staticmethod
    def moneyPit():
        """ Throws money into pit. """
        click(*MONEY_PIT)
        click(*FEED_ME)
        click(*FEED_YEAH)


class Rebirth:
    @staticmethod
    def rebirth():
        """ Rebirth. """
        click(*REBIRTH_MENU)
        sleep(5)  # to see if it's crashing
        click(*REBIRTH_BUTTON)
        click(*REBIRTH_CONFIRMATION)


class Yggdrasil:
    @staticmethod
    def harvestAll():
        """ Harvest all max tiered fruits. """
        click(*YGGDRASIL)
        click(*HARVEST_ALL_MAX_TIER)

    @staticmethod
    def activatePower():
        """ Activates power fruit. """
        click(*YGGDRASIL)
        click(*FRUIT_POWER_HARVEST)


class Misc:
    @staticmethod
    def reclaimEnergy():
        """ Reclaims all energy. """
        click(*BASIC_TRAINING)
        pyautogui.press('r')

    @staticmethod
    def reclaimMagic():
        """ Reclaims all magic. """
        click(*BASIC_TRAINING)
        pyautogui.press('t')

    @staticmethod
    def inputResource(amount='cap', idle=False):
        """ Sets input resource to {amount}. 

        Keyword arguments
        amount -- amount to input, half or cap.  
        idle -- if True will consider only the idle energy. 
        """

        click(*BASIC_TRAINING)
        if amount == 'cap':
            click(*ENERGY_CUSTOM_AMOUNT_CAP)
        elif amount == 'half':
            if idle:
                click(*ENERGY_CUSTOM_AMOUNT_HALF_IDLE)
            else:
                click(*ENERGY_CUSTOM_AMOUNT_HALF)
