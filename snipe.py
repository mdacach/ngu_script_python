""" Module for sniping bosses. """
import time
import argparse

import pyautogui

import coords 
from helper import *
from features import *
from navigation import Navigation
from inventory import invManagement
from yggdrasil import ygg

parser = argparse.ArgumentParser()
parser.add_argument('zone', help='zone to snipe', default='latest')

parser.add_argument('--verbose', help='verbose', default=False, action='store_true')

args = parser.parse_args()


def main(): 
    print(f'sniping {args.zone}')

    start = time.time()
    killCounter = 0
    print('buffing')
    Adventure.adventureZone(args.zone)
    killed = False  # kill flag to only take action after kills
    while True:
        if Adventure.enemySpawn() and Adventure.isBoss():
            Adventure.snipe(buffs=True)
            # Adventure.buff()  # first thing every fight
            # sleep(1.1)
            # Adventure.snipe()
            for i in range(2):
                sleep(0.9)
                press('w')
            killed = True
            killCounter += 1
            print(f'killed: {killCounter}')
            if killCounter % 50 == 0:
                print(f'inventory management')
                invManagement()
                print(f'harvesting ygg')
                ygg()
            Navigation.menu('adventure')
            Adventure.adventureZone('safe')
            while not Adventure.isPlayerFull():
               sleep(1)
            Adventure.adventureZone(args.zone)
        elif Adventure.enemySpawn() and not Adventure.isBoss():
            print('not boss')
            Adventure.refreshZone()
            killed = False
        # print('here')

if __name__ == "__main__":
    main()
