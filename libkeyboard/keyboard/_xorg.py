# coding=utf8

"""
@Author: baicaimp3
@Date: 2024/11/08
"""



import enum

import Xlib.display
import Xlib.ext
import Xlib.ext.xtest
import Xlib.X
import Xlib.XK
import Xlib.protocol
import Xlib.keysymdef.xkb
from . import _base


class KeyCode(_base.KeyCode):
    _PLATFORM_EXTENSIONS = (
        '_symbol',
    )

    _symbol = None

    @classmethod
    def from_symbol(cls, symbol, **kwargs):
        """Creates a key from a symbol.

        :param str symbol: The symbol name.

        :return: a key code
        """
        # First try simple translation
        keysym = Xlib.XK.string_to_keysym(symbol)
        if keysym:
            return cls.from_vk(keysym, _symbol=symbol, **kwargs)

        if not keysym:
            symbol = 'XK_' + symbol
            return cls.from_vk(getattr(Xlib.keysymdef.xkb, symbol, 0), _symbol=symbol, **kwargs)

    @classmethod
    def from_media(cls, name, **kwargs):
        return cls.from_symbol('XF86_Audio' + name, **kwargs)


class Key(enum.Enum):
    alt         = KeyCode.from_symbol('Alt_L')
    alt_l       = KeyCode.from_symbol('Alt_L')
    alt_r       = KeyCode.from_symbol('Alt_R')
    alt_gr      = KeyCode.from_symbol('Mode_switch')
    backspace   = KeyCode.from_symbol('BackSpace')
    caps_lock   = KeyCode.from_symbol('Caps_Lock')
    cmd         = KeyCode.from_symbol('Super_L')
    cmd_l       = KeyCode.from_symbol('Super_L')
    cmd_r       = KeyCode.from_symbol('Super_R')
    ctrl        = KeyCode.from_symbol('Control_L')
    ctrl_l      = KeyCode.from_symbol('Control_L')
    ctrl_r      = KeyCode.from_symbol('Control_R')
    delete      = KeyCode.from_symbol('Delete')
    down        = KeyCode.from_symbol('Down')
    end         = KeyCode.from_symbol('End')
    enter       = KeyCode.from_symbol('Return')
    esc         = KeyCode.from_symbol('Escape')
    f1          = KeyCode.from_symbol('F1')
    f2          = KeyCode.from_symbol('F2')
    f3          = KeyCode.from_symbol('F3')
    f4          = KeyCode.from_symbol('F4')
    f5          = KeyCode.from_symbol('F5')
    f6          = KeyCode.from_symbol('F6')
    f7          = KeyCode.from_symbol('F7')
    f8          = KeyCode.from_symbol('F8')
    f9          = KeyCode.from_symbol('F9')
    f10         = KeyCode.from_symbol('F10')
    f11         = KeyCode.from_symbol('F11')
    f12         = KeyCode.from_symbol('F12')
    f13         = KeyCode.from_symbol('F13')
    f14         = KeyCode.from_symbol('F14')
    f15         = KeyCode.from_symbol('F15')
    f16         = KeyCode.from_symbol('F16')
    f17         = KeyCode.from_symbol('F17')
    f18         = KeyCode.from_symbol('F18')
    f19         = KeyCode.from_symbol('F19')
    f20         = KeyCode.from_symbol('F20')
    home        = KeyCode.from_symbol('Home')
    left        = KeyCode.from_symbol('Left')
    page_down   = KeyCode.from_symbol('Page_Down')
    page_up     = KeyCode.from_symbol('Page_Up')
    right       = KeyCode.from_symbol('Right')
    shift       = KeyCode.from_symbol('Shift_L')
    shift_l     = KeyCode.from_symbol('Shift_L')
    shift_r     = KeyCode.from_symbol('Shift_R')
    space       = KeyCode.from_symbol('space', char=' ')
    tab         = KeyCode.from_symbol('Tab')
    up          = KeyCode.from_symbol('Up')

    media_play_pause    = KeyCode.from_media('Play')
    media_volume_mute   = KeyCode.from_media('Mute')
    media_volume_down   = KeyCode.from_media('LowerVolume')
    media_volume_up     = KeyCode.from_media('RaiseVolume')
    media_previous      = KeyCode.from_media('Prev')
    media_next          = KeyCode.from_media('Next')
    insert              = KeyCode.from_symbol('Insert')
    menu                = KeyCode.from_symbol('Menu')
    num_lock            = KeyCode.from_symbol('Num_Lock')
    pause               = KeyCode.from_symbol('Pause')
    print_screen        = KeyCode.from_symbol('Print')
    scroll_lock         = KeyCode.from_symbol('Scroll_Lock')
