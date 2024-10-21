from adafruit_hid.keycode import Keycode

globals().update({name: value for name, value in Keycode.__dict__.items() if not name.startswith('__')})

# Aliases
META = Keycode.COMMAND

# Custom Key Definitions
LAYER_PREV = 10001
LAYER_NEXT = 10002
BRIGHTNESS_PLUS = 10003
BRIGHTNESS_MINUS = 10004

DEVICE_REBOOT = 10010
DEVICE_BOOTLOADER = 10011

