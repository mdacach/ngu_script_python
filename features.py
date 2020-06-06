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
    GoldDiggers  

Missing:  
    AdvTraining  
    NGU  
    Beards  
    """

from collections import deque
from typing import List, Set, Dict, Tuple, Generator
import time
import re

import pyautogui

import coords
from helper import Helper
from navigation import Navigation
from statistics import Statistics

click = Helper.click
moveTo = Helper.moveTo
sleep = Helper.sleep
getRegion = Helper.getRegion
getCoords = Helper.getCoords
press = Helper.press
write = Helper.write


class BasicTraining:
    """ Add energy to basic training. """
    @staticmethod
    def basicTraining() -> None:
        """ Right click on add energy to ATK1.

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


class Itopod:
    """ Functions and variables related to ITOPOD. """

    tiers = {
        1: 0,
        2: 50,
        3: 100,
        4: 150,
        5: 200,
        6: 250,
        7: 300,
        8: 350,
        9: 400,
    }
    tiersEXP = {
        1: 1,
        2: 2,
        3: 4,
        4: 8,
        5: 14,
        6: 22,
        7: 32,
        8: 44,
        9: 58,
    }
    kills = 0
    AP_gained = 0
    EXP_gained = 0
    PP_gained = 0
    tierKillsCount = {}

    @staticmethod
    def itopodExperimental(duration: float = 0, verbose: int = 0) -> None:
        """ Abuse a bug in itopod floors to higher exp/hr. 

        Farm optimal floor until there is only one kill remaining for a tier reward.  
        If there is more than one tier with upcoming rewards, choose the highest one.  

        Global arguments:  
        killCount  -- total kills between all floors.  
        totalEXP   -- total EXP gained since first call.  
        totalAP    -- total AP gained since first call.  

        Keyword arguments:  
        duration -- if not 0, the script will only run for that amount of time. (default 0)  
        verbose -- 0 for no printing, 1 for normal printing and 2 for extra verbose. (default 0)
        """

        if verbose > 1:
            print(f'tiers: {Itopod.tiers}')
            print(f'exp: {Itopod.tiersEXP}')

        Navigation.menu('adventure')
        Adventure.turnIdleOff()
        if not Itopod.tierKillsCount:
            for tier, floor in Itopod.tiers.items():
                if verbose:
                    if verbose > 1:
                        print(f'tier: {tier}, floor: {floor}')
                    print(f'getting tier kills: ')
                tierKills = Statistics.getTierKills(str(floor))

                if tierKills == -1:
                    print('could not detect tier kills')
                    Itopod.tierKillsCount[tier] = 40
                else:
                    if verbose:
                        print(f'tier kills: {tierKills}')
                    Itopod.tierKillsCount[tier] = tierKills

        if verbose:
            print(Itopod.tierKillsCount)

        minimum = min(Itopod.tierKillsCount, key=Itopod.tierKillsCount.get)
        if verbose:
            print(
                f'minimum is tier {minimum} with {Itopod.tierKillsCount[minimum]} kill count')

        next_tiers = []
        minimum_value = min(Itopod.tierKillsCount.values())
        if verbose:
            print(f'minimum value: {minimum_value}')

        for tier in Itopod.tierKillsCount:
            if Itopod.tierKillsCount[tier] == minimum_value:  # go get its reward
                if verbose:
                    print(
                        f'minimum tier: {tier} with {Itopod.tierKillsCount[tier]}')
                next_tiers.append(tier)

        if verbose:
            print('next tiers:')
            for tier in next_tiers:
                print(f'{tier} at floor {Itopod.tiers[tier]}')

        if minimum_value == 1:
            current_tier = max(next_tiers)  # next tier I will go to
            if verbose > 1:
                print(
                    f'going to tier {current_tier} at floor {Itopod.tiers[current_tier]}')
            click(*coords.ITOPOD_ENTER, delay='fast')
            click(*coords.ITOPOD_START_INPUT, delay='fast')
            write(str(Itopod.tiers[current_tier]))
            click(*coords.ITOPOD_ENTER_CONFIRMATION, delay='fast')
            optimal = False

        else:  # must be bigger than 1
            # can afford to go to optimal
            current_tier = minimum
            if verbose > 1:
                print(f'going to optimal floor')
            click(*coords.ITOPOD_ENTER, delay='fast')
            click(*coords.ITOPOD_START_INPUT, delay='fast')
            click(*coords.ITOPOD_OPTIMAL, delay='fast')
            click(*coords.ITOPOD_ENTER_CONFIRMATION, delay='fast')
            optimal = True

        start = time.time()
        while Itopod.tierKillsCount[current_tier] > 0:

            while not Adventure.enemySpawn():
                sleep(0.03)
            Adventure.kill()
            # Adventure.snipe(fast=True) slower
            # while not Statistics.checkPixelColor(*coords.ABILITY_1, coords.ABILITY_ROW_1_READY_COLOR):
            #    sleep(0.05)
            # pyautogui.ress('w')
            Itopod.kills += 1

            for tier in Itopod.tierKillsCount:
                Itopod.tierKillsCount[tier] -= 1  # decrease all counters

            for tier in Itopod.tierKillsCount:
                if Itopod.tierKillsCount[tier] == 0:
                    Itopod.tierKillsCount[tier] = 40 - \
                        tier  # formula for new counter
                    if current_tier == tier:  # if we are in this tier, get its reward
                        Itopod.EXP_gained += Itopod.tiersEXP[tier]
                        Itopod.AP_gained += 1

            next_tiers = []
            # minimum kill counter remaining
            minimum_value = min(Itopod.tierKillsCount.values())
            for tier in Itopod.tierKillsCount:
                if Itopod.tierKillsCount[tier] == minimum_value:
                    if verbose:
                        print(
                            f'minimum tier: {tier} at floor {Itopod.tiers[tier]} with {Itopod.tierKillsCount[tier]} remaining kills')
                    next_tiers.append(tier)

            if verbose:
                print('next tiers:')
                for tier in next_tiers:
                    print(f'tier {tier} at floor {Itopod.tiers[tier]}')

            if minimum_value == 1:
                current_tier = max(next_tiers)  # next tier I will go to
                if verbose > 1:
                    print(
                        f'going to tier {current_tier} at floor {Itopod.tiers[current_tier]}')

                click(*coords.ITOPOD_ENTER, delay='fast')
                click(*coords.ITOPOD_START_INPUT, delay='fast')
                write(str(Itopod.tiers[current_tier]))
                click(*coords.ITOPOD_ENTER_CONFIRMATION, delay='fast')
                optimal = False
            elif not optimal:  # must be bigger than 1
                # can afford to go to optimal
                current_tier = minimum
                if verbose > 1:
                    print(f'going to optimal floor')

                click(*coords.ITOPOD_ENTER, delay='fast')
                click(*coords.ITOPOD_START_INPUT, delay='fast')
                click(*coords.ITOPOD_OPTIMAL, delay='fast')
                click(*coords.ITOPOD_ENTER_CONFIRMATION, delay='fast')
                optimal = True

            if verbose:
                print('*' * 20)

            if Itopod.kills % 50 == 0:
                print(f'total kills: {Itopod.kills}')
                print(f'total exp: {Itopod.EXP_gained}')
                print(f'total ap: {Itopod.AP_gained}')
                print(f'time: {round((time.time() - start)/60, 2)} minutes')

            if duration != 0 and time.time() - start > duration * 60:
                return

            if verbose:
                print(f'tiers: {Itopod.tierKillsCount}')


class Adventure:
    """ Various features related to Adventure menu. """
    # adventure zones
    # titans here need to have the same name as hovering over adv menu
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
             'bv': 16,
             'walderp': 17,
             'bdw': 18,
             'bae': 19,
             'beast': 20,
             'choco': 21, }

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
                      12: 'z',
                      13: 'x'}

    @staticmethod
    def getTitans() -> list:
        """ Get titans that are ready to kill. 

        Parse text from titan counter in adventure menu.
        """
        Navigation.menu('adventure')
        titans_ready = []
        text = Statistics.getText(region=coords.TITAN_COUNTER_REGION)
        lines = text.split('\n')
        for line in lines:
            if 'READY' in line:
                words = line.split()
                # titan namme before spawn
                titan = words[words.index('SPAWN')-1]
                # sometimes have extraneous symbols
                titan = Statistics.removeCharacters(titan).lower()
                titans_ready.append(titan)

        return titans_ready

    @staticmethod
    def killTitan(titan: str) -> None:
        """ Will kill TITAN. """
        Adventure.adventureZone(titan)
        start = time.time()
        # wait for 10s at max for spawn (in case titan ocr bugged)
        while time.time() - start < 10 and not Adventure.enemySpawn():
            sleep(0.03)
        Adventure.snipe(buffs=True)
        print(f'killed titan {titan}')

    @staticmethod
    def killTitans(titans: list, verbose: bool = True, use_fighting_loadout: bool = False) -> None:
        """ Kill all TITANS in list.

        Keep your full drop chance loadout as 1. 
        Keep your fighting loadout as 3 if you're using it. 
        Will reset your resources and retoggle your diggers. 

        Arguments:  
        titans                 -- list with titans to kill (from Adventure.getTitans). 

        Keyword arguments:  
        use_fighting_loadout  -- switch to loadout 3 for manual fights. Use this if you need to 
        mix some fight accs for your titan fight. 
        verbose                -- print output for debugging purposes. 
        """
        # loadout and diggers and kills
        Navigation.menu('inventory')

        if verbose:
            print('boosting cube')

        Inventory.boostCube()  # unclutter inventory

        if verbose:
            print('drop chance loadout')

        Inventory.loadout(1)  # drop chance
        # remembering previous diggers
        Navigation.menu('goldDiggers')
        # print('saving')
        click(*coords.SAVE_ACTIVE)
        # print('clearing')
        click(*coords.CLEAR_ACTIVE)

        if verbose:
            print('dc, adv, pp, exp diggers')

        GoldDiggers.activate(['DROP_CHANCE', 'ADVENTURE', 'PP', 'EXP'])

        if verbose:
            print('toggling autokill')

        # autokill should kill all previous titans
        click(*coords.CONFIG)
        click(*coords.AUTOKILL_TITAN_ON)
        click(*coords.AUTOKILL_TITAN_OFF)
        titans = Adventure.getTitans()
        # manually kill what's left

        if titans:
            if verbose:
                print('going to kill titans')
                print(f'titans: {titans}')

            # drop chanche and fighting accs
            if use_fighting_loadout:
                Navigation.menu('inventory')
                Inventory.loadout(3)

            Navigation.menu('adventure')
            Adventure.healHP()

            print('disabling beast mode')

            if Statistics.checkPixelColor(*coords.BEAST_MODE_ON, coords.BEAST_MODE_COLOR):
                click(*coords.BEAST_MODE)

            for t in titans:
                Adventure.killTitan(t)
        else:
            if verbose:
                print('no titans left')

        Navigation.menu('goldDiggers')
        click(*coords.CLEAR_ACTIVE)
        click(*coords.CAP_SAVED)

        if verbose:
            print(f'killed all titans')
            print('finished. you should change loadouts and diggers back now')

    @staticmethod
    def turnIdleOn() -> None:
        """ Enable Idle mode in Adventure. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        click(*coords.MY_HEALTH_BAR_BORDER)  # get rid of tooltip
        sleep(0.5)
        if (not Adventure.isIdle()):
            press('q')

    @staticmethod
    def turnIdleOff() -> None:
        """ Disable Idle mode. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        click(*coords.MY_HEALTH_BAR_BORDER)  # get rid of tooltip
        sleep(0.5)
        if (Adventure.isIdle()):
            press('q')

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

        return Statistics.checkPixelColor(*coords.IS_IDLE, coords.IS_IDLE_COLOR)

    @staticmethod
    def itopodFarm(floor: str = 'optimal') -> None:  # DEPRECATED # TODO remove?
        """ Enter ITOPOD in floor x. If no floor is specified, go to optimal.  

        Keyword arguments:  
        floor -- floor to enter.
        """
        Navigation.menu('adventure')
        click(*coords.ITOPOD_ENTER)
        if floor == 'optimal':
            click(*coords.ITOPOD_OPTIMAL)
        else:
            click(*coords.ITOPOD_START_INPUT)
            write(floor, interval=0.2)
            click(*coords.ITOPOD_END_INPUT)
            write(floor, interval=0.2)
        click(*coords.ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def itopodPush(floor: str = '500') -> None:
        """ Enter ITOPOD with starting floor MAX and ending floor x.

        Keyword arguments:  
        floor -- ending floor.
        """
        Navigation.menu('adventure')
        click(*coords.ITOPOD_ENTER)
        click(*coords.ITOPOD_MAX)
        click(*coords.ITOPOD_END_INPUT)
        write(floor, interval=0.2)
        click(*coords.ITOPOD_ENTER_CONFIRMATION)

    @staticmethod
    def adventureZone(zone: str = 'latest') -> None:
        """ Go to adventure zone ZONE.

        Keyword arguments:  
        zone -- zone to go to, by name specified in showZones.
        """
        Navigation.menu('adventure')
        click(*coords.GO_BACK_ZONE, button="right")   # start at 0
        if zone == 'latest':
            click(*coords.ADVANCE_ZONE, button="right")
        else:
            times = Adventure.zones[zone]
            for _ in range(times):
                click(*coords.ADVANCE_ZONE, delay="fast")
        # Navigation.adventureZone = zone  # update adventureZone variable #TODO have adv remember zones

    @staticmethod
    def sendAttacks() -> None:
        """ Cycle through attacks in adventure mode.

        Should be in Adventure menu already.
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        press('ytew')  # only attacks

    @staticmethod
    def kill(fast: bool = False, buffs: bool = False) -> None:
        """ Kill the current enemy.

        Should be used when you want to quickly farm with only basic attacks.  
        Use Adventure.snipe for more elaborate attacking patterns. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        while not Adventure.isEnemyDead():
            if fast:  # use only regular attacks
                press('w')
            else:  # use all attacks
                Adventure.sendAttacks()

    @staticmethod
    def getReadyAbilities(buffs: bool = False, fast: bool = True, verbose: bool = False) -> List[int]:
        """ Return the ready abilities as a list. 

        It uses different priorities if you are low on health or want to use buffs.
        Will return a single regular attack if no other ability is off cooldown. 

        Expected usage:  
        -> set fast flag if you want to quickly kill enemies and have no trouble doing so.  
        -> set buffs flag if you need to buff yourself for a difficult fight.  
        -> set verbose for debugging. 

        Keyword arguments:  
        buffs   -- if you also want to use buffs.  
        fast    -- if you only need to quickly attack.  
        verbose -- debugging purposes. 
        """
        ready = set()
        start = time.time()
        # sleep(0.1)
        img = Statistics.getScreenshot()
        end = time.time()
        if verbose:
            print(f'screenshot time: {end - start}')

        x0 = coords.ABILITY_1[0]
        y0 = coords.ABILITY_1[1]
        i = 0
        start = time.time()
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
            if Statistics.checkPixelColor(x, y, color, img=img):
                ready.add(i)
        end = time.time()
        if verbose:
            print(f'pixel color time: {end - start}')

        if not Statistics.checkPixelColor(*coords.MY_HEALTH_BAR_THRESHOLD, (236, 52, 52), img=img):
            # priority needing to heal
            if verbose:
                print('needs healing')
            if buffs:
                priority = [12, 8, 6, 13, 10, 7, 9, 11, 5, 4, 3, 2]
            else:
                priority = [12, 8, 6, 13, 10, 5, 4, 3, 2]
        else:
            # priority not needing to heal
            if verbose:
                print('no need to heal')
            if fast:
                priority = [5, 4, 2, 1]
            elif buffs:
                priority = [12, 10, 6, 7, 9, 11, 5, 4, 3, 2]
            else:
                priority = [12, 10, 5, 4, 3, 6, 2]

        # TODO
        # use an actual priority queue
        myQueue = []

        for ability in priority:
            if ability in ready:
                myQueue.append(ability)
        if not myQueue:
            myQueue.append(1)
        return myQueue

    @staticmethod
    def snipe(buffs: bool = False, verbose: bool = False, fast: bool = False):
        """ Kill an enemy using abilities. 

        Keyword arguments:  
        buffs   -- if you want to use buffs also.
        fast    --  if you only want to use quick attacks.  
        verbose -- for debugging purposes. 
        """
        # turn off idle
        queue = deque(Adventure.getReadyAbilities(buffs=buffs, fast=fast))

        if verbose:
            print(f'ABILITIES: {queue}')

        start = time.time()
        while not Adventure.isEnemyDead():  # checking for enemy text
            if not queue:  # no abilities in queue to use

                if verbose:
                    print(f'getting abilities queue')

                queue = deque(Adventure.getReadyAbilities(
                    buffs=buffs, fast=fast))

                if verbose:
                    print(f'ABILITIES: {queue}')

            ability = queue.popleft()  # ability to use now

            end = time.time()  # time till got new abilities

            # use the ability as specified by Adv. mapping
            press(Adventure.abilities_keys[ability])

            if verbose:
                print(f'time between attacks: {end - start}')

            start = time.time()

            # check if regular attack is ready (fastest ability)
            while not Statistics.checkPixelColor(*coords.ABILITY_1, coords.ABILITY_ROW_1_READY_COLOR):
                sleep(0.05)

    @staticmethod
    def isEnemyDead() -> bool:
        """ Return True if current enemy is dead, False otherwise. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        return Statistics.checkPixelColor(*coords.ENEMY_TEXT, coords.ENEMY_BACKGROUND)

    @staticmethod
    def isPlayerLow() -> bool:
        """ Returns True if player life is below 30% (approximately). 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        return Statistics.checkPixelColor(*coords.MY_HEALTH_BAR_THRESHOLD, (255, 255, 255))

    @staticmethod
    def isPlayerFull() -> bool:
        """ Return True if player life is above 95% (approximately). """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        return Statistics.checkPixelColor(*coords.MY_HEALTH_BAR_FULL, coords.HEALTH_BAR_RED)

    @staticmethod
    def healHP() -> None:
        """ Heal hp in the safe zone. """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in adventure menu!')
        Adventure.adventureZone('safe')
        while not Adventure.isPlayerFull():
            sleep(1)

    @staticmethod
    def enemySpawn() -> bool:
        """ Return True if there is an enemy in adventure zone. 

        Checks if the enemy health bar is red.  

        Should be in Adventure menu already. 
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        return not Adventure.isEnemyDead()
#        return Statistics.checkPixelColor(*coords.ENEMY_HEALTH_BAR_BORDER, coords.ENEMY_HEALTH_BAR_RED)

    @staticmethod
    def isBoss() -> bool:
        """ Return True if current enemy is a Boss. 

        Checks for the yellow crown on the adventure enemy.  

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        return Statistics.checkPixelColor(*coords.CROWN_LOCATION, coords.CROWN_COLOR)

    @staticmethod
    def refreshZone() -> None:
        """ Go to another zone and back for a new enemy to spawn. 

        Should be in Adventure menu already.  
        """
        if Navigation.currentMenu != 'adventure':
            raise Exception('should be in Adventure menu!')

        click(*coords.GO_BACK_ZONE)
        click(*coords.ADVANCE_ZONE)


class Augmentation:
    @staticmethod
    def augmentation(aug: int = 1, upgrade: bool = False):
        """ Allocate energy to augmentation.

        Keyword arguments:  
        aug     -- augmentation number, 1 is Danger Scissors.  
        upgrade -- if True, will allocate energy to aug update instead.
        """
        Navigation.menu('augments')
        if upgrade:
            x, y = coords.AUG1_UPGRADE[0], coords.AUG1_UPGRADE[1] + \
                (aug - 1) * coords.AUG_DIFF
        else:
            x, y = coords.AUG1[0], coords.AUG1[1] + (aug - 1) * coords.AUG_DIFF
        click(x, y)


class Inventory:
    @staticmethod
    def loadout(num: int) -> None:
        """ Wears loadout NUMBER. 

        Only supports loadouts 1 and 2 as of now.
        """
        Navigation.menu('inventory')
        if num == 1:
            click(*coords.LOADOUT1)
        if num == 2:
            click(*coords.LOADOUT2)
        if num == 3:
            click(*coords.LOADOUT3)

    @staticmethod
    def mergeItem(x: int, y: int) -> None:
        """ Merge item at X, Y (relative to game corner). """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        click(x, y, delay='fast')
        # two times to be sure
        press('d')
        press('d')

    @staticmethod
    def boostItem(x: int, y: int) -> None:
        """ Boost item at X, Y (relative to game corner). """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        click(x, y, delay='fast')
        # two times to be sure
        press('aa')
        press('a')

    @staticmethod
    def boostAndMergeEquipped() -> None:  # TODO add new acc slots
        """ Merge and boost all equipped items.  

        Feel free to change the order for your needs.  
        """
        Navigation.menu('inventory')
        Inventory.mergeItem(*coords.ACC1)
        Inventory.boostItem(*coords.ACC1)
        Inventory.mergeItem(*coords.ACC2)
        Inventory.boostItem(*coords.ACC2)
        Inventory.mergeItem(*coords.ACC3)
        Inventory.boostItem(*coords.ACC3)
        Inventory.mergeItem(*coords.WEAPON)
        Inventory.boostItem(*coords.WEAPON)
        Inventory.mergeItem(*coords.HEAD)
        Inventory.boostItem(*coords.HEAD)
        Inventory.mergeItem(*coords.LEGS)
        Inventory.boostItem(*coords.LEGS)
        Inventory.mergeItem(*coords.CHEST)
        Inventory.boostItem(*coords.CHEST)
        Inventory.mergeItem(*coords.BOOTS)
        Inventory.boostItem(*coords.BOOTS)

    @staticmethod
    def boostCube() -> None:
        """ Boost infinity cube. """
        Navigation.menu('inventory')
        click(*coords.CUBE, button="right")

    @staticmethod
    def boostInventory(slots: int = 36) -> None:
        """ Boost first SLOTS of inventory. 

        Will boost starting from the first one and by rows.  

        Keyword arguments:   
        slots -- number of slots to boost. 
        """
        Navigation.menu('inventory')

        num = 0
        x0 = coords.SLOT1[0]
        y0 = coords.SLOT1[1]
        i = 0
        j = 0
        click(x0, y0)  # boosting first item sometimes fail
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
    def mergeInventory(slots: int = 36) -> None:
        """ Merge first SLOTS of inventory. 

        Will boost starting from the first one and by rows.  

        Keyword arguments:  
        slots -- number of slots to merge. 
        """
        Navigation.menu('inventory')

        num = 0
        x0 = coords.SLOT1[0]
        y0 = coords.SLOT1[1]
        i = 0
        j = 0
        click(x0, y0)  # boosting first item sometimes fail
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
        """ Trash items at rows 4 and 5. 

        Be careful to not trash anything important.
        """
        Navigation.menu('inventory')
        for col in range(3, 5):
            for row in range(12):
                x = coords.SLOT1[0] + coords.INV_DIFF * row
                y = coords.SLOT1[1] + coords.INV_DIFF * col
                Inventory.trashItem(x, y)

    @staticmethod
    def trashItem(x, y):
        """ Trash item at X, Y (relative to game corner). 

        Be careful to not trash anything important.
        """
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
    def transformItem(loc: Tuple, verbose: bool = True):
        """ Transform item being hovered. 

        Keyword arguments:  
        loc -- location of the item as pyautogui Tuple.
        """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        center = pyautogui.center(loc)
        rawClick(*center)
        sleep(0.1)
        if verbose:
            print('checking transformable')
        if Inventory.checkTransformable():
            if verbose:
                print('is transformable')
            ctrlClick()

    @staticmethod
    def transformAll(image: str):
        """ Transform all items IMAGE if transformable.

        Arguments:
        image -- path to the image of item. 
        """
        Navigation.menu('inventory')
        locations = Inventory.locateAll(image)
        for loc in locations:
            Inventory.transformItem(loc)

    @staticmethod
    def locateAll(image: str, confidence: float = 0.8) -> Generator:
        """ Return a generator of the (absolute) locations of all items IMAGE. 

        Arguments:
        image -- path to the image of item.
        """
        Navigation.menu('inventory')
        inventory = Statistics.getScreenshot()
        locations = pyautogui.locateAll(
            image, inventory, confidence=confidence)
        return locations

    @staticmethod
    def locateItem(image: str, confidence: bool = 0.8) -> Tuple:
        """ Return the position of item in inventory, if exists. 

        This is a relative position to the game itself, without borders. If you want to 
        be able to click on this item, click at x, y+25 (25 px is the size of steam border).
        """
        Navigation.menu('inventory')
        click(334, 80, delay='long')  # get rid of tooltip
        inventory = Statistics.getScreenshot()
        loc = pyautogui.locate(image, inventory, confidence=confidence)
        return loc

    @staticmethod
    def getEmptySlots(debug: bool = False) -> int:  # TODO add support to multiple pages
        """ Return number of empty slots on first page of inventory. 

        Keyword arguments:  
        debug -- if set to True will hover onto all empty slots found.  
        """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        empty = Inventory.locateAll('images/empty-slot.png')
        return len(list(empty))  # empty is a generator

    @staticmethod
    def checkTransformable() -> bool:
        """ Check if item being hovered is transformable. """
        if Navigation.currentMenu != 'inventory':
            raise Exception('should be in Inventory menu!')

        region = (CORNER[0], CORNER[1], coords.GAME_WIDTH, coords.GAME_HEIGHT)
        if pyautogui.locateOnScreen('transformable.png', region=region) != None:
            return True
        return False


class TimeMachine:
    @staticmethod
    def addEnergy() -> None:
        """ Add energy to Time Machine. """
        Navigation.menu('timeMachine')
        click(*coords.TM_ADD_ENERGY)

    @staticmethod
    def addMagic() -> None:
        """ Add magic to Time Machine. """
        # click(*coords.TIME_MACHINE)
        Navigation.menu('timeMachine')
        click(*coords.TM_ADD_MAGIC)


class BloodMagic:
    @staticmethod
    def addMagic(magic=1, cap=False) -> None:
        """ Add magic to Blood Magic. 

        Keyword arguments:  :
        magic  -- magic number, starts at 1. 
        cap    -- if True, will try to cap magic instead. 
        """
        Navigation.menu('bloodMagic')

        if cap:
            x, y = coords.BM1_CAP[0], coords.BM1_CAP[1] + \
                (magic - 1) * coords.BM_DIFF
        else:
            x, y = coords.BM1_ADD[0], coords.BM1_ADD[1] + \
                (magic - 1) * coords.BM_DIFF
        click(x, y)

    @staticmethod
    def cap():
        """ Cap all blood magic spells.  """
        Navigation.menu('bloodMagic')

        click(*coords.BM_CAP_ALL)


class Wandoos:
    @staticmethod
    def addEnergy() -> None:
        """ Add energy to wandoos.  

        Will always CAP. 
        """
        Navigation.menu('wandoos')
        click(*coords.WANDOOS_ENERGY_CAP)

    @staticmethod
    def addMagic() -> None:
        """ Add magic to wandoos. 

        Will always CAP. 

        """
        Navigation.menu('wandoos')
        click(*coords.WANDOOS_MAGIC_CAP)


class MoneyPit:
    @staticmethod
    def moneyPit() -> None:
        """ Throw money into pit. """
        Navigation.menu('moneyPit')
        click(*coords.FEED_ME)
        click(*coords.FEED_YEAH)


class Rebirth:
    @staticmethod
    def rebirth() -> None:
        """ Rebirth. """
        Navigation.menu('rebirth')
        click(*coords.REBIRTH_BUTTON)
        click(*coords.REBIRTH_CONFIRMATION)


class NGU:
    @staticmethod
    def addEnergy(ngus: list):
        """ Add energy to list of NGUS. 

        Names should be in uppercase and spaces as underscores. """
        for ngu in ngus:
            click(*coords.NGUS_ENERGY[ngu])

    @staticmethod
    def addMagic(ngus: list):
        """ Add magic to list of NGUS. 

        Names should be in uppercase and spaces as underscores. """
        click(*coords.NGU_TO_MAGIC_BUTTON)
        for ngu in ngus:
            click(*coords.NGUS_MAGIC[ngu])


class Yggdrasil:
    @staticmethod
    def harvestAll() -> None:
        """ Harvest all max tiered fruits. """
        Navigation.menu('yggdrasil')
        click(*coords.HARVEST_ALL_MAX_TIER)

    @staticmethod
    def isHarvested(fruit: str) -> bool:
        """ Return True if fruit is harvested. 

        Argument:
        fruit -- string representing the name of the fruit you want to check. All caps and with underscores. """
        Navigation.menu('yggdrasil')
        pix = getCoords(*coords.FRUITS_IS_HARVESTED[fruit.upper()])
        return pyautogui.pixelMatchesColor(*pix, (255, 255, 255))

    @staticmethod
    def activate(fruit: str) -> None:
        """ Activate fruit in yggdrasil menu.

        If there is not enough resources idle, nothing happens.   
        If fruit is already activated, will harvest it. 

        Argument:
        fruit -- string representing the name of the fruit you want to check. All caps and with underscores.
        """
        Navigation.menu('yggdrasil')
        click(*coords.FRUITS[fruit.upper()])


class GoldDiggers:
    @staticmethod
    def clearActive() -> None:
        """ Clear active diggers. """
        Navigation.menu('goldDiggers')
        click(*coords.CLEAR_ACTIVE)

    @staticmethod
    def activate(diggers: List) -> None:
        """ Activate diggers in list. Pass list of UPPERCASE diggers names with underscores.  

        Example:  
        -> activate Magic Ngu and Drop Chance diggers:
        activate(['MAGIC_NGU', 'DROP_CHANCE'])

        Will pass through all diggers pages starting at 1 and activate diggers in there. 
        """
        page_1 = ['DROP_CHANCE', 'WANDOOS', 'STAT', 'ADVENTURE']
        page_2 = ['ENERGY_NGU', 'MAGIC_NGU', 'ENERGY_BEARD', 'MAGIC_BEARD']
        page_3 = ['PP', 'DAYCARE', 'BLOOD', 'EXP']

        click(*coords.DIGGERS_PAGE_1)
        for d in page_1:
            if d in diggers:
                click(*coords.DIGGERS[d])
        click(*coords.DIGGERS_PAGE_2)
        for d in page_2:
            if d in diggers:
                click(*coords.DIGGERS[d])
        click(*coords.DIGGERS_PAGE_3)
        for d in page_3:
            if d in diggers:
                click(*coords.DIGGERS[d])


class Misc:
    @staticmethod
    def reclaimEnergy() -> None:
        """ Reclaim all energy. """
        if Navigation.currentMenu == 'adventure':
            Navigation.menu('basicTraining')
        press('r')

    @staticmethod
    def reclaimMagic() -> None:
        """ Reclaim all magic. """
        if Navigation.currentMenu == 'adventure':
            Navigation.menu('basicTraining')
        press('t')

    @staticmethod
    def reclaimAll() -> None:
        """ Reclaim all resources. """
        if Navigation.currentMenu == 'adventure':
            Navigation.menu('basicTraining')
        press('r')
        press('t')

    @staticmethod
    def inputResource(amount='cap', idle=False, energy=True):
        """ Set input resource to AMOUNT. 

        Keyword arguments:   
        amount  -- cap, half or quarter.  
        idle    -- if True will consider only the idle energy. 
        """
        # menus with the input area
        possibleMenus = ['basicTraining', 'augments', 'advTraining',
                         'timeMachine', 'bloodMagic', 'wandoos', 'ngu']

        if Navigation.currentMenu not in possibleMenus:
            Navigation.menu('basicTraining')

        if energy:
            if not idle:
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
        else:
            if not idle:
                if amount == 'cap':
                    click(*coords.MAGIC_CUSTOM_AMOUNT_CAP)
                if amount == 'half':
                    click(*coords.MAGIC_CUSTOM_AMOUNT_HALF)
                if amount == 'quarter':
                    click(*coords.MAGIC_CUSTOM_AMOUNT_QUARTER_IDLE)
            else:
                if amount == 'cap':
                    click(*coords.MAGIC_CUSTOM_AMOUNT_CAP)
                if amount == 'half':
                    click(*coords.MAGIC_CUSTOM_AMOUNT_HALF_IDLE)
                if amount == 'quarter':
                    click(*coords.MAGIC_CUSTOM_AMOUNT_QUARTER)  # TODO put idle


class Questing:
    # to find in questing text ocr
    zones = {
        'sewers': 'sewers',
        'forest': 'forest',
        'security': 'hsb',
        'universe': '2d',
        'strange': 'avsp',
        'mega': 'mega',
        'beardverse': 'bv',
    }

    # questing global variables to tracking
    quests_completed = 0
    items_turned = 0
    items_needed = 0
    is_major = False
    quest_zone = ""
    is_completed = False

    @staticmethod
    def updateInfo() -> None:
        """ Get and update Questing variables: items_turned,
        items_needed, is_major, quest_zone.

        A quest must be active!
        """
        Navigation.menu('questing')
        click(100, 100)  # get rid of tooltip
        # print(f'getting text')
        # sleep(5)
        text = Statistics.getText(coords.QUESTING_TEXT_REGION)

        # print(f'text: {text}')
        if not text:
            print('there is not an active quest')
            return

        Questing.quest_zone = Questing.parseZone(text)  # get zone
        Questing.items_turned, Questing.items_needed = Questing.parseProgress(
            text)  # get progress
        # is quest completed
        Questing.is_completed = Questing.items_turned == Questing.items_needed
        Questing.is_major = Questing.isMajor(text)
        if Questing.is_completed:
            Questing.quests_completed += 1

    @staticmethod
    def status() -> None:
        """ Print general status of questing. """
        msg = f'quest in {Questing.quest_zone}'
        if Questing.is_major:
            msg = 'Major ' + msg
        else:
            msg = 'Minor ' + msg
        print(msg)
        print(f'Progress: {Questing.items_turned}/{Questing.items_needed}')
        print(f'Overall {Questing.quests_completed} quests completed.')

    @staticmethod
    def isMajor(text: str) -> bool:
        """ Return True if current quest is major. """
        return 'major' in text.lower()

    @staticmethod
    def parseZone(text: str) -> str:
        """ Return the zone specified by questing text. """
        for zone in Questing.zones:
            if zone in text.lower():
                return Questing.zones[zone]

    @staticmethod
    def findZone() -> str:
        """ Find the specified zone in questing text. """
        text = Statistics.getText(coords.QUESTING_TEXT_REGION)
        for zone in Questing.zones:
            if zone in text.lower():
                return Questing.zones[zone]

    @staticmethod
    def turnInItems(item: str) -> None:
        """ Find and right click on ITEM. """
        img = 'images/' + item + '.png'
        inv = Inventory.locateItem(img, confidence=0.9)
        if inv:  # it may be None if no item was located
            x, y, _, _ = inv
            click(x, y+25, button='right')
        else:
            print('did not locate item')

    @staticmethod
    def parseProgress(text: str) -> Tuple:
        """ Return the progress as a tuple (items_turned, items_needed). """
        lines = re.split('\n', text)
        # print(f'lines: {lines}')
        line = [line for line in lines if "PROGRESS" in line]
        # print(f'progress line: {line}')
        line = re.split('[/ ]', line[0])
        # print(f'lines split: {lines}')
        _, items_turned, items_needed = line
        # print(f'turned: {items_turned}, needed: {items_needed}')
        items_turned = Statistics.removeLetters(items_turned)
        items_needed = Statistics.removeLetters(items_needed)
        return items_turned, items_needed

    @staticmethod
    def getProgress() -> Tuple:
        """ Get and return current quest progress. 

        Should be in Questing menu!
        """
        text = Statistics.getText(coords.QUESTING_TEXT_REGION)
        lines = re.split('\n', text)
        # print(f'lines: {lines}')
        line = [line for line in lines if "PROGRESS" in line]
        # print(f'progress line: {line}')
        line = re.split('[/ ]', line[0])
        # print(f'lines split: {lines}')
        _, have, need = line
        print(f'have: {have}, need: {need}')
        return int(have), int(need)
        # return Statistics.getText(coords.QUESTING_PROGRESS_REGION)

    @staticmethod
    def isCompleted() -> bool:
        """ Return True if current quest is completed. 
        """
        Navigation.menu('questing')
        click(640, 100, delay='long')  # get rid of tooltip
        have, need = Questing.getProgress()
        return have == need

    @staticmethod
    def complete() -> None:
        """ Complete the current quest. 

        Should be in Questing menu!
        """
        click(*coords.QUESTING_COMPLETE_QUEST)

    @staticmethod
    def skip() -> None:
        """ Skip the current quest. 

        Should be in Questing menu!
        """
        click(*coords.QUESTING_SKIP_QUEST)
        click(*coords.QUESTING_SKIP_QUEST_CONFIRMATION)

    @staticmethod
    def start() -> None:
        """ Start a quest. 

        Should be in Questing menu!
        """
        click(*coords.QUESTING_COMPLETE_QUEST)  # position is the same as complete


if __name__ == "__main__":
    pass
