import argparse

import coords

from features import Adventure, GoldDiggers, Itopod, Inventory, Misc, NGU, Yggdrasil
from helper import Helper
from inventory import invManagement
from navigation import Navigation
from statistics import Statistics
from setup import Setup

parser = argparse.ArgumentParser()

parser.add_argument('--duration', '-d',
                    help='duration to run itopod script for',
                    type=int, default=5)

parser.add_argument('--nosetup',
                    help='will not set up diggers and ngu',
                    action='store_true')

parser.add_argument('--notitans',
                    help='disable killing titans',
                    action='store_true')

parser.add_argument('--verbose',
                    help='print output',
                    action='store_true')

parser.add_argument('--snipe',
                    help='use fighting loadout for manualing titans and first optimal rotation',
                    action='store_true')
parser.add_argument('--noygg',
                    help='do not harvest ygg',
                    action='store_true')

parser.add_argument('--nobeast',
                    help='do not use beast mode',
                    action='store_true')

parser.add_argument('--setup',
                    help='setup to use from setup script',
                    default='itopod')

args = parser.parse_args()

print(args)


def main():

    Helper.init()

    totalTime = 0
    duration = args.duration
    if args.nosetup:
        itopod_setup = True
    else:
        itopod_setup = False
    while True:
        if not args.notitans:
            if args.verbose:
                print('getting available titans')
            titans = Adventure.getTitans()
            if titans:
                # after this needs to reset loadout and diggers and e/m
                Adventure.turnIdleOff()

                print('calling killTitans with args.snipe {args.snipe}')
                Adventure.killTitans(
                    titans, verbose=args.verbose, snipe=args.snipe)

                itopod_setup = False

        if not itopod_setup:
            Setup.setup(args.setup)
            itopod_setup = True

        Navigation.menu('adventure')

        if not args.nobeast:
            if not Statistics.checkPixelColor(*coords.BEAST_MODE_ON, coords.BEAST_MODE_COLOR):
                Helper.click(*coords.BEAST_MODE)
        print('*' * 30)
        Itopod.itopodExperimental(duration=duration)
        totalTime += duration
        print(f'total exp: {Itopod.EXP_gained}')
        print(f'total ap: {Itopod.AP_gained}')
        print(f'kills: {Itopod.kills}')
        print(f'total time: {totalTime} minutes')
        print('*' * 30)

        Navigation.menu('inventory')
        if Inventory.getEmptySlots() < 10:
            invManagement(boost=2, merge=8)

        if not args.noygg:
            Yggdrasil.harvestAll()


if __name__ == '__main__':
    main()
