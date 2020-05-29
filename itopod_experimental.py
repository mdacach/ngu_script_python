from inventory import invManagement
from features import Itopod, Inventory, Yggdrasil
from navigation import Navigation

totalTime = 0
duration = 5
while True:
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

    Yggdrasil.harvestAll()
