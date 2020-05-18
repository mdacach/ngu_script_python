import argparse
import time 

import coords 

from features import Adventure, Questing, Inventory 
from navigation import Navigation 
from helper import sleep 

# start quest, get zone, farm zone, turn items, check if completed, if yes, repeat 
def main():
    quests_completed = 0 
    while True:
        if quests_completed:
            print(f'completed a quest')
            print(f'quests completed: {quests_completed}')
            print(f'time: {round((end-start)/60, 2)} min')

        start = time.time() 
        Navigation.menu('questing')
        Questing.start() 
        zone = Questing.findZone() 
        Adventure.adventureZone(zone)
        Navigation.menu('questing')
        while not Questing.isCompleted():
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
            Navigation.menu('inventory')
            Inventory.boostCube()
            Questing.turnInItems(zone)
            Navigation.menu('questing')
            if Questing.isCompleted():
                quests_completed += 1
                Questing.complete() 
                end = time.time()
        

if __name__ == '__main__':
    print(f'starting questing script at {time.strftime("%H:%M:%S", time.localtime())}')
    main()