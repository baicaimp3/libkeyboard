# coding=utf8

"""
@Author: baicaimp3
@Date: 2024/11/08
"""

import time
from .keyboard.linux import KeyBoard


def keyboard_group(*args, interval=0.02):
    """
    模拟键盘的组合按键 group_press('ctrl', 'c')
    :param args:
    :param interval: 每个按键之间的间隔时间
    :return:
    """
    with KeyBoard() as keyboard:
        for key in args:
            keyboard.press(key)
            time.sleep(interval)
        for key in args[::-1]:
            keyboard.release(key)
            time.sleep(interval)


def keyboard_write(text, interval=0.02):
    """
    模拟键盘打字
    :param text: 需要打字的内容
    :param interval: 每个字符的间隔时间
    """
    if text in (None, ""):
        return

    with KeyBoard() as keyboard:
        for i in str(text):
            keyboard.press(i, True)
            keyboard.release(i)
            time.sleep(interval)
