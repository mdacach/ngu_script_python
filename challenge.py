import argparse
import coords
from helper import Helper
from statistics import Statistics
from navigation import Navigation
import time

from features import FightBosses, Adventure, Inventory, Wandoos, Misc, Augmentation, TimeMachine, BloodMagic, Challenges, Rebirth, GoldDiggers

runs = [180, 180, 180, 180, 300, 300, 300, 600, 600, 900, 1800, 3600, 3600]
index = 0


def main(duration=180):
    start = time.time()

    Navigation.menu('fightBoss')
    FightBosses.nuke()
    Helper.sleep(3)
    FightBosses.fightBoss()

    Navigation.menu('inventory')
    Inventory.loadout(1)  # gold heavy

    Navigation.menu('adventure')
    Adventure.adventureZone()
    Adventure.turnIdleOn()


# before augments

    Misc.inputResource(amount='cap', idle=False, energy=True)
    while (time.time() - start < duration and Statistics.checkPixelColor(*coords.AUGS_LOCKED, coords.BUTTON_LOCKED_COLOR)):
        print('before augments loop')
        Navigation.menu('wandoos')
        Wandoos.addEnergy(cap=False)
        Wandoos.addMagic(cap=False)
        Helper.sleep(5)
        Navigation.menu('fightBoss')
        FightBosses.nuke()
        FightBosses.fightBoss()

    if time.time() - start < duration:
        Misc.reclaimEnergy()
        Misc.inputResource(amount='quarter', idle=True, energy=True)
        kc = 0

    while (time.time() - start < duration and Statistics.checkPixelColor(*coords.TM_LOCKED, coords.BUTTON_LOCKED_COLOR)):
        print('before tm loop')
        Navigation.menu('augments')
        Augmentation.augmentation(aug=1)
        Augmentation.augmentation(aug=2)
        Augmentation.augmentation(aug=3)
        Augmentation.augmentation(aug=4)
        Helper.sleep(5)
        Navigation.menu('fightBoss')
        FightBosses.nuke()
        FightBosses.fightBoss()
        if kc % 5 == 0:
            Navigation.menu('adventure')
            Adventure.adventureZone()
        kc += 1

    if time.time() - start < duration:
        Navigation.menu('inventory')
        Inventory.loadout(3)
        Misc.reclaimAll()
        kc = 0

    while (time.time() - start < duration and Statistics.checkPixelColor(*coords.BM_LOCKED, coords.BUTTON_LOCKED_COLOR)):
        print('before bm loop')
        Misc.inputResource(amount='quarter', idle=True, energy=True)
        Navigation.menu('timeMachine')
        for _ in range(2):
            TimeMachine.addEnergy()
            TimeMachine.addMagic()

        Navigation.menu('wandoos')
        Wandoos.addEnergy(cap=True)
        Wandoos.addMagic(cap=True)
        Navigation.menu('augments')

        Misc.inputResource(amount='cap', idle=True, energy=True)
        for _ in range(2):
            Augmentation.augmentation(aug=5)

        Navigation.menu('fightBoss')
        FightBosses.nuke()
        FightBosses.fightBoss()
        if kc % 5 == 0:
            Navigation.menu('adventure')
            Adventure.adventureZone()
        kc += 1

    if time.time() - start < duration:
        Misc.reclaimAll()
        Navigation.menu('bloodMagic')
        for i in range(1, 8):
            BloodMagic.addMagic(magic=i, cap=True)
        Misc.inputResource(amount='cap', idle=True, energy=False)
        Navigation.menu('timeMachine')
        TimeMachine.addMagic()
        Misc.inputResource(amount='quarter', idle=True, energy=True)
        TimeMachine.addEnergy()
        Navigation.menu('goldDiggers')
        GoldDiggers.clearActive()
        GoldDiggers.activate(['STAT', 'WANDOOS'])
        Navigation.menu('wandoos')
        Wandoos.addEnergy(cap=True)

        kc = 0
        Challenges.update()

    while time.time() - start < duration and Challenges.is_active():
        print('final loop')
        Navigation.menu('augments')
        Misc.inputResource(amount='half', idle=True, energy=True)
        Augmentation.augmentation(aug=(kc % 5)+1)
        Augmentation.augmentation(aug=(kc % 5)+1, upgrade=True)
        Helper.sleep(3)
        Navigation.menu('fightBoss')
        FightBosses.nuke()
        FightBosses.fightBoss()
        if kc % 5 == 0:
            Navigation.menu('adventure')
            Adventure.adventureZone()
            Navigation.menu('goldDiggers')
            GoldDiggers.clearActive()
            GoldDiggers.activate(['STAT', 'WANDOOS'])
        if kc % 20 == 0:
            Challenges.update()
        kc += 1
        Navigation.menu('wandoos')
        Wandoos.addEnergy(cap=True)  # release some energy
        Wandoos.addMagic(cap=True)
        Navigation.menu('timeMachine')
        TimeMachine.addMagic()

    Challenges.update()
    global index
    global runs
    if Challenges.is_active():
        index += 1
        print(f'current index: {index}')
        Navigation.menu('fightBoss')
        Helper.click(*coords.STOP)
        Rebirth.rebirth()
        main(runs[index])
        # main
    else:
        print('done with challenge')
        print('starting another one')
        index = 0
        Challenges.start('NO_REBIRTH')
        main(runs[index])


if __name__ == '__main__':
    Helper.init()
    main(runs[index])
