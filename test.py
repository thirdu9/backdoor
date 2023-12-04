# Just a file to test functionality

import pyautogui

#PyAutoGUI testing
    # im1 = pyautogui.screenshot()
    # im1.save('my_screenshot.png')
    # im2 = pyautogui.screenshot('my_screenshot2.png')

#Persistance Testing
import winreg as reg

# path = winreg.HKEY_CURRENT_USER

# software = winreg.OpenKeyEx(path, r"SOFTWARE\\")
# new_key = winreg.CreateKeyEx(software,'test3')



# winreg.SetValueEx(new_key, "newvalue2", 0 , winreg.REG_SZ, "hello world")

# if new_key:
#     winreg.CloseKey(new_key)

# key="HKEY_CURRENT_USER"
key_value=r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"

opening=reg.OpenKey(reg.HKEY_CURRENT_USER, key_value, 0, reg.KEY_ALL_ACCESS)

reg.SetValueEx(opening, "test", 0, reg.REG_SZ, r"Hello World2")

reg.CloseKey(opening)
