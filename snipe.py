""" Module for sniping bosses. 

Command-line arguments:  
--zone: zone to snipe.  
--verbose: print information.  
--heal: heal between fights.  
"""

import time
import argparse

from helper import Helper
from features import Adventure
from navigation import Navigation
from inventory import invManagement
from yggdrasil import ygg

sleep = Helper.sleep

parser = argparse.ArgumentParser()
parser.add_argument('zone',
                    help='zone to snipe.')

parser.add_argument('--verbose',
                    help='print information, default: False.',
                    default=False,
                    action='store_true')

parser.add_argument('--heal',
                    help='heal between fights in safezone, default: False',
                    default=False,
                    action='store_true')

args = parser.parse_args()


if args.verbose:
    print(f'args: {args}')


def main():
    Helper.init()

    if args.verbose:
        print(f'sniping {args.zone}')

    killCounter = 0
    Adventure.adventureZone(args.zone)
    while True:

        while not Adventure.enemySpawn():
            sleep(0.03)

        if Adventure.isBoss():
            Adventure.snipe(buffs=True)
            killCounter += 1

            if args.verbose:
                print(f'killed: {killCounter}')

            if killCounter % 50 == 0:
                if args.verbose:
                    print(f'inventory management')
                invManagement()
                if args.verbose:
                    print(f'harvesting ygg')
                ygg()

            Navigation.menu('adventure')

            if args.heal:
                Adventure.healHP()
                Adventure.adventureZone(args.zone)

        else:
            Helper.press('d')  # heal
            Adventure.refreshZone()


if __name__ == "__main__":
    main()
