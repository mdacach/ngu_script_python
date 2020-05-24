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
    Inventory.boostInventory(slots=3)
    Inventory.mergeInventory(slots=5)
    Inventory.boostCube()


if __name__ == '__main__':
    Navigation.menu('inventory')
    empty = Inventory.getEmptySlots()
    print(f'empty slots: {empty}')
