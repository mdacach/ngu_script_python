import pyautogui
from coords import *
import time  # keep track of rebirth time


################INIT########################
# get corner pixel
CORNER = pyautogui.locateOnScreen("ingame-corner.png")
pyautogui.PAUSE = 0.01

# - 25 to account for ingame corner pixel


def moveTo(x, y):
    x = CORNER[0] + x
    y = CORNER[1] + y - 25
    pyautogui.moveTo


def click(x, y, button="left"):
    x = CORNER[0] + x
    y = CORNER[1] + y - 25
    pyautogui.click(x, y, button=button)
    pyautogui.sleep(0.5)

########################################


# runs


def run15():
    start = time.time()
    print("start")
    f.basicTraining()
    f.fightBosses()
    f.adjustAdventureZone()
    print('basic loop for 30 times')
    counter = 0
    while ((time.time() - start)/60 < 13):
        f.farmAdventure(30)
        reclaimEnergy()
        f.basicTraining()
        f.augmentation()
        f.fightBosses()
        if (counter % 5 == 0):
            i.handleEquips()
        counter += 1
    print('last part')
    reclaimEnergy()
    f.augmentation(upgrade=True)
    f.farmAdventure(30)
    f.fightBosses()
    f.moneyPit()
    while ((time.time() - start)/60 < 15):
        pyautogui.sleep(5)
    f.rebirth()
    print('end')


def run30():
    print('basic loop 3 times')
    for i in range(3):
        f.basicTraining()
        f.fightBosses()
        f.adjustAdventureZone()
        i.handleEquips()
        print('handle training')
        for i in range(3):
            print(f'loop {i+1}')
            pyautogui.sleep(30)
            reclaimEnergy()
            f.basicTraining()
            f.augmentation()
        f.farmAdventure(180)
        reclaimEnergy()
        f.basicTraining()
        f.augmentation()
        f.fightBosses()
        f.farmAdventure(180)
    print('final part')
    reclaimEnergy()
    f.basicTraining()
    reclaimEnergy()
    f.augmentation()
    f.farmAdventure(120)
    reclaimEnergy()
    f.augmentation(upgrade=True)
    f.farmAdventure(60)
    i.handleEquips()
    f.fightBosses()
    f.moneyPit()
    f.rebirth()


def main():
    print('initializing the script')
    print('scripts:')
    print("1 - speedrun")
    print("2 - farming")
    choice = input()
    if choice == "1":
        print('choose the length of the speedrun:')
        print('15 min')
        print('30 min')
        choice = input()

        print('requirements: ')
        print('check if adventure is in Idle Mode!')
        pyautogui.sleep(3)
        counter = 0
        while True:
            start = time.time()
            print('*******************')
            if choice == "15":
                run15()
            if choice == "30":
                run30()
            end = time.time()
            print(f'rebirth {counter} time: {round((end - start)/60)}')
            counter += 1
            print('*******************')
            print()
    if choice == "2":
        print('farming script')
        start = time.time()
        counter = 0
        while True:
            farming()
            counter += 1
            if (counter % 10):
                print(f'time elapsed: {round((time.time() - start)/60)}')


class Features:

    def basicTraining(self):
        click(*BASIC_TRAINING)
        click(*ATK1)
        click(*DEF1)
        click(*ATK2)
        click(*DEF2)
        click(*ATK3)
        click(*DEF3)
        click(*ATK4)
        click(*DEF4)
        click(*DEF5)
        click(*ATK5)

    def moneyPit(self):
        click(*MONEY_PIT)
        click(*FEED_ME)
        click(*FEED_YEAH)

    def rebirth(self):
        click(*REBIRTH_MENU)
        pyautogui.sleep(5)
        print("going to rebirth")
        click(*REBIRTH_BUTTON)
        click(*REBIRTH_CONFIRMATION)
        print("rebirth")

    def fightBosses(self):
        click(*FIGHT_BOSS)
        click(*NUKE)
        for i in range(5):
            pyautogui.sleep(2)
            click(*FIGHT)

    def adjustAdventureZone(self):
        click(*ADVENTURE)
        click(*ADVANCE_ZONE, button="right")

    def farmAdventure(self, time):
        self.adjustAdventureZone()
        pyautogui.sleep(0.5)
        pyautogui.press('q')
        pyautogui.sleep(0.5)
        for i in range(time):
            pyautogui.press('y')
            pyautogui.press('t')
            pyautogui.press('r')
            pyautogui.press('e')
            pyautogui.press('w')
            pyautogui.sleep(1)
        pyautogui.sleep(0.5)
        pyautogui.press('q')
        pyautogui.sleep(0.5)

    def augmentation(self, upgrade=False):
        click(*AUGMENTATION)
        if (upgrade):
            click(*AUG1_UPGRADE)
        else:
            click(*AUG1)


class Inventory:
    def mergeItem(self, x, y):
        global CORNER
        pyautogui.moveTo(CORNER[0] + x, CORNER[1] + y - 25)
        pyautogui.press('d')

    def boostItem(self, x, y):
        global CORNER
        pyautogui.moveTo(CORNER[0] + x, CORNER[1] + y - 25)
        pyautogui.press('a')

    def handleEquips(self):
        click(*INVENTORY)
        self.mergeItem(*HEAD)
        self.mergeItem(*CHEST)
        self.mergeItem(*LEGS)
        self.mergeItem(*BOOTS)
        self.mergeItem(*WEAPON)
        self.mergeItem(*ACC1)
        self.mergeItem(*ACC2)
        self.boostItem(*HEAD)
        self.boostItem(*CHEST)
        self.boostItem(*LEGS)
        self.boostItem(*BOOTS)
        self.boostItem(*WEAPON)
        self.boostItem(*ACC1)
        self.boostItem(*ACC2)

        x = SLOT1[0]
        y = SLOT1[1]
        # merge and boost front row
        for i in range(12):
            self.mergeItem(x + INV_DIFF * i, y)
            self.boostItem(x + INV_DIFF * i, y)

        # boost infinity cube
        click(*CUBE, button="right")

        # for i in range(12):
        #     for j in range(3):
        #         mergeItem(x + INV_DIFF * i, y + INV_DIFF * j)
        #         boostItem(x + INV_DIFF * i, y + INV_DIFF * j)


def farming():
    f.farmAdventure(60)
    i.handleEquips()


def reclaimEnergy():
    click(*BASIC_TRAINING)
    pyautogui.press('r')  # should reclaim energy


# helper classes
f = Features()
i = Inventory()

if __name__ == "__main__":
    main()
