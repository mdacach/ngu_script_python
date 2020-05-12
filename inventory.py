""" Inventory management script. """
import time

import pyautogui

import coords
from helper import *
from features import Inventory
from navigation import Navigation


def invManagement(slots=10):
    print(f'should go to inventory!!')
    Navigation.menu('inventory')
    Inventory.boostAndMergeEquipped()
    Inventory.mergeInventory(slots=8)
    Inventory.boostInventory(slots=8)
    Inventory.boostCube()


if __name__ == '__main__':
    Navigation.menu('inventory')
    empty = Inventory.getEmptySlots(debug=True)
    print(f'empty slots: {empty}')
