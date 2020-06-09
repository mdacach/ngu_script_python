""" Inventory management script. 

    Should only be called inside other scripts.
"""
from features import Inventory
from navigation import Navigation


def invManagement(slots=10):
    Navigation.menu('inventory')
    Inventory.boostAndMergeEquipped()
    Inventory.boostInventory(slots=slots)
    Inventory.mergeInventory(slots=slots)
    Inventory.boostCube()


if __name__ == '__main__':
    invManagement()
