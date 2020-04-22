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

args = parser.parse_args()


print(f'sniping {args.zone}')

start = time.time()
killCounter = 0
print('buffing')
Adventure.adventureZone(args.zone)
killed = False  # kill flag to only take action after kills
while True:
    if Adventure.enemySpawn() and Adventure.isBoss():
        Adventure.kill(buffs=True)
        # Adventure.buff()  # first thing every fight
        # sleep(1.1)
        # Adventure.snipe()
        sleep(1)
        press('w')
        killed = True
        killCounter += 1
        print(f'killed: {killCounter}')
        if killCounter % 50 == 0:
            print(f'inventory management')
            invManagement()
            print(f'harvesting ygg')
            ygg()
        Adventure.adventureZone('safe')
        while not Adventure.isPlayerFull():
            sleep(1)
        Adventure.adventureZone(args.zone)
    elif Adventure.enemySpawn() and not Adventure.isBoss():
        Adventure.refreshZone()
        killed = False
