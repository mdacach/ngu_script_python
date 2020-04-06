""" Scripts module. """
from helper import *
from coords import *
from features import *
import time


def run15():
    """ Performs a 15 minute run. """
    start = time.time()
    sleep(20)  # wait for energy to all trainings
    print('sleeping for 20s to have enough energy for training')
    BasicTraining.basicTraining()
    FightBosses.fightBosses()
    Adventure.adventureZone()
    # basic loop
    counter = 0
    timeElapsed = time.time() - start
    while ((timeElapsed)/60 < 13):  # until 13 minutes
        Misc.inputResource(amount='half', idle=True)
        Adventure.adventureZone()
        TimeMachine.addEnergy()
        Augmentation.augmentation()
        FightBosses.fightBosses()
        BloodMagic.addMagic()
        Adventure.itopodFarm()
        # Adventure.killMonsters(kills=10)
        Inventory.boostAndMergeEquips()
        timeElapsed = time.time() - start
        counter += 1
        if (counter % 30 == 0):
            Adventure.adventureZone()
            sleep(10)
    Misc.reclaimEnergy()
    Misc.inputResource()
    Augmentation.augmentation(upgrade=True)
    Adventure.adventureZone()
    FightBosses.fightBosses()
    MoneyPit.moneyPit()
    timeElapsed = time.time() - start
    print('time elapsed: ' + str(timeElapsed))
    while (timeElapsed/60 < 15):
        pyautogui.sleep(2)
        timeElapsed = time.time() - start
    FightBosses.fightBosses()
    Rebirth.rebirth()


def farmScript():
    """ Personal script to farming. """
    print('farming script')


def farmZone(zone='latest'):
    """ Farms an adventure zone. """
    Adventure.adventureZone(zone=zone)
    Adventure.turnIdleOff()
    killMonsters()


def killMonsters():
    """ Kills adventure monsters """
    while True:
        if Adventure.enemySpawn():
            Adventure.kill()
            pyautogui.press('d')  # to heal


def farmAdventure():
    """ Farms adventure zones. """
    print('starting farming script')

    print('which zone: (default latest)')
    Adventure.showZones()
    zone = input() or 'latest'

    print('kill bosses only? (default no)')
    boss = input() or 'n'

    print('would you like to kill last titan? (default no)')
    titan = input() or 'n'

    kills = input("kills till inv management? (default 50)") or 50
    kills = int(kills)

    counter = 0
    start = time.time()

    while True:
        if boss == 'y':
            Adventure.killMonsters(zone=zone, bossOnly=True, kills=kills)
        else:
            Adventure.killMonsters(zone=zone, kills=kills)
        counter += kills
        # if counter > 0 and counter % 300 == 0:
        #     print('transforming pendants')
        #     Inventory.transformPendants()

        Inventory.boostAndMergeEquipped()
        Inventory.mergeInventory()
        Inventory.boostInventory(slots=3)

        if (counter > 0 and counter % 300 == 0):  # at every 300 kills
            print('trashing items')
            Inventory.trashItems()
            Yggdrasil.harvestAll()
            Yggdrasil.activatePower()

        if titan == 'y':
            print('attempting to kill titan')
            Adventure.killTitan()

        MoneyPit.moneyPit()
        print(f'killed {counter} monsters')
        print(f'{round((time.time() - start)/60)} min elapsed')
        print()


def farmItopod():
    """ Farms ITOPOD. """
    print('itopod farming script')
    floor = input('floor: ')
    # Adventure.itopodFarm(floor=floor)
    Adventure.itopodPush(floor=floor)
    Adventure.turnIdleOff()
    counter = 0
    while True:
        if (Adventure.enemySpawn()):
            Adventure.kill()
            counter += 1
            if (counter % 25 == 0):
                # Inventory.boostInventory(slots=3)  # to farm boosts
                Inventory.boostAndMergeEquipped()
                click(*ADVENTURE)
