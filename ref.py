import pyautogui
widgetwin = pyautogui.getWindowsWithTitle("Kim's Simple Widget")[0]

print(widgetwin)
if widgetwin.isActive == False:
    widgetwin.activate()