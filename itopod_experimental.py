from inventory import invManagement
from features import Adventure, Yggdrasil
from navigation import Navigation

totalTime = 0 
duration = 10 
while True:
    Navigation.menu('adventure')
    print('*' * 30)
    Adventure.itopodExperimental(duration=duration) 
    totalTime += duration 
    print(f'total exp: {Adventure.totalEXP}')
    print(f'total ap: {Adventure.totalAP}')
    print(f'kills: {Adventure.killCount}')
    print(f'total time: {totalTime} minutes')
    print('*' * 30)
    invManagement() 
    Yggdrasil.harvestAll() 

