from keycode import *

from colors import *

DEBUG = False
ENABLE_HOST_COMMS = False

DELAY = 0.01            # Delay between loops, if we're missing key presses lower this.
DELAY_SLEEPING = 0.5    # Delay between loop if the device is asleep
DELAY_ANIMATION = 0.05  # Delay to use between animation cycles, lower = faster anims

BRIGHTNESS_DEFAULT = int(0xFF / 10)  # LEDs are mad bright, lets save our retinas
BRIGHTNESS_STEP    = 3 # int(0xFF / 40)  # Jump ~2.5% at a time

# Keycodes listed here: https://docs.circuitpython.org/projects/hid/en/latest/api.html
# Each key can be
# - None            - Do nothing
# - Keycode         - Press a single key
# - Special keycode - Perform an action like change layer, reboot, bootloader, brightness+-
# - List of keycode - Press all keys simultaneously

TOP_LAYER = [HOME, END, PAGE_UP, PAGE_DOWN]
BOTTOM_LAYER = [LAYER_PREV, PRINT_SCREEN, DEVICE_REBOOT, LAYER_NEXT]


SHRUGGIE = [CONTROL, SHIFT, ALT, S]
SWITCH_PHP = [CONTROL, SHIFT, ALT, P]
SWITCH_PYCHARM = [CONTROL, SHIFT, ALT, Y]
SWITCH_CAIDO = [CONTROL, SHIFT, ALT, C]

SWITCH_DISCO = [CONTROL, SHIFT, ALT, D]
SWITCH_SIGNAL = [CONTROL, SHIFT, ALT, N]

SWITCH_FIREFOX = [CONTROL, SHIFT, ALT, F]
SWITCH_CHROMIUM = [CONTROL, SHIFT, ALT, H]


SWITCH_OBSIDIAN = [CONTROL, SHIFT, ALT, O]
SWITCH_KATE = [CONTROL, SHIFT, ALT, K]
SWITCH_DOLPHIN = [CONTROL, SHIFT, ALT, L]

XKILL = [CONTROL, SHIFT, ESCAPE]

# Numeric keypad layout
KEYMAP_00 = [
    TOP_LAYER,
    [SEVEN, EIGHT, NINE, BRIGHTNESS_PLUS],
    [FOUR, FIVE, SIX, BRIGHTNESS_MINUS],
    [ONE, TWO, THREE, SHRUGGIE],
    [ZERO, ZERO, PERIOD, "hello"],
    BOTTOM_LAYER,
]

# Shortcut layer
KEYMAP_01 = [
    TOP_LAYER,
    [SWITCH_PHP, SWITCH_PYCHARM, None, SWITCH_DISCO],
    [SWITCH_CAIDO, None, None, SWITCH_SIGNAL],
    [None, SWITCH_OBSIDIAN, SWITCH_KATE, SWITCH_DOLPHIN],
    [SWITCH_FIREFOX, SWITCH_CHROMIUM, None, XKILL],
    BOTTOM_LAYER,
]

KEYMAP_02 = [
    TOP_LAYER,
    [None, None, None, BRIGHTNESS_PLUS],
    [None, UP_ARROW, None, BRIGHTNESS_MINUS],
    [LEFT_ARROW, DOWN_ARROW, RIGHT_ARROW, None],
    [None, DOWN_ARROW, None, None],
    BOTTOM_LAYER,
]

KEYMAP_03 = [
    TOP_LAYER,
    [None,               None,             None,                 BRIGHTNESS_PLUS],
    [None,               UP_ARROW ,     None,                 BRIGHTNESS_MINUS],
    [LEFT_ARROW, None,                  RIGHT_ARROW,  None],
    [None,               DOWN_ARROW,    None,                 [COMMAND, L]],
    BOTTOM_LAYER,
]

# The number of keys in this list should match the number of color maps exactly
# So each layer has a mapping for both LEDs and key presses, you can reuse layers if you want like:
# `LAYER_KEYMAPS = [ KEYMAP_01, KEYMAP_01, KEYMAP_01]
LAYER_KEYMAPS = [ KEYMAP_00, KEYMAP_01, KEYMAP_00] # , KEYMAP_00, KEYMAP_00 ]

COLORMAP_00 = [
    [GREEN, GREEN,   GREEN, GREEN],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [AQUA,  FUSHIA,    AQUA,  AQUA],
    [AQUA,  AQUA,    AQUA,  OFF],
    [AQUA,  AQUA,    FUSHIA,  OFF],
    [GREEN, FUSHIA,  AQUA,  GREEN],
]


COLORMAP_01 = [
    [GREEN, GREEN,   GREEN, GREEN],
    [PURPLE,  LIME,    OFF,  PURPLE],
    [DARK_ORANGE,  OFF,    OFF,  TURQUOISE],
    [OFF,  PURPLE,    WHITE,  AQUA],
    [ORANGE,    MIDNIGHT_BLUE,  OFF, RED],
    [GREEN, FUSHIA,  AQUA,  GREEN],
]

# COLORMAP_02 = [
#     [RED,    RED,    RED,    RED],
#     [YELLOW, YELLOW, YELLOW, YELLOW],
#     [YELLOW, WHITE,  YELLOW, YELLOW],
#     [WHITE,  YELLOW, WHITE,  YELLOW],
#     [YELLOW, WHITE,  YELLOW, YELLOW],
#     [GREEN,  FUSHIA, AQUA,   GREEN],
# ]


COLORMAP_02 = [
    [(255, 8, 0),   (255, 29, 0),   (255, 126, 0),   (255, 186, 0)],
    [(255, 222, 0), (178, 255, 0),  (137, 255, 0),   (72, 255, 0)],
    [(30, 255, 0),  (0, 255, 43),   (0, 255, 103),   (0, 255, 206)],
    [(0, 255, 220), (0, 156, 255),  (0, 157, 255),   (0, 85, 255)],
    [(0, 36, 255),  (85, 0, 255),   (157, 0, 255),   (230, 0, 255)],
    [(255, 0, 244), (255, 0, 162),  (255, 0, 146),   (255, 0, 37)],
]

COLORMAP_03 = [
    [(255, 14, 0),   (255, 45, 0),   (255, 98, 0),   (255, 169, 0)],
    [(255, 236, 0),  (170, 255, 0),  (143, 255, 0),  (62, 255, 0)],
    [(0, 255, 0),    (0, 255, 48),   (0, 255, 112),  (0, 255, 203)],
    [(0, 230, 255),  (0, 195, 255),  (0, 135, 255),  (0, 86, 255)],
    [(0, 22, 255),   (66, 0, 255),   (109, 0, 255),  (212, 0, 255)],
    [(255, 0, 222),  (255, 0, 217),  (255, 0, 129),  (255, 0, 53)],
]

COLORMAP_04 = [
    [(255, 0, 22),   (255, 21, 0),   (255, 100, 0),  (255, 205, 0)],
    [(255, 251, 0),  (224, 255, 0),  (123, 255, 0),  (36, 255, 0)],
    [(14, 255, 0),   (0, 255, 92),   (0, 255, 113),  (0, 255, 160)],
    [(0, 228, 255),  (0, 191, 255),  (0, 103, 255),  (0, 39, 255)],
    [(42, 0, 255),   (100, 0, 255),  (141, 0, 255),  (160, 0, 255)],
    [(255, 0, 243),  (255, 0, 174),  (255, 0, 102),  (255, 0, 76)],
]


# COLORMAP_03 = [
#     [YELLOW, YELLOW, YELLOW, YELLOW],
#     [FUSHIA, FUSHIA, FUSHIA, FUSHIA],
#     [FUSHIA, FUSHIA, FUSHIA, FUSHIA],
#     [FUSHIA, FUSHIA, FUSHIA, FUSHIA],
#     [FUSHIA, FUSHIA, FUSHIA, FUSHIA],
#     [GREEN,  FUSHIA, AQUA,   GREEN],
# ]

# You can define each layer as a map for each individual key or have an entire color for a layer
# like: `COLORMAP_01 = RED`
LAYER_COLORS = [ COLORMAP_00, COLORMAP_01, COLORMAP_02] #,, COLORMAP_03, COLORMAP_04 ]