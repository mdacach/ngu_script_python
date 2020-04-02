from helper import *
from coords import *
from features import *
import time


def run15():
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


def farmAdventure():
    print('farming script')
    print('which zone: ')
    zones = ""
    for z in Adventure.zones.keys():
        zones += z + "  "
    print(zones)
    zone = input() or 'latest'
    print('would you like to kil only bosses? (y/n)')
    boss = input() or 'n'
    print('would you like to kill GRB? (y/n)')
    titan = input() or 'n'
    kills = int(input("kills till inv management?")) or 50
    counter = 0
    start = time.time()
    while True:
        if boss == 'y':
            Adventure.killMonsters(zone=zone, bossOnly=True, kills=kills)
        else:
            Adventure.killMonsters(zone=zone, kills=kills)
        counter += kills
        Inventory.boostAndMergeEquips()
        if (counter > 0 and counter % 100 == 0):  # at every 400 kills
            Inventory.trashItems()
        if titan == 'y':
            Adventure.killTitan()
        MoneyPit.moneyPit()
        print(f'killed {counter} monsters')
        print(f'{round((time.time() - start)/60)}min elapsed')
        print()


def farmItopod():
    print('itopod farming script')
    floor = input('floor: ')
    Adventure.itopodFarm(floor=floor)
    pyautogui.press('q')
    start = time.time()
    while True:
        Adventure.kill()
        end = (time.time() - start)
        print(round(end/60))
        currentTime = round(end/60)
        if (currentTime % 10 == 0 and currentTime > 0):
            print('inventory management')
            Inventory.boostAndMergeEquips()
            Adventure.itopodFarm(floor=floor)
            currentTime += 1
