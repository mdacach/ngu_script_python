""" Speedrun script with command line arguments. """
import argparse
from helper import *
import coords
import features as f
from navigation import Navigation
import time
import pyautogui

parser = argparse.ArgumentParser()
parser.add_argument('--duration', help='duration of the run',
                    default=3)
args = parser.parse_args()

print(args.duration)


def main():
    if (args.duration == 3):
        print('10 minute runs!')
        start = time.time()
        counter = 0
        while True:
            counter += 1
            print(f'run {counter}')
            print(f'time: {round((time.time() - start))} sec')
            run10()


def run3():
    """ Performs a 3 minute run. """
    start = time.time()
    f.BasicTraining.basicTraining()
    f.Inventory.loadout(2)
    f.FightBosses.fightBosses()
    f.Adventure.adventureZone()
    sleep(10)
    loopCounter = 0
    while (time.time() - start < 150):
        loopCounter += 1
        f.Misc.inputResource(amount='half', idle=True)
        f.TimeMachine.addEnergy()
        f.Augmentation.augmentation()
        f.BloodMagic.addMagic(cap=True)
        f.FightBosses.fightBosses()
        if loopCounter % 5 == 0:
            f.Adventure.adventureZone()
            f.Inventory.loadout(1)
        # if (loopCounter % 10 == 0):
        #     f.Adventure.adventureZone()
        #     print('sleeping for overall check')
        #     sleep(30)  # 30 sec to check on the run

    f.Misc.reclaimEnergy()
    f.Misc.reclaimMagic()
    f.Misc.inputResource(amount='cap', idle=True)
    f.Augmentation.augmentation(upgrade=True)
    f.FightBosses.fightBosses()
    f.MoneyPit.moneyPit()
    while (time.time() - start < 180):
        f.FightBosses()
    f.Rebirth.rebirth()


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
    # TIME MACHINE LOOP
    f.Misc.inputResource()

    print(f'Time Machine loop for 4 minutes')
    while (time.time() - start < 240):
        f.TimeMachine.addEnergy()
        f.TimeMachine.addMagic()

    f.Misc.reclaimAll()
    print(f'Main loop until 10 minutes')
    while (time.time() - start < 600):
        f.FightBosses.fightBosses()
        f.Misc.inputResource(amount='half')
        f.Augmentation.augmentation()
        f.Augmentation.augmentation(upgrade=True)
        f.BloodMagic.addMagic(cap=True)

    f.MoneyPit.moneyPit()
    f.Rebirth.rebirth()


if __name__ == "__main__":
    main()
