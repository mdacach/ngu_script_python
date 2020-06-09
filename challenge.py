import argparse

import coords
from helper import Helper
from statistics import Statistics
from navigation import Navigation
import time

from features import Yggdrasil, FightBosses, Adventure, Inventory, Wandoos, Misc, Augmentation, TimeMachine, BloodMagic, Challenges, Rebirth, GoldDiggers

index = 0

parser = argparse.ArgumentParser()

parser.add_argument('challenge',
                    help='challenge to do. lowercase and underscore_separated')

args = parser.parse_args()


class ChallengeRuns:
    runs = [180, 180, 180, 180, 300, 300, 300, 600, 600, 900, 1800, 3600, 3600]
    current_run = 0  # index
    completed = 0

    @staticmethod
    def start(challenge: str):
        """ Start CHALLENGE.

        This is a wrapper for starting different challenges in this module.
        Arguments:
        challenge -- challenge name all lowercase and underscore_separated"""
        print(f'starting a {challenge.upper()} challenge')
        Challenges.start(challenge.upper())
        ChallengeRuns.current_run = 0
        print(f'arg: {challenge}')
        names = {  # mapping from name to challenge logic
            'basic': 'basic',
            'blind': 'basic',
            'no_ngu': 'basic',
            'no_tm': 'no_tm',
            'no_rebirth': 'no_rebirth',
        }
        challenge = names[challenge]
        print(f'starting {challenge} run')
        if challenge == 'basic':
            ChallengeRuns.basic(ChallengeRuns.runs[0])
        elif challenge == 'no_tm':
            ChallengeRuns.no_tm(ChallengeRuns.runs[0])
        elif challenge == 'no_rebirth':
            ChallengeRuns.no_rebirth()
        else:
            print('something went wrong. make sure you spelled the challenge correctly.')
            return

    @staticmethod
    def basic(duration: int):
        """ Basic challenge logic.

        Arguments:
        duration -- duration of current run.
        """

        start = time.time()

        Navigation.menu('fightBoss')
        FightBosses.nuke()
        Helper.sleep(3)  # wait for nuke
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

        while (time.time() - start < duration and (Statistics.checkPixelColor(*coords.TM_LOCKED, coords.BUTTON_LOCKED_COLOR)) or Statistics.checkPixelColor(*coords.TM_LOCKED, coords.TM_LOCKED_IRON_PILL)):
            print('before tm loop')
            Navigation.menu('wandoos')
            Wandoos.addEnergy(cap=True)
            Wandoos.addMagic(cap=True)

            Navigation.menu('augments')
            Misc.inputResource(amount='quarter', idle=True, energy=True)
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
            GoldDiggers.activate(['STAT', 'WANDOOS', 'MAGIC_BEARD'])
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
                GoldDiggers.activate(['STAT', 'WANDOOS', 'MAGIC_BEARD'])

                Challenges.update()

            kc += 1

            Navigation.menu('wandoos')
            Wandoos.addEnergy(cap=True)  # release some energy
            Wandoos.addMagic(cap=True)

            Navigation.menu('bloodMagic')
            for i in range(1, 8):
                BloodMagic.addMagic(magic=i, cap=True)

            Navigation.menu('timeMachine')
            TimeMachine.addMagic()

        Challenges.update()
        if Challenges.is_active():
            ChallengeRuns.current_run += 1
            cr = ChallengeRuns.current_run
            print(f'next duration: {ChallengeRuns.runs[cr]}')
            Navigation.menu('fightBoss')
            Helper.click(*coords.STOP)
            Rebirth.rebirth()
            ChallengeRuns.basic(ChallengeRuns.runs[cr])
            # main
        else:
            print('done with challenge')
            print('starting another one')
            ChallengeRuns.completed += 1
            print(f'completed: {ChallengeRuns.completed}')
            ChallengeRuns.start(args.challenge)

    @ staticmethod
    def no_tm(duration: int):
        """ Basic challenge logic without TM.

        Arguments:
        duration -- duration of current run.
        """

        start = time.time()

        Navigation.menu('fightBoss')
        FightBosses.nuke()
        Helper.sleep(3)  # wait for nuke
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

        while (time.time() - start < duration and (Statistics.checkPixelColor(*coords.TM_LOCKED, coords.BUTTON_LOCKED_COLOR) or Statistics.checkPixelColor(*coords.TM_LOCKED, coords.TM_LOCKED_IRON_PILL))):
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
            Navigation.menu('wandoos')
            Wandoos.addEnergy(cap=True)
            Wandoos.addMagic(cap=True)

            Navigation.menu('augments')
            Misc.inputResource(amount='half', idle=True, energy=True)
            Augmentation.augmentation(aug=5)
            Augmentation.augmentation(aug=4)

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

            Navigation.menu('wandoos')
            Wandoos.addEnergy(cap=True)
            Wandoos.addMagic(cap=True)

            kc = 0
            Challenges.update()

        while time.time() - start < duration and Challenges.is_active():
            print('final loop')

            Navigation.menu('wandoos')
            Wandoos.addEnergy(cap=True)  # release some energy
            Wandoos.addMagic(cap=True)

            Navigation.menu('bloodMagic')
            for i in range(1, 8):
                BloodMagic.addMagic(magic=i, cap=True)

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

                Challenges.update()

            kc += 1

        Challenges.update()
        if Challenges.is_active():
            ChallengeRuns.current_run += 1
            cr = ChallengeRuns.current_run
            print(f'next duration: {ChallengeRuns.runs[cr]}')
            Navigation.menu('fightBoss')
            Helper.click(*coords.STOP)
            Rebirth.rebirth()
            ChallengeRuns.no_tm(ChallengeRuns.runs[cr])
            # main
        else:
            print('done with challenge')
            print('starting another one')
            ChallengeRuns.completed += 1
            print(f'completed: {ChallengeRuns.completed}')
            ChallengeRuns.start(args.challenge)

    @ staticmethod
    def no_rebirth():
        """ No Rebirth challenge logic.

        Basically the same as basic challenge but with no rebirths.
        """

        Navigation.menu('fightBoss')
        FightBosses.nuke()
        Helper.sleep(3)  # wait for nuke
        FightBosses.fightBoss()

        Navigation.menu('inventory')
        Inventory.loadout(1)  # gold heavy

        Navigation.menu('adventure')
        Adventure.adventureZone()
        Adventure.turnIdleOn()

        # before augments
        Misc.inputResource(amount='cap', idle=False, energy=True)
        while Statistics.checkPixelColor(*coords.AUGS_LOCKED, coords.BUTTON_LOCKED_COLOR):
            print('before augments loop')
            Navigation.menu('wandoos')
            Wandoos.addEnergy(cap=False)
            Wandoos.addMagic(cap=False)
            Helper.sleep(5)
            Navigation.menu('fightBoss')
            FightBosses.nuke()
            FightBosses.fightBoss()

        Misc.reclaimEnergy()
        Misc.inputResource(amount='quarter', idle=True, energy=True)
        Misc.inputResource(amount='quarter', idle=True, energy=True)
        kc = 0

        while Statistics.checkPixelColor(*coords.TM_LOCKED, coords.TM_LOCKED_IRON_PILL) or Statistics.checkPixelColor(*coords.TM_LOCKED, coords.BUTTON_LOCKED_COLOR):
            print('before tm loop')

            Navigation.menu('augments')
            Augmentation.augmentation(aug=1)
            Augmentation.augmentation(aug=1)
            Augmentation.augmentation(aug=2)
            Augmentation.augmentation(aug=3)
            Augmentation.augmentation(aug=4)

            Navigation.menu('fightBoss')
            FightBosses.nuke()
            FightBosses.fightBoss()

            if kc % 5 == 0:
                Navigation.menu('adventure')
                Adventure.adventureZone()
            kc += 1

        Navigation.menu('inventory')
        Inventory.loadout(3)
        Misc.reclaimAll()
        kc = 0

        while Statistics.checkPixelColor(*coords.BM_LOCKED, coords.BUTTON_LOCKED_COLOR):
            print('before bm loop')
            Misc.inputResource(amount='quarter', idle=True, energy=True)
            Misc.inputResource(amount='quarter', idle=True, energy=True)
            for _ in range(2):
                TimeMachine.addEnergy()
                TimeMachine.addMagic()

            Navigation.menu('wandoos')
            Wandoos.addEnergy(cap=True)
            Wandoos.addEnergy(cap=True)
            Wandoos.addMagic(cap=True)
            Navigation.menu('augments')

            Misc.inputResource(amount='cap', idle=True, energy=True)
            Augmentation.augmentation(aug=5)
            Augmentation.augmentation(aug=5)
            Navigation.menu('fightBoss')
            FightBosses.nuke()
            FightBosses.fightBoss()
            if kc % 5 == 0:
                Navigation.menu('adventure')
                Adventure.adventureZone()
            kc += 1

        Misc.reclaimAll()

        Navigation.menu('bloodMagic')
        for i in range(1, 8):
            BloodMagic.addMagic(magic=i, cap=True)

        Navigation.menu('wandoos')
        Wandoos.addEnergy(cap=True)
        Wandoos.addMagic(cap=True)

        Navigation.menu('timeMachine')
        Misc.inputResource(amount='cap', idle=True, energy=False)
        TimeMachine.addMagic()
        Misc.inputResource(amount='quarter', idle=True, energy=True)
        TimeMachine.addEnergy()

        Navigation.menu('goldDiggers')
        GoldDiggers.clearActive()
        GoldDiggers.activate(['STAT', 'WANDOOS', 'MAGIC_BEARD', 'BLOOD'])

        kc = 0
        Challenges.update()
        print('final loop: ')
        print('augments, diggers, ygg, wandoos, bm')

        while Challenges.is_active():

            Navigation.menu('augments')
            Misc.inputResource(amount='half', idle=True, energy=True)
            Augmentation.augmentation(aug=(kc % 5)+1)
            Augmentation.augmentation(aug=(kc % 5)+1, upgrade=True)

            Navigation.menu('fightBoss')
            FightBosses.nuke()
            FightBosses.fightBoss()

            if kc % 5 == 0:
                Navigation.menu('adventure')
                Adventure.adventureZone()

                Navigation.menu('goldDiggers')
                GoldDiggers.clearActive()
                GoldDiggers.activate(
                    ['STAT', 'WANDOOS', 'MAGIC_BEARD', 'BLOOD'])

                Navigation.menu('yggdrasil')
                Yggdrasil.activate('POWER_ALPHA')
                Yggdrasil.activate('POWER_BETA')

                Challenges.update()
            kc += 1

            Navigation.menu('wandoos')
            Wandoos.addEnergy(cap=True)  # release some energy
            Wandoos.addMagic(cap=True)

            Navigation.menu('bloodMagic')
            for i in range(1, 8):
                BloodMagic.addMagic(magic=i, cap=True)

        print('done')
        print(f'starting another {args.challenge}')
        ChallengeRuns.completed += 1
        print(f'completed: {ChallengeRuns.completed}')
        ChallengeRuns.start(args.challenge)


if __name__ == '__main__':
    Helper.init()
    ChallengeRuns.start(args.challenge)

