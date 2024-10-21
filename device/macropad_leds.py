"""
This class is responsible for illuminating the macropad LEDs
"""
import time

import board
import busio
import digitalio
from framework_is31fl3743 import IS31FL3743
from config import DELAY_ANIMATION, BRIGHTNESS_DEFAULT, BRIGHTNESS_STEP

import colors

class MacropadLEDs:

    # LED mapping (physical LED positions)
    MATRIX_LED_MAP = [
        [40, 37, 52, 49],
        [ 4,  1, 16, 13],
        [22, 19, 34, 31],
        [58, 55, 70, 67],
        [25, 61, 64, 28],
        [ 7, 43, 46, 10],
    ]

    def __init__(self):
        # Enable LED controller via SDB pin
        self.sdb = digitalio.DigitalInOut(board.GP29)
        self.sdb.direction = digitalio.Direction.OUTPUT
        self.sdb.value = True

        self.i2c = busio.I2C(board.SCL, board.SDA)  # Or board.I2C()

        # Scan the I2C bus and unlock it
        self.i2c.try_lock()
        self.i2c.scan()
        self.i2c.unlock()

        self.is31 = IS31FL3743(self.i2c, address=0x20)
        self.brightness = BRIGHTNESS_DEFAULT
        self.is31.set_led_scaling(self.brightness)  # Full brightness
        self.is31.global_current = 0xFF  # Set current to max
        self.is31.enable = True
        self.previous_sleep_state = True

        # SLEEP# pin. Low if the host is sleeping
        self.sleep_pin = digitalio.DigitalInOut(board.GP0)
        self.sleep_pin.direction = digitalio.Direction.INPUT

    def brightness_plus(self):
        self.brightness = min(self.brightness + BRIGHTNESS_STEP, 0xFF)
        self.is31.set_led_scaling(self.brightness)
        print(self.brightness)

    def brightness_minus(self):
        self.brightness = max(self.brightness - BRIGHTNESS_STEP, 0)
        self.is31.set_led_scaling(self.brightness)
        print(self.brightness)

    def set_led_color(self, col, row, color):
        led_index = self.MATRIX_LED_MAP[row][col]
        self.is31[led_index] = color[2]
        self.is31[led_index+1] = color[1]
        self.is31[led_index+2] = color[0]

    def set_led_flash(self, col, row, color, repeats=5):
        for _ in range(repeats):
            self.set_led_color(col, row, colors.OFF)
            time.sleep(DELAY_ANIMATION * 2)
            self.set_led_color(col, row, color)
            time.sleep(DELAY_ANIMATION * 2)

    def fill(self, color):
        for row in range(0, len(self.MATRIX_LED_MAP)):
            for col in range(0, len(self.MATRIX_LED_MAP[0])):
                if isinstance(color, tuple):
                    self.set_led_color(col, row, color)
                else:
                    self.set_led_color(col, row, color[row][col])

    def fill_from_left(self, color):
        for col in range(0, len(self.MATRIX_LED_MAP[0])):
            for row in range(0, len(self.MATRIX_LED_MAP)):
                if isinstance(color, tuple):
                    self.set_led_color(col, row, color)
                else:
                    self.set_led_color(col, row, color[row][col])
            time.sleep(DELAY_ANIMATION)

    def fill_from_right(self, color):
        for col in reversed(range(0, len(self.MATRIX_LED_MAP[0]))):
            for row in range(0, len(self.MATRIX_LED_MAP)):
                if isinstance(color, tuple):
                    self.set_led_color(col, row, color)
                else:
                    self.set_led_color(col, row, color[row][col])
            time.sleep(DELAY_ANIMATION)

    def fill_from_bottom(self, color):
        for row in reversed(range(0, len(self.MATRIX_LED_MAP))):
            for col in range(0, len(self.MATRIX_LED_MAP[0])):
                if isinstance(color, tuple):
                    self.set_led_color(col, row, color)
                else:
                    self.set_led_color(col, row, color[row][col])
            time.sleep(DELAY_ANIMATION)

    def fill_from_top(self, color):
        for row in range(0, len(self.MATRIX_LED_MAP)):
            for col in range(0, len(self.MATRIX_LED_MAP[0])):
                if isinstance(color, tuple):
                    self.set_led_color(col, row, color)
                else:
                    self.set_led_color(col, row, color[row][col])
            time.sleep(DELAY_ANIMATION)

    def is_awake(self, on_wake, on_sleep):
        # Get the current state of the sleep pin
        current_state = self.sleep_pin.value
        self.is31.enable = current_state

        # Check for wake-up event (transition from sleep to awake)
        if not self.previous_sleep_state and current_state:
            print("Waking up")
            if on_wake:
                on_wake()

        # Check for sleep event (transition from awake to sleep)
        if self.previous_sleep_state and not current_state:
            print("Going to sleep")
            if on_sleep:
                on_sleep()

        # Update the previous state
        self.previous_sleep_state = current_state

        return current_state

