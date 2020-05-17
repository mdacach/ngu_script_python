""" Inventory management script. """
import time

import pyautogui

import coords
from helper import *
from features import Inventory
from navigation import Navigation


def invManagement(slots=10):
    Navigation.menu('inventory')
    Inventory.boostAndMergeEquipped()
    Inventory.mergeInventory(slots=24)
    Inventory.boostInventory(slots=8)
    Inventory.boostCube()


if __name__ == '__main__':
    Navigation.menu('inventory')
    empty = Inventory.getEmptySlots()
    print(f'empty slots: {empty}')
