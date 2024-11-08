# coding=utf8

"""
@Author: baicaimp3
@Date: 2024/11/08
"""

import itertools
from ._xorg import Key, KeyCode


_MODIFIER_KEYS = (
    (Key.alt_gr, (Key.alt_gr.value,)),
    (Key.alt,    (Key.alt.value,   Key.alt_l.value,   Key.alt_r.value)),
    (Key.cmd,    (Key.cmd.value,   Key.cmd_l.value,   Key.cmd_r.value)),
    (Key.ctrl,   (Key.ctrl.value,  Key.ctrl_l.value,  Key.ctrl_r.value)),
    (Key.shift,  (Key.shift.value, Key.shift_l.value, Key.shift_r.value)))

#: Normalised modifiers as a mapping from virtual key code to basic modifier.
NORMAL_MODIFIERS = {
    value: key
    for combination in _MODIFIER_KEYS
    for key, value in zip(
        itertools.cycle((combination[0],)),
        combination[1])}
