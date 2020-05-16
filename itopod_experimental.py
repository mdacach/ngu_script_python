from inventory import invManagement
from features import Adventure, Yggdrasil
from navigation import Navigation


totalEXP = 0 
totalTime = 0 
while True:
    Navigation.menu('adventure')
    print('*' * 30)
    totalEXP += Adventure.itopodExperimental(duration=10) 
    totalTime += 20
    print(f'total time: {totalTime}')
    print(f'total exp: {totalEXP}')
    print('*' * 30)
    invManagement() 
    Yggdrasil.harvestAll() 

