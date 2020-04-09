""" Inventory management script. """
from helper import *
from coords import *
from features import Inventory
from navigation import Navigation
import time
import pyautogui


def invManagement(slots):
    Inventory.boostAndMergeEquipped()
    Inventory.mergeInventory(slots=slots)
    Inventory.boostInventory(slots=slots)
    Inventory.boostCube()
