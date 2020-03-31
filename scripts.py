from helper import *
from coords import *
from features import *
import time


def run15():
    start = time.time()
    BasicTraining.basicTraining()
    FightBosses.fightBosses()
    Adventure.adventureZone()
    # basic loop
    counter = 0
    timeElapsed = time.time() - start
    while ((timeElapsed)/60 < 13):  # until 13 minutes
        Adventure.farmZone(30)
        Misc.reclaimEnergy()
        BasicTraining.basicTraining()
        Augmentation.augmentation()
        FightBosses.fightBosses()
        if counter % 5 == 0:
            Inventory.boostAndMergeEquips()
        counter += 1
        timeElapsed = time.time() - start
    Misc.reclaimEnergy()
    Augmentation.augmentation(upgrade=True)
    Adventure.farmZone(30)
    FightBosses.fightBosses()
    MoneyPit.moneyPit()
    timeElapsed = time.time() - start
    while (timeElapsed/60 < 15):
        pyautogui.sleep(2)
    Rebirth.rebirt()


def farmAdventure():
    print('farming script')
    print('which zone: ')
    zones = ""
    for z in Adventure.zones.keys():
        zones += z + "  "
    print(zones)
    zone = input()
    print('would you like to kil only bosses? (y/n)')
    boss = input()
    print('would you like to kill GRB? (y/n)')
    titan = input()
    counter = 0
    start = time.time()
    while True:
        if boss == 'y':
            Adventure.killMonsters(zone=zone, bossOnly=True)
        else:
            Adventure.killMonsters(zone=zone)
        counter += 20
        Inventory.boostAndMergeEquips()
        if titan == 'y':
            Adventure.killTitan()
        print(f'killed {counter} monsters')
        print(f'{round((time.time() - start)/60)}min elapsed')
        print()
