""" Navigation module. """
import coords
from helper import *


class Navigation:
    """ Class to navigate through menus. """

    menus = {
        'basicTraining': coords.BASIC_TRAINING,
        'fightBoss': coords.FIGHT_BOSS,
        'moneyPit': coords.MONEY_PIT,
        'adventure': coords.ADVENTURE,
        'inventory': coords.INVENTORY,
        'augments': coords.AUGMENTATION,
        'advTraining': coords.ADV_TRAINING,
        'timeMachine': coords.TIME_MACHINE,
        'bloodMagic': coords.BLOOD_MAGIC,
        'wandoos': coords.WANDOOS,
        'ngu': coords.NGU,
        'yggdrasil': coords.YGGDRASIL,
        'goldDiggers': coords.GOLD_DIGGERS,
        'rebirth': coords.REBIRTH_MENU,
        'exp': coords.EXP_MENU
    }

    currentMenu = ''
    adventureZone = ''

    @staticmethod
    def menu(m):
        """ Navigates to specified menu. """
        if (Navigation.currentMenu == m):  # already on menu
            return
        click(*Navigation.menus[m])
        Navigation.currentMenu = m
        sleep(0.5)
