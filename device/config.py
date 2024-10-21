from keycode import *

from colors import *

DEBUG = False
ENABLE_HOST_COMMS = False

DELAY = 0.01            # Delay between loops, if we're missing key presses lower this.
DELAY_SLEEPING = 0.5    # Delay between loop if the device is asleep
DELAY_ANIMATION = 0.05  # Delay to use between animation cycles, lower = faster anims

BRIGHTNESS_DEFAULT = int(0xFF / 10)  # LEDs are mad bright, lets save our retinas
BRIGHTNESS_STEP    = 1 # int(0xFF / 40)  # Jump ~2.5% at a time

# Keycodes listed here: https://docs.circuitpython.org/projects/hid/en/latest/api.html
# Each key can be
# - None            - Do nothing
# - Keycode         - Press a single key
# - Special keycode - Perform an action like change layer, reboot, bootloader, brightness+-
# - List of keycode - Press all keys simultaneously
KEYMAP_01 = [
    [HOME,       None,                  None,                 DEVICE_REBOOT],
    [None,               F,             None,                 BRIGHTNESS_PLUS],
    [None,               UP_ARROW ,     None,                 BRIGHTNESS_MINUS],
    [LEFT_ARROW, None,                  RIGHT_ARROW,  None],
    [None,               DOWN_ARROW,    None,                 [COMMAND, L]],
    [LAYER_PREV, PRINT_SCREEN,  None,                 LAYER_NEXT],
]

# The number of keys in this list should match the number of color maps exactly
# So each layer has a mapping for both LEDs and key presses, you can reuse layers if you want like:
# `LAYER_KEYMAPS = [ KEYMAP_01, KEYMAP_01, KEYMAP_01]
LAYER_KEYMAPS = [ KEYMAP_01, KEYMAP_01, KEYMAP_01 ]

COLORMAP_01 = [
    [GREEN, GREEN,   GREEN, GREEN],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [GREEN, FUSHIA,  AQUA,  GREEN],
]

COLORMAP_02 = [
    [RED,    RED,    RED,    RED],
    [YELLOW, YELLOW, YELLOW, YELLOW],
    [YELLOW, YELLOW, YELLOW, YELLOW],
    [YELLOW, YELLOW, YELLOW, YELLOW],
    [YELLOW, YELLOW, YELLOW, YELLOW],
    [GREEN,  FUSHIA, AQUA,   GREEN],
]

COLORMAP_03 = [
    [YELLOW, YELLOW, YELLOW, YELLOW],
    [FUSHIA, FUSHIA, FUSHIA, FUSHIA],
    [FUSHIA, FUSHIA, FUSHIA, FUSHIA],
    [FUSHIA, FUSHIA, FUSHIA, FUSHIA],
    [FUSHIA, FUSHIA, FUSHIA, FUSHIA],
    [GREEN,  FUSHIA, AQUA,   GREEN],
]

# You can define each layer as a map for each individual key or have an entire color for a layer
# like: `COLORMAP_01 = RED`
LAYER_COLORS = [ COLORMAP_01, COLORMAP_02, COLORMAP_03 ]