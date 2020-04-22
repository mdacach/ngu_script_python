""" Inventory management script. """
from helper import *
from coords import *
from features import Inventory
from navigation import Navigation
import time
import pyautogui


def invManagement(slots=10):
    print(f'should go to inventory!!')
    Navigation.menu('inventory')
    Inventory.boostAndMergeEquipped()
    Inventory.mergeInventory(slots=slots)
    Inventory.boostInventory(slots=slots)
    Inventory.boostCube()


if __name__ == '__main__':
    Navigation.menu('inventory')
    empty = Inventory.getEmptySlots()
    print(f'empty slots: {empty}')
