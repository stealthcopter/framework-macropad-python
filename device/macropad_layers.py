"""
Responsible for:
- Converting key presses to keyboard input events
- Switching between layers of colors and key events
"""
from adafruit_hid.keyboard import Keyboard
from keycode import *

import usb_hid
import colors
import config
from utils import reboot, jump_to_bootloader

ANIM_FROM_LEFT   = 0
ANIM_FROM_RIGHT  = 1
ANIM_FROM_TOP    = 2
ANIM_FROM_BOTTOM = 3

LAYER_COUNT = len(config.LAYER_KEYMAPS)

if len(config.LAYER_COLORS) != len(config.LAYER_KEYMAPS):
    raise ValueError("Layer colors and keymaps must have the same length")

class MacropadLayer:

    def __init__(self, macropad_leds):
        self.macropad_leds = macropad_leds
        self.keyboard = Keyboard(usb_hid.devices)

        self.current_layer = 0
        self.reboot_counter = 0
        self.bootloader_counter = 0

        self.macropad_leds.fill(colors.OFF)
        self.change_layer(ANIM_FROM_BOTTOM)

    def on_keypress(self, x, y):
        code = config.LAYER_KEYMAPS[self.current_layer][y][x]
        if code:
            print(f"Pressed {code} ({x}, {y})")

            if code != DEVICE_REBOOT:
                self.reboot_counter = 0
            if code != DEVICE_BOOTLOADER:
                self.bootloader_counter = 0

            if isinstance(code, list):
                # Multi-key presses
                self.keyboard.press(*code)
                self.keyboard.release_all()
            elif code < 1000:
                # Single key presses
                self.keyboard.press(code)
                self.keyboard.release_all()
            else:
                # Special key presses
                self.macropad_event(code, x, y)

    def macropad_event(self, code, x, y):
        if code == LAYER_PREV:
            self.layer_prev()

        elif code == LAYER_NEXT:
            self.layer_next()

        elif code == BRIGHTNESS_PLUS:
            self.macropad_leds.brightness_plus()
        elif code == BRIGHTNESS_MINUS:
            self.macropad_leds.brightness_minus()

        elif code == DEVICE_BOOTLOADER:
            self.bootloader_counter += 1
            if self.bootloader_counter == 3:
                self.macropad_leds.set_led_flash(x, y, config.LAYER_COLORS[self.current_layer][y][x], colors.RED)
            elif self.bootloader_counter >= 4:
                jump_to_bootloader()

        elif code == DEVICE_REBOOT:
            self.reboot_counter += 1
            if self.reboot_counter == 3:
                self.macropad_leds.set_led_flash(x, y, config.LAYER_COLORS[self.current_layer][y][x], colors.RED)
            elif self.reboot_counter >= 4:
                reboot()

    def layer_next(self):
        self.current_layer = (self.current_layer + 1) % LAYER_COUNT
        self.change_layer(ANIM_FROM_RIGHT)

    def layer_prev(self):
        self.current_layer = (self.current_layer - 1) % LAYER_COUNT
        self.change_layer(ANIM_FROM_LEFT)

    def change_layer(self, anim=None):
        print(f'layer {self.current_layer}')

        color_layer = config.LAYER_COLORS[self.current_layer]

        if anim == ANIM_FROM_RIGHT:
            self.macropad_leds.fill_from_right(color_layer)
        elif anim == ANIM_FROM_LEFT:
            self.macropad_leds.fill_from_left(color_layer)
        elif anim == ANIM_FROM_TOP:
            self.macropad_leds.fill_from_top(color_layer)
        else:
            self.macropad_leds.fill_from_bottom(color_layer)

    def on_wake(self):
        self.change_layer(ANIM_FROM_BOTTOM)

    def on_sleep(self):
        self.macropad_leds.fill_from_bottom(colors.OFF)




