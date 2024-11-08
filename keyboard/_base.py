# coding=utf-8

import six
import enum
import unicodedata


class KeyCode(object):
    """
    A :class:`KeyCode` represents the description of a key code used by the
    operating system.
    """
    #: The names of attributes used as platform extensions.
    _PLATFORM_EXTENSIONS = []

    def __init__(self, vk=None, char=None, is_dead=False, **kwargs):
        self.vk = vk
        self.char = six.text_type(char) if char is not None else None
        self.is_dead = is_dead

        if self.is_dead:
            try:
                self.combining = unicodedata.lookup(
                    'COMBINING ' + unicodedata.name(self.char))
            except KeyError:
                self.is_dead = False
                self.combining = None
            if self.is_dead and not self.combining:
                raise KeyError(char)
        else:
            self.combining = None

        for key in self._PLATFORM_EXTENSIONS:
            setattr(self, key, kwargs.pop(key, None))
        if kwargs:
            raise ValueError(kwargs)

    def __repr__(self):
        if self.is_dead:
            return '[%s]' % repr(self.char)
        if self.char is not None:
            return repr(self.char)
        else:
            return '<%d>' % self.vk

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.char is not None and other.char is not None:
            return self.char == other.char and self.is_dead == other.is_dead
        else:
            return self.vk == other.vk and all(
                getattr(self, f) == getattr(other, f)
                for f in self._PLATFORM_EXTENSIONS)

    def __hash__(self):
        return hash(repr(self))

    @classmethod
    def from_vk(cls, vk, **kwargs):
        """Creates a key from a virtual key code.

        :param vk: The virtual key code.

        :param kwargs: Any other parameters to pass.

        :return: a key code
        """
        return cls(vk=vk, **kwargs)


class Key(enum.Enum):

    alt = 0
    alt_l = 0
    alt_r = 0
    alt_gr = 0

    backspace = 0

    caps_lock = 0

    cmd = 0
    cmd_l = 0
    cmd_r = 0

    ctrl = 0
    ctrl_l = 0
    ctrl_r = 0

    delete = 0



    end = 0

    enter = 0

    esc = 0

    f1 = 0
    f2 = 0
    f3 = 0
    f4 = 0
    f5 = 0
    f6 = 0
    f7 = 0
    f8 = 0
    f9 = 0
    f10 = 0
    f11 = 0
    f12 = 0
    f13 = 0
    f14 = 0
    f15 = 0
    f16 = 0
    f17 = 0
    f18 = 0
    f19 = 0
    f20 = 0

    up = 0
    down = 0
    left = 0
    right = 0
    home = 0


    page_down = 0

    page_up = 0


    shift = 0

    shift_l = 0

    shift_r = 0

    space = 0

    tab = 0


    media_play_pause = 0

    media_volume_mute = 0

    media_volume_down = 0

    media_volume_up = 0

    media_previous = 0

    media_next = 0

    insert = 0

    menu = 0

    num_lock = 0

    pause = 0

    print_screen = 0

    scroll_lock = 0
