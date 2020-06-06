import argparse

from helper import Helper
from navigation import Navigation
from features import BloodMagic, Inventory, GoldDiggers, NGU, Misc


class Setup:
    presets = {
        'itopod': {
            'loadout': 2,
            'diggers': ['PP', 'EXP', 'ADVENTURE', 'ENERGY_NGU', 'MAGIC_NGU'],
            'energy_ngus': ['ADVENTURE_ALPHA', 'DROP_CHANCE'],
            'magic_ngus': ['YGGDRASIL', 'EXP'],
            'energy_input': {
                'amount': 'half',
                'idle': True,
                'energy': True,
            },
            'magic_input': {
                'amount': 'half',
                'idle': True,
                'energy': False,
            }
        },
        'cblock': {
            'loadout': 2,
            'diggers': ['PP', 'EXP', 'ADVENTURE', 'ENERGY_NGU', 'MAGIC_NGU'],
            'energy_ngus': ['AUGMENTS', 'WANDOOS', 'GOLD', 'POWER_ALPHA'],
            'magic_ngus': ['POWER_BETA', 'NUMBER', 'TIME_MACHINE', 'YGGDRASIL'],
            'energy_input': {
                'amount': 'quarter',
                'idle': True,
                'energy': True,
            },
            'magic_input': {
                'amount': 'quarter',
                'idle': True,
                'energy': False,
            }
        }
    }

    @staticmethod
    def setup(preset='itopod'):

        preset = Setup.presets[preset]
        # print(preset)

        Helper.init()

        # loadout
        Navigation.menu('inventory')
        Inventory.loadout(preset['loadout'])

        # blood magic
        Navigation.menu('bloodMagic')
        BloodMagic.cap()

        # gold diggers
        Navigation.menu('goldDiggers')
        GoldDiggers.clearActive()
        GoldDiggers.activate(preset['diggers'])

        # ngu
        Navigation.menu('ngu')
        Misc.inputResource(**preset['energy_input'])
        NGU.addEnergy(preset['energy_ngus'])
        Misc.inputResource(**preset['magic_input'])
        NGU.addMagic(preset['magic_ngus'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
parser.add_argument('--preset', '-p',
                    help='preset of what to run',
                    default='itopod')

args = parser.parse_args()
Setup.setup(args.preset)
