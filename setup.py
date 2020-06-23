""" Script to setup resources in stuff. 

loadout -- inventory loadout (1-3).  
diggers -- array of strings representing the diggers. 
           # will assign from page 1 through 3.
ngus    -- dictionaries with key string and value int.
           special values:
             0 - all cap idle
             1 - half cap idle
             2 - quarter cap idle
inputs  -- deprecated. previously used for assigning resources to ngus.  
"""
import argparse

import coords
from helper import Helper
from navigation import Navigation
from features import Augmentation, BloodMagic, Inventory, GoldDiggers, NGU, Misc, Wandoos, TimeMachine


class Setup:
    presets = {
        'itopod': {
            'loadout': 2,
            'diggers': ['PP', 'EXP', 'ADVENTURE', 'ENERGY_NGU', 'MAGIC_NGU', 'DAYCARE', 'ENERGY_BEARD'],
            # 'diggers': ['PP', 'EXP', 'MAGIC_BEARD', 'ENERGY_NGU', 'MAGIC_NGU', 'DAYCARE'],
            # 'diggers': ['PP', 'EXP', 'ADVENTURE', 'ENERGY_NGU', 'MAGIC_NGU', 'MAGIC_BEARD'],
            'energy_ngus': {
                'AUGMENTS': 1e9,
                'WANDOOS': 1e9,
                'RESPAWN': 1e9,
                'GOLD': 1e9,
                'POWER_ALPHA': 1e9,
                'ADVENTURE_ALPHA': 3e9,
                'DROP_CHANCE': 2e10,
                # 'PP': 0,
                'MAGIC_NGU': 0,
            },
            'magic_ngus': {
                'YGGDRASIL': 4e9,
                'EXP': 9e9,
                # 'POWER_BETA': 1.5e10,
                # 'NUMBER': 0,
                # 'TIME_MACHINE': 0,
                # 'ENERGY_NGU': 0,
                'ADVENTURE_BETA': 0,
            },
            # 'tm': {
            # 'energy':
            # 'energy_input': {
            # 'amount': 'half',
            # # 'amount': 'cap',
            # 'idle': True,
            # 'energy': True,
            # },
            # 'magic_input': {
            # 'amount': 'half',
            # 'idle': True,
            # 'energy': False,
            # }
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

        # wandoos
        Navigation.menu('wandoos')
        Wandoos.addEnergy(cap=True)
        Wandoos.addMagic(cap=True)

        # time machine
        Navigation.menu('timeMachine')
        Misc.inputValue(1e9)
        TimeMachine.addEnergy()
        TimeMachine.addMagic()

        # augments
        Navigation.menu('augments')
        Augmentation.augmentation(aug=5)
        Augmentation.augmentation(aug=5, upgrade=True)

        # gold diggers
        Navigation.menu('goldDiggers')
        GoldDiggers.clearActive()
        GoldDiggers.activate(preset['diggers'])

        # advanced training
        Navigation.menu('advTraining')
        Helper.click(*coords.ADV_TOUGHNESS)
        Helper.click(*coords.ADV_POWER)
        Helper.click(*coords.ADV_BLOCK)
        Helper.click(*coords.ADV_WANDOOS_MAGIC)
        Helper.click(*coords.ADV_WANDOOS_ENERGY)

        # ngu
        Navigation.menu('ngu')
        print('waiting for e/m')
        Helper.sleep(65)
        # Misc.inputResource(**preset['energy_input'])
        NGU.addEnergy(preset['energy_ngus'])
        # Misc.inputResource(**preset['magic_input'])
        NGU.addMagic(preset['magic_ngus'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preset', '-p',
                        help='preset of what to run',
                        default='itopod')

    args = parser.parse_args()
    Setup.setup(args.preset)
