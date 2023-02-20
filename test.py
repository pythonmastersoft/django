import pyautogui
import time
while True:
    time.sleep(60)
    pyautogui.moveTo(100, 100, duration=1)
    time.sleep(1)
    pyautogui.moveRel(300, 50, duration=1)

