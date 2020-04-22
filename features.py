""" Module for various features handling.

Features:  
    BasicTraining   
    FightBoss 
    MoneyPit  
    Adventure  
    Inventory  
    Augmentation  
    TimeMachine  
    BloodMagic  
    Wandoos  
    Yggdrasil  

Missing:  
    AdvTraining  
    NGU  
    GoldDiggers  
    Beards  
    """

from collections import deque
from typing import List, Set, Dict, Tuple

import time

import coords
from helper import *
from navigation import Navigation
from statistics import Statistics


class BasicTraining:
    """ Add energy to basic training. """
    @staticmethod
    def basicTraining() -> None:
        """ Right clicks on add energy to ATK1.

            Requires training auto advance to be bought.
        """
        Navigation.menu('basicTraining')
        # training auto advance
        click(*coords.BASIC_TRAINING_ADD, button="right")


class FightBosses:
    """ Nuke and Fight story bosses. """
    @staticmethod
    def nuke() -> None:
        """ Nuke in Fight Boss menu. """
        Navigation.menu('fightBoss')
        click(*coords.NUKE)

    @staticmethod
    def fightBoss() -> None:
        """ Click Fight Boss once. 

        Should be in Fight Boss menu.  
        """
        if Navigation.currentMenu != 'fightBoss':
            raise Exception('should be in Fight Boss menu!')
        click(*coords.FIGHT)

    @staticmethod
    def fightBosses() -> None:
        """ Wrapper for nuke and fight bosses in sucession. """
        Navigation.menu('fightBoss')
        click(*coords.NUKE)
        for _ in range(5):  # wait for boss to die
            pyautogui.sleep(2)
            click(*coords.FIGHT)


class Adventure:
    """ Various features related to Adventure menu. """
    # adventure zones
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
             'avsp': 13,
             'mega': 14,
             'uug': 15,
             'beardverse': 16}

    # abilities mapping
    abilities_keys = {1: 'w',
                      2: 'e',
                      3: 'r',
                      4: 't',
                      5: 'y',
                      6: 'a',
                      7: 's',
                      8: 'd',
                      9: 'f',
                      10: 'g',
                      11: 'h',
                      13: 'x'}

    @staticmethod
    def turnIdleOn() -> None:
        """ Enable Idle mode in Adventure. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        if (not Adventure.isIdle()):
            pyautogui.press('q')

    @staticmethod
    def turnIdleOff() -> None:
        """ Disable Idle mode. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        if (Adventure.isIdle()):
            pyautogui.press('q')

    @staticmethod
    def showZones() -> None:
        """ Print the available adventure zones to the screen. """
        z = ""
        for zone in Adventure.zones:
            z += zone + " "
        print(z)

    @staticmethod
    def isIdle() -> bool:
        """ Return true if Idle Mode is enabled, false otherwise. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        pix = getCoords(*coords.IS_IDLE)
        return pyautogui.pixelMatchesColor(*pix, coords.IS_IDLE_COLOR)

    @staticmethod
    def itopodFarm(floor: str = 'optimal') -> None:
        """ Enter ITOPOD in floor x.

        Keyword arguments:  
        floor -- floor to enter.
        """
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
    def itopodExperimental() -> None:  # TODO
        """ Abuse a bug in itopod floors to higher exp/hr. """
        # tiers = {1: 0,
        #          2: 50,
        #          3: 100,
        #          4: 150,
        #          5: 200}
        # only from 150 on
        tiers = {4: 150,
                 5: 200}

        Navigation.menu('adventure')
        tierKillsCount = {}
        for tier, floor in tiers.items():
            print(tier, floor)
            click(*coords.ITOPOD_ENTER)
            click(*coords.ITOPOD_START_INPUT)
            pyautogui.write(str(floor))
            click(*coords.ITOPOD_ENTER_CONFIRMATION)
            print(f'getting tier kills: ')
            tierKills = Statistics.getTierKills()

            if tierKills == -1:
                print('could not detect tier kills')
            else:
                print(f'tier kills: {tierKills}')
                tierKillsCount[tier] = tierKills

        print(tierKillsCount)

    @staticmethod
    def itopodPush(floor: str = '200') -> None:
        """ Enter ITOPOD with starting floor MAX and ending floor x.

        Keyword arguments:  
        floor -- ending floor.
        """
        Navigation.menu('adventure')
        click(*coords.ITOPOD_ENTER)
        click(*coords.ITOPOD_MAX)
        click(*coords.ITOPOD_END_INPUT)
        pyautogui.write(floor, interval=0.2)
        click(*coords.ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def adventureZone(zone: str = 'latest') -> None:
        """ Go to adventure zone x.

        Keyword arguments:  
        zone -- zone to go to, by name specified in showZones.
        """
        Navigation.menu('adventure')
        # if (Navigation.adventureZone == zone):
        #     return # TODO
        click(*coords.GO_BACK_ZONE, button="right")   # start at 0
        if zone == 'latest':
            click(*coords.ADVANCE_ZONE, button="right")
        else:
            times = Adventure.zones[zone]
            for _ in range(times):
                click(*coords.ADVANCE_ZONE, delay="fast")
        Navigation.adventureZone = zone  # update adventureZone variable

    @staticmethod
    def sendAttacks(buffs: bool = False) -> None:
        """ Cycle through attacks in adventure mode.

        Keyword arguments:  
        buffs - if set to True, will use buffs and heal when available.  

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        if buffs:
            press('gsfhdxytrew')  # all attacks and buffs
        else:
            press('ytew')  # only attacks

    @staticmethod
    def killTitan():  # REWORK #TODO
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
    def kill(fast: bool = False, buffs: bool = False) -> None:
        """ Kill the current enemy. 

        Should be in Adventure menu already.  """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        while not Adventure.isEnemyDead():
            if fast:  # use only regular attacks
                pyautogui.press('w')
            elif buffs:  # use all attacks and buffs
                Adventure.sendAttacks(buffs=True)
            else:  # use all attacks
                Adventure.sendAttacks()
                sleep(0.1)
        # after this, player may be dead

    @staticmethod
    # EXPERIMENTAL # TODO
    def getReadyAbilities(buffs: bool = False) -> List[int]:
        """ Return the ready abilities as a list. 

        Keyword arguments:  
        buffs -- if you want to use buffs also (not recommended).
        """
        ready = set()
        image = getScreenshot()

        x0 = coords.ABILITY_1[0]
        y0 = coords.ABILITY_1[1]
        i = 0
        while i <= 15:  # 16 abilities (MOVE 69 LOCKED)
            if i < 5:  # row 1
                x = x0 + i * coords.ABILITY_OFFSET_X
                y = y0
                color = coords.ABILITY_ROW_1_READY_COLOR
            elif i < 11:  # row 2
                x = x0 + (i - 6) * coords.ABILITY_OFFSET_X
                y = y0 + coords.ABILITY_OFFSET_Y
                color = coords.ABILITY_ROW_2_READY_COLOR
            else:  # row 3
                x = x0 + (i - 12) * coords.ABILITY_OFFSET_X
                y = y0 + 2 * coords.ABILITY_OFFSET_Y
                color = coords.ABILITY_ROW_3_READY_COLOR
            i += 1
            # print(f'ability: {getPixelColor(x, y)}')
            # print(f'color: {color}')
            if getPixelColor(x, y, image=image) == color:
                # print(f'{i} ready')
                ready.add(i)

        if getPixelColor(*coords.MY_HEALTH_BAR_THRESHOLD) != (236, 52, 52):
            # priority needing to heal
            print('needs healing')
            if buffs:
                priority = [8, 13, 10, 7, 9, 11, 5, 4, 3, 6, 2]
            else:
                priority = [8, 13, 10, 5, 4, 3, 6, 2]
        else:
            # priority not needing to heal
            print('no need to heal')
            if buffs:
                priority = [10, 7, 9, 11, 5, 4, 3, 6, 2]
            else:
                priority = [10, 5, 4, 3, 6, 2]

        # TODO
        # use an actual priority queue
        myQueue = []

        for ability in priority:
            if ability in ready:
                myQueue.append(ability)
        # for _ in range(3):  # experimental -> 3 regular attacks afterwards
        #     myQueue.append(1)
        myQueue.append(1)
        return myQueue

    @staticmethod
    def snipe(buffs=False):  # EXPERIMENTAL #TODO
        """ Snipe a boss using ready rotations. 

        Keyword arguments:  
        buffs -- if you want to use buffs also (not recommended).
        """
        # turn off idle
        print(f'getting abilities queue')
        start = time.time()
        if buffs:
            queue = deque(Adventure.getReadyAbilities(buffs=True))
        else:
            queue = deque(Adventure.getReadyAbilities())
        print(f'time: {time.time() - start}')
        while not Adventure.isEnemyDead():
            if not queue:
                print('rotation over')
                print(f'getting abilities queue')
                start = time.time()
                if buffs:
                    queue = deque(Adventure.getReadyAbilities(buffs=True))
                else:
                    queue = deque(Adventure.getReadyAbilities())
                print(f'time: {time.time() - start}')
                print(f'ABILITIES: {queue}')
            ability = queue.popleft()
            print(ability)
            press(Adventure.abilities_keys[ability])

            # WORK AROUND - SLEEP 1s (MY CD TIME)
            sleep(1.1)

            """
            # WAIT FOR COOLDOWN
            # sleep(0.3)
            # start = time.time()
            # print(f'taking screenshot')
            # image = getScreenshot(coords.ABILITY_1_REGION)
            # color = getPixelColor(1, 1, image=image)
            color = getPixelColor(*coords.ABILITY_1)
            # print(f'time: {time.time() - start}')
            while color != coords.ABILITY_ROW_1_READY_COLOR:
                # print('waiting for cd')
                # print(f'taking screenshot')
                # image = getScreenshot(coords.ABILITY_1_REGION)
                # color = getPixelColor(1, 1, image=image)
                color = getPixelColor(*coords.ABILITY_1)
                # print(f'time: {time.time() - start}')
                sleep(0.05)
            """

    @staticmethod
    def isEnemyDead() -> bool:
        """ Return True if current enemy is dead, false otherwise. 

        Should be in Adventure menu already.  
        """
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
    def isPlayerLow() -> bool:
        """ Returns True if player life is below 30% (approximately). 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        border = getCoords(*coords.MY_HEALTH_BAR)
        if (pyautogui.pixelMatchesColor(*border, (255, 255, 255))):
            return True
        else:
            return False

    @staticmethod
    def isPlayerFull() -> bool:
        """ Return True if player life is above 95% (approximately). """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        pix = getCoords(*coords.MY_HEALTH_BAR_FULL)
        return pyautogui.pixelMatchesColor(*pix, coords.HEALTH_BAR_RED, tolerance=10)

    @staticmethod
    def healHP() -> None:  # DEPRECATED
        """ Heal HP in the Safe Zone. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        Adventure.adventureZone('safe')
        sleep(25)
        # click(*ADVANCE_ZONE, button="right")

    @staticmethod
    def enemySpawn() -> bool:
        """ Return True if there is an enemy in adventure zone. 

        May return false if enemy hp is low enough for the color check.  

        Should be in Adventure menu already. 
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        enemy_hp = getCoords(*coords.ENEMY_HEALTH_BAR_BORDER)
        return pyautogui.pixelMatchesColor(*enemy_hp, coords.HEALTH_BAR_RED)

    @staticmethod
    def isBoss() -> bool:
        """ Return True if current enemy is a Boss. 

        Will check for the yellow crown on the adventure enemy.  

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        # get the pixel of the crown
        # match it with yellow
        crown = getCoords(*coords.CROWN_LOCATION)
        return pyautogui.pixelMatchesColor(*crown, coords.CROWN_COLOR)

    @staticmethod
    def refreshZone() -> None:
        """ Go to another zone and back for a new enemy to spawn. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        click(*coords.GO_BACK_ZONE)
        click(*coords.ADVANCE_ZONE)

    @staticmethod
    def buff() -> None:
        """ Use adventure buffs. 

        Order:  
        Charge -> Defensive -> Offensive -> Ultimate
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')
        press('gsfh', delay=1.1)


class Augmentation:
    @staticmethod
    def augmentation(aug=1, upgrade=False):
        """ Allocates energy to augmentation.

        Keyword arguments:  
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
        # sleep(coords.MEDIUM_SLEEP)
        pyautogui.press('d')
        sleep(coords.FAST_SLEEP)
        pyautogui.press('d')

    @staticmethod
    def boostItem(x, y):
        """ Attempts to boost item at x, y (relative). """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        click(x, y)
        # sleep(coords.MEDIUM_SLEEP)
        pyautogui.press('a')
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

        Keyword arguments:  : 
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
        """ Merge first slots of inventory. 

        Keyword arguments:  : 
        slots -- number of slots to merge, starting from first one. 
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
    def getEmptySlots():
        """ Return number of empty slots on first page of inventory. """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')
        empty = Inventory.locateAll('images/empty-slot.png')
        return len(list(empty))  # empty is a generator

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

        Keyword arguments:  :
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
        Navigation.menu('rebirth')
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
    def isHarvested(fruit):
        """ Return True if fruit is harvested. """
        Navigation.menu('yggdrasil')
        pix = getCoords(*coords.FRUITS_IS_HARVESTED[fruit.upper()])
        return pyautogui.pixelMatchesColor(*pix, (255, 255, 255))

    @staticmethod
    def activate(fruit):
        """ Activate fruit in yggdrasil menu.

        If there is not enough resources idle, nothing happens.   
        If fruit is already activated, will harvest it. 
        """
        Navigation.menu('yggdrasil')
        click(*coords.FRUITS[fruit.upper()])


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
    def reclaimAll():
        """ Reclaim all resources. """
        if Navigation.currentMenu == 'adventure':
            Navigation.menu('basicTraining')
        pyautogui.press('r')
        pyautogui.press('t')

    @staticmethod
    def inputResource(amount='cap', idle=False):
        """ Sets input resource to {amount}. 

        Keyword arguments:   
        amount -- cap, half or quarter.  
        idle -- if True will consider only the idle energy. 
        """
        possibleMenus = ['basicTraining', 'augments', 'advTraining',
                         'timeMachine', 'bloodMagic', 'wandoos', 'ngu']

        if Navigation.currentMenu not in possibleMenus:
            Navigation.menu('basicTraining')
        # click(*coords.BASIC_TRAINING)
        if idle:
            if amount == 'cap':
                click(*coords.ENERGY_CUSTOM_AMOUNT_CAP)
            if amount == 'half':
                click(*coords.ENERGY_CUSTOM_AMOUNT_HALF)
            if amount == 'quarter':
                click(*coords.ENERGY_CUSTOM_AMOUNT_QUARTER)
        else:
            if amount == 'cap':
                click(*coords.ENERGY_CUSTOM_AMOUNT_CAP)
            if amount == 'half':
                click(*coords.ENERGY_CUSTOM_AMOUNT_HALF_IDLE)
            if amount == 'quarter':
                click(*coords.ENERGY_CUSTOM_AMOUNT_QUARTER_IDLE)
