""" Speedrun script with command line arguments. """
import argparse
from helper import *
import coords
import features as f
from navigation import Navigation
import time
import pyautogui

# parser = argparse.ArgumentParser()
# parser.add_argument('--duration', help='duration of the run',
#                     default=10)
# args = parser.parse_args()

# print(args.duration)


def run7():
    """ Perfoms a 7 minute run. """
    start = time.time()
    f.BasicTraining.basicTraining()
    f.FightBosses.fightBosses()
    f.Adventure.adventureZone()
    # basic loop
    loopCounter = 0
    while (time.time() - start < 360):
        loopCounter += 1
        f.Misc.inputResource(amount='half', idle=True)
        f.TimeMachine.addEnergy()
        f.Augmentation.augmentation()
        f.BloodMagic.addMagic(cap=True)



def run10():
    """ Performs a 10 minute run. """
    start = time.time()
    f.BasicTraining.basicTraining()
    f.FightBosses.fightBosses()
    f.Adventure.adventureZone()
    # 10 min is 600 sec
    loopCounter = 0
    while (time.time() - start < 540):  # until 9 min
        loopCounter += 1
        f.Misc.inputResource(amount='half', idle=True)
        f.TimeMachine.addEnergy()
        f.Augmentation.augmentation()
        f.BloodMagic.addMagic(cap=True)
        f.Adventure.itopodFarm()
        f.FightBosses.fightBosses()
        if (loopCounter % 10 == 0):
            f.Adventure.adventureZone()
            print('sleeping for overall check')
            sleep(30)  # 30 sec to check on the run

    f.Misc.reclaimEnergy()
    f.Misc.reclaimMagic()
    f.Augmentation.augmentation(upgrade=True)
    f.FightBosses.fightBosses()
    f.MoneyPit.moneyPit()
    while (time.time() - start < 600):
        f.FightBosses()
    f.Rebirth.rebirth()
