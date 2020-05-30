from inventory import invManagement
from features import Adventure, GoldDiggers, Itopod, Inventory, Misc, NGU, Yggdrasil
from navigation import Navigation

print(f'initial preparations')
Navigation.menu('inventory')
Inventory.loadout(2)
Navigation.menu('goldDiggers')
GoldDiggers.clearActive()
GoldDiggers.activate(['PP', 'EXP', 'ENERGY_NGU', 'MAGIC_NGU'])
Misc.inputResource(amount='half', idle=True, energy=True)
Navigation.menu('ngu')
NGU.addEnergy(['ADVENTURE_ALPHA', 'DROP_CHANCE'])
Misc.inputResource(amount='half', idle=True, energy=False)
NGU.addMagic(['YGGDRASIL', 'EXP'])

totalTime = 0
duration = 5
while True:
    titans = Adventure.getTitans()
    if titans:
        # after this needs to reset loadout and diggers and e/m
        Adventure.turnIdleOff()
        Adventure.killTitans(titans)
        Navigation.menu('inventory')
        Inventory.loadout(2)
        Inventory.boostCube()
        Navigation.menu('goldDiggers')
        GoldDiggers.clearActive()
        GoldDiggers.activate(['PP', 'EXP', 'ENERGY_NGU', 'MAGIC_NGU'])
        Misc.inputResource(amount='half', idle=True, energy=True)
        Navigation.menu('ngu')
        NGU.addEnergy(['ADVENTURE_ALPHA', 'DROP_CHANCE'])
        Misc.inputResource(amount='half', idle=True, energy=False)
        NGU.addMagic(['YGGDRASIL', 'EXP'])

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
