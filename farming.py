""" Farming script with command line arguments. """
import argparse
import time

import pyautogui

from features import Adventure, Inventory
from helper import Helper
from inventory import invManagement
from navigation import Navigation
from yggdrasil import ygg

sleep = Helper.sleep

parser = argparse.ArgumentParser()
parser.add_argument('zone',
                    help='the zone to farm')

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

parser.add_argument('--fast', '-f',
                    help='use only regular attacks',
                    action='store_true')

parser.add_argument('--slots',
                    help='slots to boost/merge',
                    type=int,
                    default=10)

parser.add_argument('--noygg',
                    help='do not harvest ygg',
                    action='store_true')

args = parser.parse_args()


def main():
    Helper.init()

    Adventure.adventureZone(args.zone)

    if args.verbose:
        print(f'farming zone {args.zone}')
        print(f'boss only: {args.boss}')
        print(f'kills until inv management: {args.kills}')

    Adventure.turnIdleOff()
    killCounter = 0
    lastKill = False
    while True:
        while not Adventure.enemySpawn():
            sleep(0.03)

        if Adventure.isBoss():
            if args.fast:
                Adventure.kill(fast=True)
            else:
                Adventure.snipe()
            killCounter += 1
            lastKill = True
            if args.verbose:
                print(f'killed: {killCounter}')

        else:
            if args.boss:
                Adventure.refreshZone()
                lastKill = False
            else:
                if args.fast:
                    Adventure.kill(fast=True)
                else:
                    Adventure.snipe()

                killCounter += 1
                lastKill = True

                if args.verbose:
                    print(f'killed: {killCounter}')

        if lastKill and killCounter % args.kills == 0:
            if args.verbose:
                print(f'inv management:')

            Adventure.turnIdleOn()

            Navigation.menu('inventory')
            emptySlots = Inventory.getEmptySlots()

            if args.verbose:
                print(f'empty slots: {emptySlots}')
            if emptySlots < 10:
                invManagement(boost=2, merge=0)
                if not args.noygg:
                    ygg()

            Navigation.menu('adventure')
            Adventure.turnIdleOff()


if __name__ == '__main__':
    main()
