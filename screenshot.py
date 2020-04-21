import time

import d3dshot
import pyautogui
from mss import mss

print(f'd3dshot: ')
d = d3dshot.create()
start = time.time()
for i in range(100):
    d.screenshot()
end = time.time()

print(f'took 100 screenshots in {end-start} seconds.')
print(f'average of {100/(end-start)}/s.')

print()

print(f'pyautogui:')
start = time.time()
for i in range(100):
    pyautogui.screenshot()
end = time.time()

print(f'took 100 screenshots in {end-start} seconds.')
print(f'average of {100/(end-start)}/s.')

print()

print(f'mss:')
start = time.time()
with mss() as sct:
    for i in range(100):
        sct.shot()
end = time.time()

print(f'took 100 screenshots in {end-start} seconds.')
print(f'average of {100/(end-start)}/s.')
