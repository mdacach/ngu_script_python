""" Navigation module. """
from coords import *
from helper import *


class Navigation:
    """ Class to navigate through menus. """

    menus = {
        'basicTraining': BASIC_TRAINING,
        'fightBoss': FIGHT_BOSS,
        'moneyPit': MONEY_PIT,
        'adventure': ADVENTURE,
        'inventory': INVENTORY,
        'augments': AUGMENTATION,
        'timeMachine': TIME_MACHINE,
        'bloodMagic': BLOOD_MAGIC,
        'wandoos': WANDOOS,
        'ngu': NGU,
        'yggdrasil': YGGDRASIL,
        'rebirth': REBIRTH_MENU,
    }

    @staticmethod
    def menu(m):
        """ Navigates to specified menu. """
        click(*menus[m])
