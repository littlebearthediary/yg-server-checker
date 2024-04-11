import cv2
import numpy as np
import pyautogui
import time
import noti
import ctypes

def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def findAndClickYGIcon(screenshot, icon_path, threshold):
    icon_template = cv2.imread(icon_path)
    icon_h, icon_w, _ = icon_template.shape
    icon_res = cv2.matchTemplate(screenshot, icon_template, cv2.TM_CCOEFF_NORMED)
    icon_loc = np.where(icon_res >= threshold)

    if len(icon_loc[0]) > 0:
        print(f"Open YG Launcher.")
        icon_x = icon_loc[1][0] + icon_w // 2
        icon_y = icon_loc[0][0] + icon_h // 2

        pyautogui.moveTo(icon_x, icon_y, duration=0.1)
        time.sleep(0.1)
        pyautogui.click(clicks=2, interval=0.2)

def checkMaintainPopup(screenshot, maintain_path, threshold):
    maintain_template = cv2.imread(maintain_path)
    maintain_h, maintain_w, _ = maintain_template.shape
    maintain_res = cv2.matchTemplate(screenshot, maintain_template, cv2.TM_CCOEFF_NORMED)
    maintain_loc = np.where(maintain_res >= threshold)

    if len(maintain_loc[0]) > 0:
        print(f"YG Server Offline.")
        print(f"Close YG Launcher.")
        maintain_x = maintain_loc[1][0] + maintain_w // 2
        maintain_y = maintain_loc[0][0] + maintain_h // 2

        pyautogui.moveTo(maintain_x, maintain_y, duration=0.1)
        time.sleep(0.1)
        pyautogui.click(clicks=2, interval=0.2)
        return False
    else:
        noti.send_line_notification(f"YG Server Online.")
        return True

def main(icon_path, maintain_path, threshold = 0.8):
    while True:
        screenshot = capture_screen()

        findAndClickYGIcon(screenshot, icon_path, threshold)
        time.sleep(3)

        screenshot = capture_screen()

        if checkMaintainPopup(screenshot, maintain_path, threshold):
            break

if __name__ == "__main__":
    main_path = "images/"
    icon_path = f"{main_path}yg_icon.png"
    maintain_path = f"{main_path}maintain.png"

    version = "v1.0.0"

    ctypes.windll.kernel32.SetConsoleTitleW(f"YG Server Checker {version}")

    main(icon_path, maintain_path)