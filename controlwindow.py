import pywinauto
import pygetwindow
import time

def getWindow():
    widgetwin = pygetwindow.getWindowsWithTitle("Kim's Simple Widget")[0]
    ActivateWindow(widgetwin)

def ActivateWindow(win):
    time.sleep(0.1)
    if win.isActive == False:
        pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
        win.activate()
        print("reactivate")
    ActivateWindow(win)