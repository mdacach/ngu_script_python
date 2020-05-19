import argparse
import time 

import coords 

from features import Adventure, Questing, Inventory 
from navigation import Navigation 
from helper import sleep, printTime 
from yggdrasil import ygg 

parser = argparse.ArgumentParser() 

parser.add_argument('--force_zone',
                    help='if the current quest is not major, will skip quests until one in the desired zone',
                    default='')

args = parser.parse_args() 
# start quest, get zone, farm zone, turn items, check if completed, if yes, repeat 
def main():
    while True:
        start = time.time() 
        Navigation.menu('questing')
        Questing.start() 
        Questing.updateInfo() 
        Questing.status()
        if args.force_zone:
            if Questing.is_major:
                print('major quest. will not skip')
            else:
                while Questing.quest_zone != args.force_zone:
                    Questing.skip()
                    Questing.start()
                    Questing.updateInfo()
                    Questing.status() 

        # zone = Questing.findZone() 
        Adventure.adventureZone(Questing.quest_zone)
        Navigation.menu('questing')
        while not Questing.is_completed:
            Navigation.menu('inventory')
            Inventory.boostCube()
            # farm that zone 
            Navigation.menu('adventure')
            kc = 0 
            while kc < 50:
                while not Adventure.enemySpawn():
                    sleep(0.05)
                # kill the enemy
                Adventure.snipe(fast=True)
                kc += 1 
            print(f'killed 50 monsters')
            print(f'time: ', end='')
            printTime() 
            Navigation.menu('inventory')
            Inventory.boostAndMergeEquipped() 
            Inventory.boostCube()
            Questing.turnInItems(Questing.quest_zone)
            Inventory.mergeInventory(slots=5)
            ygg()
            Questing.updateInfo() 
            Questing.status() 
            Navigation.menu('questing')
            
            if Questing.is_completed:
                Questing.complete() 
                end = time.time()
                break
        

if __name__ == '__main__':
    print(f'starting questing script at ')
    printTime() 
    main()
