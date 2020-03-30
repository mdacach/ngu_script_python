from scripts import *
import time


def main():
    print('starting the script')
    print('check if adventure is in Idle mode!')
    scriptStart = time.time()
    counter = 0
    while True:
        runStart = time.time()
        print('*' * 10)
        run15()
        runEnd = time.time()
        print(f'rebirth {counter} time: {round((runEnd - runStart)/60)}')
        counter += 1
        print()



if __name__ == "__main__":
    main()
