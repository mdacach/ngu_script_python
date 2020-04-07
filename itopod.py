""" Farming itopod script with fast attack """
import argparse
from helper import *
from coords import *
import features as f
from navigation import Navigation
import time
import pyautogui

parser = argparse.ArgumentParser()
parser.add_argument('--push', help='push to max possible floor')
parser.add_argument(
    '--fast', help='use only regular attacks to be faster', default=False)
parser.add_argument('--floor', help='floor to farm', default='optimal')

args = parser.parse_args()
print(args)


if args.floor != 'optimal':
    f.Adventure.itopodFarm(args.floor)
else:
    f.Adventure.itopodFarm()

start = time.time()
killCounter = 0
while True:
    Navigation.menu('adventure')
    f.Adventure.turnIdleOff()
    if f.Adventure.enemySpawn():
        if args.fast:
            f.Adventure.kill(fast=True)
        else:
            f.Adventure.kill()
        killCounter += 1

        if killCounter % 100 == 0:  # at every 100 kills
            f.Inventory.boostAndMergeEquipped()
            f.Inventory.boostInventory(slots=10)
            f.Inventory.boostCube()
            f.Inventory.mergeInventory(slots=3)

# add support to yggdrasil (TODO)
