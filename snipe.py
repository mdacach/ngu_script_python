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

Adventure.adventureZone(args.zone)

print(f'sniping {args.zone}')

start = time.time()
killCounter = 0

# while True:
