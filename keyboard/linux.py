# coding=utf8

import Xlib
import Xlib.X
import Xlib.ext
import Xlib.XK
import contextlib
from Xlib.display import Display
from Xlib.ext.xtest import fake_input
from keyboard import Key, NORMAL_MODIFIERS
from util.xorg import display_manager, alt_gr_mask, alt_mask
from keyboard.keyboard_mapping import keyboardMapping as kmp


class KeyBoard(Display):
    def __init__(self):
        super().__init__()
        self.min_keycode      = self.display.info.min_keycode               # 最小键值
        self.max_keycode      = self.display.info.max_keycode               # 最大键值
        self.count            = self.max_keycode - self.min_keycode + 1     # 可注册的按键数量
        self.press_event      = Xlib.display.event.KeyPress                 # 按下键盘的事件
        self.release_event    = Xlib.display.event.KeyRelease               # 松开键盘的事件
        self.ctrl_press       = Xlib.X.KeyPress
        self.ctrl_release     = Xlib.X.KeyRelease
        self.register_mapping = {}      # {keysym: {keycode: 1, keyidx: 0}} 已注册的键盘映射表
        self.event_mapping    = {}      # {keysym: {keycode: 1, keyidx: 0, count: 1}} 被按下的次数
        self.modifiers        = set()
        self.closed           = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        try:
            if self.closed is False:
                self.close()
        except AttributeError:
            pass

    def key_to_keysym(self, key):
        """转文本码keysym"""
        _key = None
        keysym = None
        if key.lower() in ('ps', 'printscreen', 'print screen'):
            key = 'print_screen'
        if hasattr(Key, key.lower()):
            keysym = getattr(Key, key.lower()).value.vk
            _key = getattr(Key, key.lower()).value

        elif key in ("\n", "\r"):
            _key = Key.enter.value
            keysym = _key.vk

        elif key == "\t":
            _key = Key.Tab.value
            keysym = _key.vk

        elif key.lower() in {'win', 'cmd', 'winleft'}:
            keysym = Key.cmd.value.vk
            _key = Key.cmd.value

        elif key in kmp:
            keysym = kmp.get(key)
            _key = None

        elif len(key) != 1:
            self.pro_raise(Exception("字符长度必须为1"))
        else:
            keysym = self.char_to_keysym(key)
        return _key, keysym

    def _update_modifiers(self, key, is_press):
        """在key是ctrl,shift,slt时做记录"""
        if NORMAL_MODIFIERS.get(key, None):
            if is_press:
                self.modifiers.add(key)
            else:
                try:
                    self.modifiers.remove(key)
                except KeyError:
                    pass

    def press(self, key, register=False):
        """
        按下一个按键
        :param key: 键盘按键
        :param register: 当没有此按键时, 是否注册按键 出於安全考慮，只有在write()時，才爲True
        """
        _key, keysym = self.key_to_keysym(key)      # 获取对应的文本码
        if _key is not None:
            self._update_modifiers(_key, True)

        if kmp.get(key) is not None:
            keycode, keyidx = kmp.get(key), 0
            needshift = True if key.isupper() or key in '~!@#$%^&*()_+{}|:"<>?' else False
            if needshift:
                self._send_event(self.ctrl_press, kmp['shift'])     # 按下shift

            self._send_event(self.ctrl_press, kmp.get(key))

            if needshift:
                self._send_event(self.ctrl_release, kmp['shift'])   # 松开shift

        else:
            keycode, keyidx = self.get_keycode(keysym, register)        # 获取按键码
            if keycode is None:
                self.pro_raise(KeyError(f"没有此按键'{key}'"))
            event = self.press_event if not _key else self.ctrl_press
            self._send_event(event, keycode, keyidx)        # 发送键盘事件

        self.sync()
        # 记录事件
        if keysym in self.event_mapping:
            self.event_mapping[keysym]['count'] += 1
        else:
            self.event_mapping[keysym] = {"keycode": keycode, "keyidx": keyidx, "count": 1}

    def release(self, key):
        """松开一个按键"""
        _key, keysym = self.key_to_keysym(key)
        if _key is not None:
            self._update_modifiers(_key, False)

        if kmp.get(key) is not None:        # 热键
            keycode = kmp.get(key)
            self._send_event(self.ctrl_release, keycode)

        elif keysym in self.event_mapping:
            keycode, keyidx = self.event_mapping[keysym]["keycode"], self.event_mapping[keysym]['keyidx']
            event = self.release_event if not _key else self.ctrl_release
            self._send_event(event, keycode, keyidx)

        self.sync()
        # 清除事件记录
        if keysym in self.event_mapping:
            self.event_mapping[keysym]["count"] -= 1
            if self.event_mapping[keysym]["count"] == 0:
                del self.event_mapping[keysym]

    def _shift_statue(self, modifiers):
        return 0 | (alt_mask(self) if Key.alt in modifiers else 0) | (
            alt_gr_mask if Key.alt_gr in modifiers else 0) | (
            Xlib.X.ControlMask if Key.ctrl in modifiers else 0) | (
            Xlib.X.ShiftMask if Key.shift in modifiers else 0)

    def reset_keyboard(self):
        """重置键盘, 松开所有按键"""
        for keysym, data in self.event_mapping.items():
            keycode, keyidx, count = data["keycode"], data["keyidx"], data["count"]
            if count >= 0:
                for i in range(count):
                    self._send_event(self.release_event, keycode, keyidx)
                data['count'] = 0
        self.event_mapping = {}

    def _send_event(self, event, keycode, keyidx=0):
        """发送一个键盘事件"""
        with display_manager(self) as dm, self._modifiers as modifiers:
            if isinstance(event, int):
                Xlib.ext.xtest.fake_input(dm, event, keycode)
            else:
                window = dm.get_input_focus().focus
                send_event = getattr(window, "send_event", lambda _event: dm.send_event(window, _event))
                send_event(event(
                    detail=keycode,
                    state=keyidx | self._shift_statue(modifiers),
                    time=0,
                    root=dm.screen().root,
                    window=window,
                    same_screen=0,
                    child=Xlib.X.NONE,
                    root_x=0, root_y=0, event_x=0, event_y=0
                ))

    @property
    @contextlib.contextmanager
    def _modifiers(self):
        yield set(NORMAL_MODIFIERS.get(modifier, None) for modifier in self.modifiers)

    def get_all_mapping(self):
        """获取所有的键盘映射"""
        return self.get_keyboard_mapping(self.min_keycode, self.count)

    def get_void_keycode(self):
        """获取一个没有被注册的键值"""
        for _keycode, _keysym in enumerate(self.get_all_mapping()[128:]):
            if not any(_keysym):
                keyidx = 0
                return _keycode + self.min_keycode + 128, keyidx

        # 没有空余的按键, 从已注册的当中去一个没有被按键的按键
        for keysym, data in self.register_mapping.items():
            if keysym not in self.event_mapping or self.event_mapping[keysym].get('count', 0) == 0:
                return data["keycode"], data["keyidx"]
        self.pro_raise("没有空余的按键")

    def _update_register_mapping(self, keysym, keycode, keyidx):
        """修改已注册的按键映射表"""
        _temp = None
        for _keysym, data in self.register_mapping.items():
            if data["keycode"] == keycode and data["keyidx"] == keyidx:
                if keysym == _keysym:
                    _temp = _keysym
                    break
        if _temp:
            del self.register_mapping[_temp]
        self.register_mapping[keysym] = {"keycode": keycode, "keyidx": keyidx}

    def _register(self, keysym, keycode, keyidx):
        """注册按键 一般在内容是中文时才会调用"""
        mapping = self.get_all_mapping()
        mapping[keycode - self.min_keycode][0] = keysym
        with display_manager(self) as dm:
            mapping[keycode - self.min_keycode][keyidx] = keysym
            dm.change_keyboard_mapping(keycode, mapping[keycode - self.min_keycode: keycode - self.min_keycode + 1])
            self._update_register_mapping(keysym, keycode, keyidx)

        return keycode, keyidx

    def get_keycode(self, keysym, register=False):
        """符号码keysym转按键码keycode"""
        keycode = self.keysym_to_keycode(keysym)
        if keycode:
            try:
                all_kb = self.get_all_mapping()
                keyidx = all_kb[keycode - self.min_keycode].index(keysym)
                return keycode, keyidx
            except ValueError:
                return keycode, 0

        if keysym in self.register_mapping:     # 从已注册的里面找此按键
            return self.register_mapping[keysym]['keycode'], self.register_mapping[keysym]['keyidx']

        for keycode, mapping in enumerate(self.get_all_mapping()):      # 从键盘映射里面找此按键
            if mapping[0] == keysym:
                return keycode + self.min_keycode, 0
            elif mapping[1] == keysym:
                return keycode + self.min_keycode, 1

        if register:        # 没有找到此按键 注册一下
            keycode, keyidx = self._register(keysym, *self.get_void_keycode())
            return keycode, keyidx
        return None, None

    @staticmethod
    def char_to_keysym(char):
        """
        文本对应的文本码
        :param char: 长度为1的字符
        :return: 文本码 keysym
        """
        ordinal = ord(char)
        if ordinal < 0x100:
            return ordinal
        else:
            return ordinal | 0x01000000

    def clear_keycode(self, keycode):
        """清除一个按键"""
        mapping = self.get_all_mapping()
        max_num = len(mapping[keycode - self.min_keycode])
        with display_manager(self) as dm:
            mapping[keycode - self.min_keycode] = [0 for i in range(max_num)]
            dm.change_keyboard_mapping(keycode, mapping[keycode - self.min_keycode: keycode - self.min_keycode + 1])

    def clear_mapping(self):
        """
        清除所有注册的按键
        """
        if self.register_mapping:
            mapping = self.get_all_mapping()
            del_list = []
            with display_manager(self) as dm:
                for keysym, data in self.register_mapping.items():
                    mapping[data['keycode'] - self.min_keycode] = [0 for i in range(7)]
                    dm.change_keyboard_mapping(data['keycode'], mapping[data['keycode'] - self.min_keycode: data['keycode'] - self.min_keycode + 1])
                    del_list.append(keysym)

            for k in del_list:
                del self.register_mapping[k]

    def pro_raise(self, ex):
        """抛出异常"""
        self.close()
        raise ex

    def close(self):
        try:
            self.reset_keyboard()       # 松开所有按键
        except Exception as e:
            pass

        try:
            self.clear_mapping()        # 清除所有注册的按键
        except Exception as e:
            pass

        try:
            self.display.close()
            self.closed = True
        except Xlib.error.ConnectionClosedError:
            pass
