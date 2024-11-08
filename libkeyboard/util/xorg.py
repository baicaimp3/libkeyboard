# coding=utf8

"""
@Author: baicaimp3
@Date: 2024/11/08
"""

import contextlib
import Xlib.display
import Xlib.keysymdef
import Xlib.threaded
import Xlib.XK


class X11Error(Exception):
    pass


@contextlib.contextmanager
def display_manager(display):
    errors = []

    def handler(*args):
        errors.append(args)

    old_handler = display.set_error_handler(handler)
    try:
        yield display
        display.sync()
    finally:
        display.set_error_handler(old_handler)
    if errors:
        raise X11Error(errors)


def _find_mask(display, symbol):
    modifier_keycode = display.keysym_to_keycode(
        Xlib.XK.string_to_keysym(symbol))

    for index, keycodes in enumerate(display.get_modifier_mapping()):
        for keycode in keycodes:
            if keycode == modifier_keycode:
                return 1 << index
    return 0


def alt_mask(display):
    if not hasattr(display, '__alt_mask'):
        display.__alt_mask = _find_mask(display, 'Alt_L')
    return display.__alt_mask


def alt_gr_mask(display):
    if not hasattr(display, '__altgr_mask'):
        display.__altgr_mask = _find_mask(display, 'Mode_switch')
    return display.__altgr_mask
