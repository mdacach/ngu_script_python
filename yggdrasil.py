""" Yggdrasil management script. """
import coords
from features import Yggdrasil
from navigation import Navigation


def ygg():
    Navigation.menu('yggdrasil')
    Yggdrasil.harvestAll()


if __name__ == '__main__':
    ygg()
