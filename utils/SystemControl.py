import os
import time
import datetime

from win32.lib import win32con
from win32 import win32api, win32gui, win32print


def get_real_screen_resolution():
    """
    获取真实的分辨率
    :return:
    """
    hDC = win32gui.GetDC(0)
    width = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    height = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return {"width": width, "height": height}


def get_screen_size():
    """
    获取缩放后的分辨率
    :return:
    """
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)
    return {"width": width, "height": height}


def get_screen_scale():
    """
    获取屏幕的缩放比例
    :return:
    """
    real_resolution = get_real_screen_resolution()
    screen_size = get_screen_size()
    proportion = round(real_resolution['width'] / screen_size['width'], 2)
    return proportion


# print("屏幕真实分辨率：", get_real_screen_resolution()["width"], 'x', get_real_screen_resolution()["height"])
# print("缩放后的屏幕分辨率：", get_screen_size()["width"], 'x', get_screen_size()["height"])
# print("屏幕缩放比：", get_screen_scale())
