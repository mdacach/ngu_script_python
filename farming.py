""" Farming script with command line arguments. """
import argparse
from helper import *
from coords import *
from features import *
from navigation import Navigation
import time
import pyautogui

parser = argparse.ArgumentParser()
parser.add_argument('zone', help='the zone to farm')
parser.add_argument('--boss', '-b',
                    help='kill only bosses',
                    action='store_true')
parser.add_argument('--kills', '-k',
                    help='kills between inv management',
                    type=int,
                    default=50)
parser.add_argument('--verbose', '-v',
                    help='print stuff',
                    action='store_true')

args = parser.parse_args()
print(args)

Adventure.adventureZone(args.zone)
print(Navigation.currentMenu)
killCounter = 0
if args.verbose:
    print(f'farming zone {args.zone}')
    print(f'boss only: {args.boss}')
    print(f'kills until inv management: {args.kills}')

start = time.time()
while True:
    if Adventure.enemySpawn():
        if args.boss:
            if Adventure.isBoss():
                Adventure.kill()
                killCounter += 1
                if args.verbose:
                    print(f'kill count: {killCounter}')
                sleep(1)
                pyautogui.press('d')
            else:
                Adventure.refreshZone()
        else:
            Adventure.kill()
            killCounter += 1
            if args.verbose:
                print(f'kill count: {killCounter}')
            sleep(1)
            pyautogui.press('d')
        if killCounter > 0 and killCounter % args.kills == 0:
            print(f'inv management')
            print(f'time: {round((time.time() - start))/60} minutes')
            Adventure.turnIdleOn()
            Inventory.boostAndMergeEquipped()
            Inventory.boostInventory(slots=5)
            Inventory.boostCube()
            # Inventory.mergeInventory(slots=4)
            if killCounter % 300 == 0:
                Inventory.trashItems()
                Yggdrasil.harvestAll()
            # go back to adventure
            print(f'going back to adventure')
            Navigation.menu('adventure')
            Adventure.turnIdleOff()
