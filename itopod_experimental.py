import argparse

from inventory import invManagement
from features import Adventure, GoldDiggers, Itopod, Inventory, Misc, NGU, Yggdrasil
from navigation import Navigation

parser = argparse.ArgumentParser()

parser.add_argument('--duration', '-d',
                    help='duration to run itopod script for',
                    type=int, default=5)

parser.add_argument('--nosetup',
                    help='will not set up diggers and ngu',
                    action='store_true')

parser.add_argument('--notitans',
                    help='disable killing titans',
                    action='store_true')

parser.add_argument('--verbose',
                    help='print output',
                    action='store_true')

parser.add_argument('--use_fighting_loadout',
                    help='use fighting loadout for manualing titans',
                    action='store_true')
parser.add_argument('--noygg',
                    help='do not harvest ygg',
                    action='store_true')

args = parser.parse_args()


def main():
    if not args.nosetup:
        if args.verbose:
            print(f'initial preparations')
        Navigation.menu('inventory')
        Inventory.loadout(2)
        Navigation.menu('goldDiggers')
        GoldDiggers.clearActive()
        GoldDiggers.activate(['PP', 'EXP', 'ENERGY_NGU', 'MAGIC_NGU'])
        Misc.inputResource(amount='half', idle=True, energy=True)
        Navigation.menu('ngu')
        NGU.addEnergy(['ADVENTURE_ALPHA', 'DROP_CHANCE'])
        Misc.inputResource(amount='half', idle=True, energy=False)
        NGU.addMagic(['YGGDRASIL', 'EXP'])

    totalTime = 0
    duration = args.duration
    while True:
        if not args.notitans:
            if args.verbose:
                print('getting available titans')
            titans = Adventure.getTitans()
            if titans:
                # after this needs to reset loadout and diggers and e/m
                Adventure.turnIdleOff()
                Adventure.killTitans(
                    titans, verbose=args.verbose, use_fighting_loadout=args.use_fighting_loadout)
                if args.verbose:
                    print('redoing setup')
                Navigation.menu('inventory')
                Inventory.loadout(2)
                Inventory.boostCube()
                # kill titans won't mess with gold diggers now
                # Navigation.menu('goldDiggers')
                # GoldDiggers.clearActive()
                # GoldDiggers.activate(['PP', 'EXP', 'ENERGY_NGU', 'MAGIC_NGU'])
                Misc.inputResource(amount='half', idle=True, energy=True)
                Navigation.menu('ngu')
                NGU.addEnergy(['ADVENTURE_ALPHA', 'DROP_CHANCE'])
                Misc.inputResource(amount='half', idle=True, energy=False)
                NGU.addMagic(['YGGDRASIL', 'EXP'])

        Navigation.menu('adventure')
        print('*' * 30)
        Itopod.itopodExperimental(duration=duration)
        totalTime += duration
        print(f'total exp: {Itopod.EXP_gained}')
        print(f'total ap: {Itopod.AP_gained}')
        print(f'kills: {Itopod.kills}')
        print(f'total time: {totalTime} minutes')
        print('*' * 30)

        Navigation.menu('inventory')
        if Inventory.getEmptySlots() < 10:
            invManagement()

        if not args.noygg:
            Yggdrasil.harvestAll()


if __name__ == '__main__':
    main()
