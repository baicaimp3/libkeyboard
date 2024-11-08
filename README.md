# libkeyboard
用于Linux系统的桌面环境下的模拟键盘输入，支持信创系统，支持中文

## 依赖
  - Python 3
  - python-xlib (>=0.16)

## 使用
把libkeyboard文件夹复制到python目录的site-packages目录下
```python
from libkeyboard import keyboard_write, keyboard_group


keyboard_write("测试内容123")            # 模拟键盘打字
keyboard_group("ctrl", "a")             # ctrl+a
keyboard_group("ctrl", "shift", "a")    # ctrl+shift+a
```
