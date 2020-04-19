""" Module for sniping bosses. """
import argparse
from helper import *
from coords import *
from features import *
from navigation import Navigation
from inventory import invManagement
import time
import pyautogui

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
        sleep(1)
        press('w')
        killed = True
        Adventure.adventureZone('safe')
        while not Adventure.isPlayerFull():
            sleep(1)
        Adventure.adventureZone(args.zone)
    elif Adventure.enemySpawn() and not Adventure.isBoss():
        Adventure.refreshZone()
        killed = False
