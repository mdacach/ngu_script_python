""" Farming script with command line arguments. """
import argparse
from helper import *
from coords import *
from features import *
from navigation import Navigation
from inventory import invManagement
from yggdrasil import ygg
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
parser.add_argument('--fast', '-f', help='use only regular attacks',
                    action='store_true')

parser.add_argument('--slots',
                    help='slots to boost/merge',
                    type=int,
                    default=10)

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
Adventure.turnIdleOff()
while True:
    if Adventure.enemySpawn():
        if args.boss:
            if Adventure.isBoss():
                if args.fast:
                    Adventure.kill(fast=True)
                else:
                    Adventure.kill(buffs=True)
                sleep(0.8) # with redliquid cd -> 0.8s
                pyautogui.press('w')
                killCounter += 1
                if args.verbose:
                    print(f'kill count: {killCounter}')
                # sleep(1)
                # pyautogui.press('d')
                killed = True
            else:
                killed = False
                Adventure.refreshZone()
        else:
            if args.fast:
                Adventure.kill(fast=True)
            else:
                Adventure.kill()
            sleep(0.8)
            pyautogui.press('w') 
            killCounter += 1
            if args.verbose:
                print(f'kill count: {killCounter}')
            # sleep(1)
            # pyautogui.press('d')
            killed = True

        if killed and killCounter > 0 and killCounter % args.kills == 0:

            print(f'inv management')
            print(f'time: {round((time.time() - start))/60} minutes')
            Adventure.turnIdleOn()
            #Adventure.adventureZone('safe')

            Navigation.menu('inventory')
            emptySlots = Inventory.getEmptySlots()
            print(f'empty slots: {emptySlots}')
            if emptySlots < 10:
                # Inventory.mergeInventory(slots=10)
                invManagement(slots=args.slots)
                # Inventory.trashItems()
                ygg()

            print(f'going back to adventure')
            Navigation.menu('adventure')
            #Adventure.adventureZone(args.zone)
            Adventure.turnIdleOff()
