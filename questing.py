""" Script for doing quests. 
Command Line arguments:
--force_zone: will skip non-major quests until one in the desired zone.  
--verbose:    will print stuff (i.e time).  
--kills:      number of kills in zone before turning in items.  
"""
import argparse
import time

import coords

from features import Adventure, Questing, Inventory
from navigation import Navigation
from helper import Helper
from yggdrasil import ygg

sleep = Helper.sleep
printTime = Helper.printTime

parser = argparse.ArgumentParser()

parser.add_argument('--force_zone',
                    help='if the current quest is not major, will skip quests until one in the desired zone',
                    default='')

parser.add_argument('--verbose', '-v',
                    help='print stuff',
                    default=False,
                    action='store_true')

parser.add_argument('--kills', '-k',
                    help='kills between turning items',
                    default=50,
                    type=int)

args = parser.parse_args()

# start quest, get zone, farm zone, turn items, check if completed, if yes, repeat


def main():
    Helper.init()
    while True:
        Navigation.menu('questing')
        Questing.start()
        Questing.updateInfo()
        Questing.status()
        if args.force_zone:
            if Questing.is_major:
                print('major quest. will not skip')
            else:
                while Questing.quest_zone != args.force_zone:
                    Questing.skip()
                    Questing.start()
                    Questing.updateInfo()
                    Questing.status()

        Inventory.boostCube()  # unclutter inventory
        start = time.time()
        Adventure.adventureZone(Questing.quest_zone)
        Navigation.menu('questing')
        while not Questing.is_completed:
            Navigation.menu('inventory')
            # farm that zone
            Navigation.menu('adventure')
            Adventure.turnIdleOff()
            kc = 0
            while kc < args.kills:
                while not Adventure.enemySpawn():
                    sleep(0.03)
                # kill the enemy
                Adventure.snipe(fast=True)
                kc += 1

            if args.verbose:
                print(f'killed {args.kills} monsters')
                print(f'time: ', end='')
                printTime()

            Navigation.menu('inventory')
            Inventory.boostCube()
            # inv = Inventory.getEmptySlots()
            # if inv < 10:
            # Inventory.boostAndMergeEquipped()
            # Inventory.boostCube()
            Questing.turnInItems(Questing.quest_zone)
            # Inventory.mergeInventory(slots=5)
            ygg()
            Questing.updateInfo()
            if args.verbose:
                Questing.status()

            Navigation.menu('questing')
            if Questing.is_completed:
                Questing.complete()
                end = time.time()
                print(f'completed quest at ')
                printTime()
                print(f'duration: {round((end-start)/60, 2)} minutes')
                break


if __name__ == '__main__':
    print(f'starting questing script at ')
    printTime()
    main()
