""" Inventory management script. 

    Should only be called inside other scripts.
"""
from features import Inventory
from navigation import Navigation


def invManagement(slots=10):
    Navigation.menu('inventory')
    Inventory.boostAndMergeEquipped()
    Inventory.boostInventory(slots=5)
    Inventory.mergeInventory(slots=10)
    Inventory.boostCube()


if __name__ == '__main__':
    invManagement()
