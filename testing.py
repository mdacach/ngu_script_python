""" Testing module. """
from features import *
from statistics import *
from navigation import Navigation
import helper

if __name__ == "__main__":
    print('testing')
    # BasicTraining.basicTraining()
    # print(Navigation.currentMenu)
    # FightBosses.fightBosses()
    # Adventure.isIdle()
    # Adventure.itopodFarm()
    # Navigation.menu('timeMachine')
    # Misc.inputResource()
    # print(Inventory.locateAll('pendant.png'))
    # Inventory.transformAll('flubber.png')
    # locations = Inventory.locateAll('flubber.png')
    # for loc in locations:
    #     sleep(0.5)
    #     # rawMove(*pyautogui.center(loc))
    #     Inventory.transformItem(loc)
    Inventory.loadout(2)
