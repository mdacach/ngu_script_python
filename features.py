""" Module for various features handling."""

from helper import *
# from coords import *
import coords
from navigation import Navigation
import time


class BasicTraining:
    """ Basic training handling. """
    @staticmethod
    def basicTraining():
        """ Right clicks on add energy to ATK1.

            Requires training auto advance to be bought.
        """
        # click(*coords.BASIC_TRAINING)
        Navigation.menu('basicTraining')
        # training auto advance
        click(*coords.BASIC_TRAINING_ADD, button="right")


class FightBosses:        # click(*coords.BASIC_TRAINING)
    """ Fighthing bosses handling. """
    @staticmethod
    def nuke():
        """ Clicks Nuke in Fight Boss menu. """
        # click(*coords.FIGHT_BOSS)
        Navigation.menu('fightBoss')
        click(*coords.NUKE)

    @staticmethod
    def fightBosses():
        """ Clicks Nuke and then Fight Boss for 10 more seconds. """
        # click(*coords.FIGHT_BOSS)
        Navigation.menu('fightBoss')
        click(*coords.NUKE)
        for _ in range(5):  # wait for boss to die
            pyautogui.sleep(2)
            click(*coords.FIGHT)


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
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        if (not Adventure.isIdle()):
            pyautogui.press('q')

    @staticmethod
    def turnIdleOff():
        """ Disables Idle mode. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
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
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        pix = getCoords(*coords.IS_IDLE)
        return pyautogui.pixelMatchesColor(*pix, coords.IS_IDLE_COLOR)

    @staticmethod
    def itopodFarm(floor='optimal'):
        """ Enters ITOPOD in {floor} floor.

        Keyword arguments
        floor -- floor to stay on.
        """
        # click(*coords.ADVENTURE)
        Navigation.menu('adventure')
        click(*coords.ITOPOD_ENTER)
        if floor == 'optimal':
            click(*coords.ITOPOD_OPTIMAL)
        else:
            click(*coords.ITOPOD_START_INPUT)
            pyautogui.write(floor, interval=0.2)
            click(*coords.ITOPOD_END_INPUT)
            pyautogui.write(floor, interval=0.2)
        click(*coords.ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def itopodPush(floor='200'):
        """ Enters ITOPOD with starting floor MAX and ending floor {floor}.

        Keyword arguments
        floor -- ending floor to farm.
        """
        # click(*coords.ADVENTURE)
        Navigation.menu('adventure')
        click(*coords.ITOPOD_ENTER)
        click(*coords.ITOPOD_MAX)
        click(*coords.ITOPOD_END_INPUT)
        pyautogui.write(floor, interval=0.2)
        click(*coords.ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def adventureZone(zone='latest'):
        """ Navigates to adventure zone {zone}.

        Keyword arguments
        zone -- zone to go to, by name specified in showZones.
        """
        # click(*coords.ADVENTURE)
        Navigation.menu('adventure')
        if (Navigation.adventureZone == zone):
            return
        click(*coords.GO_BACK_ZONE, button="right")   # start at 0
        if zone == 'latest':
            click(*coords.ADVANCE_ZONE, button="right")
        else:
            times = Adventure.zones[zone]
            for _ in range(times):
                click(*coords.ADVANCE_ZONE)
        Navigation.adventureZone = zone

    @staticmethod
    def sendAttacks():
        """ Cycles through attacks in adventure mode. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        pyautogui.press('y')
        pyautogui.press('t')
        # pyautogui.press('r')
        pyautogui.press('e')
        pyautogui.press('w')

    @staticmethod
    def killTitan():  # REWORK
        """ Go to latest zone and attempts to kill the titan.
         """
        # click(*coords.ADVENTURE)
        Navigation.menu('adventure')
        click(*coords.ADVANCE_ZONE, button="right")
        click(*coords.ADVANCE_ZONE)
        # pyautogui.press('q')
        Adventure.turnIdleOff()
        # grb health bar color is not red
        enemy_hp = getCoords(*coords.ENEMY_HEALTH_BAR)
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
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        while not Adventure.isEnemyDead():
            Adventure.sendAttacks()
            sleep(0.1)
        # after this, player may be dead

    @staticmethod
    def isEnemyDead():
        """ Returns True if current enemy is dead, false otherwise. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        border = getCoords(*coords.ENEMY_HEALTH_BAR_BORDER)
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
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        border = getCoords(*coords.MY_HEALTH_BAR)
        if (pyautogui.pixelMatchesColor(*border, (255, 255, 255))):
            return True
        else:
            return False

    @staticmethod
    def healHP():
        """ Heal HP in the Safe Zone. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        Adventure.adventureZone('safe')
        sleep(25)
        # click(*ADVANCE_ZONE, button="right")

    @staticmethod
    def enemySpawn():
        """ Returns True if enemy in adventure zone is spawned. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        enemy_hp = getCoords(*coords.ENEMY_HEALTH_BAR_BORDER)
        return pyautogui.pixelMatchesColor(*enemy_hp, coords.HEALTH_BAR_RED)

    @staticmethod
    def isBoss():
        """ Returns True if current enemy is a Boss. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        # get the pixel of the crown
        # match it with yellow
        crown = getCoords(*coords.CROWN_LOCATION)
        return pyautogui.pixelMatchesColor(*crown, coords.CROWN_COLOR)

    @staticmethod
    def refreshZone():
        """ Go to another zone and back. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        click(*coords.GO_BACK_ZONE)
        click(*coords.ADVANCE_ZONE)


class Augmentation:
    @staticmethod
    def augmentation(aug=1, upgrade=False):
        """ Allocates energy to augmentation.

        Keyword arguments
        aug -- augmentation number, 1 is Danger Scissors.
        upgrade -- if True, will allocate energy to aug update instead.
        """
        # click(*coords.AUGMENTATION)
        Navigation.menu('augments')
        if upgrade:
            x, y = coords.AUG1_UPGRADE[0], coords.AUG1_UPGRADE[1] + \
                (aug - 1) * coords.AUG_DIFF
        else:
            x, y = coords.AUG1[0], coords.AUG1[1] + (aug - 1) * coords.AUG_DIFF
        click(x, y)


class Inventory:
    @staticmethod
    def loadout(num):
        """ Wears loadout {num}. """
        Navigation.menu('inventory')
        if num == 1:
            click(*coords.LOADOUT1)
        if num == 2:
            click(*coords.LOADOUT2)

    @staticmethod
    def mergeItem(x, y):
        """ Attemps to merge to item at x, y (relative). """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        click(x, y)
        sleep(coords.FAST_SLEEP)
        pyautogui.press('d')

    @staticmethod
    def boostItem(x, y):
        """ Attempts to boost item at x, y (relative). """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        click(x, y)
        sleep(coords.FAST_SLEEP)
        pyautogui.press('a')

    @staticmethod
    def boostAndMergeEquipped():
        """ Wrapper function to boost and merge all equipped items. """
        # click(*coords.INVENTORY)
        Navigation.menu('inventory')
        Inventory.mergeItem(*coords.WEAPON)
        Inventory.boostItem(*coords.WEAPON)
        Inventory.mergeItem(*coords.ACC1)
        Inventory.boostItem(*coords.ACC1)
        Inventory.mergeItem(*coords.ACC2)
        Inventory.boostItem(*coords.ACC2)
        Inventory.mergeItem(*coords.ACC3)
        Inventory.boostItem(*coords.ACC3)
        Inventory.mergeItem(*coords.HEAD)
        Inventory.boostItem(*coords.HEAD)
        Inventory.mergeItem(*coords.CHEST)
        Inventory.boostItem(*coords.CHEST)
        Inventory.mergeItem(*coords.LEGS)
        Inventory.boostItem(*coords.LEGS)
        Inventory.mergeItem(*coords.BOOTS)
        Inventory.boostItem(*coords.BOOTS)

    @staticmethod
    def boostCube():
        """ Boost infinity cube. """
        # click(*coords.INVENTORY)
        Navigation.menu('inventory')
        click(*coords.CUBE, button="right")

    @staticmethod
    def boostInventory(slots=36):
        """ Boost first {slots} slots of inventory. 

        Keyword arguments: 
        slots -- number of slots to boost. 
        """
        Navigation.menu('inventory')

        num = 0
        x0 = coords.SLOT1[0]
        y0 = coords.SLOT1[1]
        i = 0
        j = 0
        while num < slots:
            if (i >= 12):
                i = 0
                j += 1
            x = x0 + coords.INV_DIFF * i
            y = y0 + coords.INV_DIFF * j
            i += 1
            Inventory.boostItem(x, y)
            num += 1

    @staticmethod
    def mergeInventory(slots=36):
        """ Merge first {slots} slots of inventory. 

        Keyword arguments 
        slots -- number of slots to merge. 
        """
        Navigation.menu('inventory')

        num = 0
        x0 = coords.SLOT1[0]
        y0 = coords.SLOT1[1]
        i = 0
        j = 0
        while num < slots:
            if (i >= 12):
                i = 0
                j += 1
            x = x0 + coords.INV_DIFF * i
            y = y0 + coords.INV_DIFF * j
            i += 1
            Inventory.mergeItem(x, y)
            num += 1

    @staticmethod
    def trashItems():
        """ Wrapper function to trash items at rows 4 and 5. """
        # click(*coords.INVENTORY)
        Navigation.menu('inventory')
        for col in range(3, 5):
            for row in range(12):
                x = coords.SLOT1[0] + coords.INV_DIFF * row
                y = coords.SLOT1[1] + coords.INV_DIFF * col
                Inventory.trashItem(x, y)

    @staticmethod
    def trashItem(x, y):
        """ Trashes item at x, y (relative). """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

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
        Navigation.menu('inventory')

        locations = Inventory.locatePendants()
        for loc in locations:
            center = pyautogui.center(loc)
            rawMove(*center)  # show tooltip
            sleep(0.1)
            if Inventory.checkTransformable():
                ctrlClick()
                # print('control click')

    @staticmethod
    def transformItem(loc):
        """ Transforms item being hovered. """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')
        center = pyautogui.center(loc)
        rawClick(*center)
        sleep(0.1)
        print('checking transformable')
        if Inventory.checkTransformable():
            print('is transformable')
            ctrlClick()

    @staticmethod
    def transformAll(image):
        """ Transform all items if transformable. """
        Navigation.menu('inventory')
        locations = Inventory.locateAll(image)
        for loc in locations:
            Inventory.transformItem(loc)

    @staticmethod
    def locateAll(image):
        """ Returns a generator of the (absolute) locations of all items {image}. """
        Navigation.menu('inventory')
        region = (CORNER[0], CORNER[1], coords.GAME_WIDTH, coords.GAME_HEIGHT)
        locations = pyautogui.locateAllOnScreen(image, region=region)
        return locations

    @staticmethod
    def locatePendants():
        """ Returns a generator of the (absolute) locations of all pendants. """
        Navigation.menu('inventory')
        region = (CORNER[0], CORNER[1], coords.GAME_WIDTH, coords.GAME_HEIGHT)
        locations = pyautogui.locateAllOnScreen('pendant.png', region=region)
        return locations

    @staticmethod
    def checkTransformable():
        """ Check if item being highlighted is transformable. """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        region = (CORNER[0], CORNER[1], coords.GAME_WIDTH, coords.GAME_HEIGHT)
        if pyautogui.locateOnScreen('transformable.png', region=region) != None:
            return True
        return False


class TimeMachine:
    @staticmethod
    def addEnergy():
        """ Adds energy to Time Machine. """
        # click(*coords.TIME_MACHINE)
        Navigation.menu('timeMachine')
        click(*coords.TM_ADD_ENERGY)

    @staticmethod
    def addMagic():
        """ Adds magic to Time Machine. """
        # click(*coords.TIME_MACHINE)
        Navigation.menu('timeMachine')
        click(*coords.TM_ADD_MAGIC)


class BloodMagic:
    @staticmethod
    def addMagic(magic=1, cap=False):
        """ Adds magic to Blood Magic. 

        Keyword arguments 
        magic -- magic number, starts at 1. 
        cap -- if True, will try to cap magic instead. 
        """
        # click(*coords.BLOOD_MAGIC)
        Navigation.menu('bloodMagic')

        if cap:
            x, y = coords.BM1_CAP[0], coords.BM1_CAP[1] + \
                (magic - 1) * coords.BM_DIFF
        else:
            x, y = coords.BM1_ADD[0], coords.BM1_ADD[1] + \
                (magic - 1) * coords.BM_DIFF
        click(x, y)


class MoneyPit:
    @staticmethod
    def moneyPit():
        """ Throws money into pit. """
        # click(*coords.MONEY_PIT)
        Navigation.menu('moneyPit')

        click(*coords.FEED_ME)
        click(*coords.FEED_YEAH)


class Rebirth:
    @staticmethod
    def rebirth():
        """ Rebirth. """
        # click(*coords.REBIRTH_MENU)
        Navigation.menu('rebirth')
        sleep(5)  # to see the number
        click(*coords.REBIRTH_BUTTON)
        click(*coords.REBIRTH_CONFIRMATION)


class Yggdrasil:
    @staticmethod
    def harvestAll():
        """ Harvest all max tiered fruits. """
        # click(*coords.YGGDRASIL)
        Navigation.menu('yggdrasil')
        click(*coords.HARVEST_ALL_MAX_TIER)

    @staticmethod
    def activatePower():
        """ Activates power fruit. """
        # click(*coords.YGGDRASIL)
        Navigation.menu('yggdrasil')
        click(*coords.FRUIT_POWER_HARVEST)


class Misc:
    @staticmethod
    def reclaimEnergy():
        """ Reclaims all energy. """
        # click(*coords.BASIC_TRAINING)
        if Navigation.currentMenu == 'adventure':
            Navigation.menu('basicTraining')
        pyautogui.press('r')

    @staticmethod
    def reclaimMagic():
        """ Reclaims all magic. """
        # click(*coords.BASIC_TRAINING)
        if Navigation.currentMenu == 'adventure':
            Navigation.menu('basicTraining')
        pyautogui.press('t')

    @staticmethod
    def inputResource(amount='cap', idle=False):
        """ Sets input resource to {amount}. 

        Keyword arguments: \n
        amount -- amount to input, half or cap.  \n
        idle -- if True will consider only the idle energy. 
        """
        possibleMenus = ['basicTraining', 'augments', 'advTraining',
                         'timeMachine', 'bloodMagic', 'wandoos', 'ngu']

        if Navigation.currentMenu not in possibleMenus:
            Navigation.menu('basicTraining')
        # click(*coords.BASIC_TRAINING)
        if amount == 'cap':
            click(*coords.ENERGY_CUSTOM_AMOUNT_CAP)
        elif amount == 'half':
            if idle:
                click(*coords.ENERGY_CUSTOM_AMOUNT_HALF_IDLE)
            else:
                click(*coords.ENERGY_CUSTOM_AMOUNT_HALF)
