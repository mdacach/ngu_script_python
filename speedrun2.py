""" Speedrun script with command line arguments. """

import argparse
import pyautogui
import time

import coords
from helper import sleep
from features import Adventure, Augmentation, BloodMagic, BasicTraining, FightBosses, Inventory, Misc, MoneyPit, Rebirth, TimeMachine
from navigation import Navigation


def run10():
    """ Perform a 10 minute run. """
    start = time.time()
    Inventory.loadout(2)  # loadout 2 is bars-heavy
    BasicTraining.basicTraining()
    FightBosses.fightBosses()
    Adventure.adventureZone()  # go to latest zone

    Misc.inputResource()  # all energy

    print(f'Time Machine loop for 5 minutes')
    while time.time() - start < 300:
        TimeMachine.addEnergy()
        TimeMachine.addMagic()
        print(f'sleeping for 30 seconds')
        sleep(30)

    Inventory.loadout(1)
    BasicTraining.basicTraining()

    Misc.reclaimAll()  # reclaim energy and magic from TM

    print(f'Main loop until 10 minutes')
    mainStart = time.time()
    pushAdventure = False
    while time.time() - start < 570:
        # push to new adventure zone
        if time.time() - mainStart > 120 and not pushAdventure:
            Adventure.adventureZone()
            pushAdventure = True
        print(f'sleeping 30 seconds')
        sleep(30)
        # fight bosses
        FightBosses.nuke()
        for _ in range(5):
            FightBosses.fightBoss()
        # augments
        Misc.inputResource(amount='quarter', idle=True)
        for _ in range(3):
            Augmentation.augmentation()
        Augmentation.augmentation(upgrade=True)
        # blood magic
        BloodMagic.addMagic(cap=True)

    MoneyPit.moneyPit()
    Navigation.menu('rebirth')
    while time.time() - start < 600:
        sleep(1)
    Rebirth.rebirth()


if __name__ == "__main__":
    print()
    print(f'speedrun script')
    print(f'10 minutes runs')

    runCounter = 0
    while True:
        print('*' * 15)
        runCounter += 1
        print(f'run {runCounter}')
        run10()
        print('*' * 15)
