""" Inventory management script. 

    Should only be called inside other scripts.
"""
from features import Inventory
from navigation import Navigation


def invManagement(boost=10, merge=10):
    Navigation.menu('inventory')
    # Inventory.boostAndMergeEquipped()
    # Inventory.boostInventory(slots=boost)
    # Inventory.mergeInventory(slots=merge)
    Inventory.boostCube()


if __name__ == '__main__':
    invManagement()
