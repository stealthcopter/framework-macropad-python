"""
Responsible for detecting the key presses on the macropad
"""
import board
import digitalio
import analogio

MATRIX_COLS = 8
MATRIX_ROWS = 4

ADC_THRESHOLD = 1
DEBUG = False

MATRIX = [
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 3), (1, 4)],
    [(0, 5), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 1), (3, 3)],
    [(3, 5), (0, 0), (1, 0), None, (3, 0), (3, 2), (3, 4), (1, 5)],
    [None, None, None, None, (2, 0), None, None, None],
]

class MacropadKeys:

    def __init__(self):
        # Set unused pins to input to avoid interfering. They're hooked up to rows 5 and 6
        gp6 = digitalio.DigitalInOut(board.GP6)
        gp6.direction = digitalio.Direction.INPUT
        gp7 = digitalio.DigitalInOut(board.GP7)
        gp7.direction = digitalio.Direction.INPUT

        # Set up analog MUX pins
        mux_enable = digitalio.DigitalInOut(board.MUX_ENABLE)
        mux_enable.direction = digitalio.Direction.OUTPUT
        mux_enable.value = False  # Low to enable it
        self.mux_a = digitalio.DigitalInOut(board.MUX_A)
        self.mux_a.direction = digitalio.Direction.OUTPUT
        self.mux_b = digitalio.DigitalInOut(board.MUX_B)
        self.mux_b.direction = digitalio.Direction.OUTPUT
        self.mux_c = digitalio.DigitalInOut(board.MUX_C)
        self.mux_c.direction = digitalio.Direction.OUTPUT

        # Set up KSO pins
        self.kso_pins = [
            digitalio.DigitalInOut(x)
            for x in [
                # KSO0 - KSO7 for Keyboards and Numpad
                board.KSO0,
                board.KSO1,
                board.KSO2,
                board.KSO3,
                board.KSO4,
                board.KSO5,
                board.KSO6,
                board.KSO7,
                # KSO8 - KSO15 for Keyboards only
                board.KSO8,
                board.KSO9,
                board.KSO10,
                board.KSO11,
                board.KSO12,
                board.KSO13,
                board.KSO14,
                board.KSO15,
            ]
        ]
        for kso in self.kso_pins:
            kso.direction = digitalio.Direction.OUTPUT

        # Set up ADC input for reading button presses
        self.adc_in = analogio.AnalogIn(board.GP28)

        # Signal boot done (this may be unnecessary depending on your setup)
        boot_done = digitalio.DigitalInOut(board.BOOT_DONE)
        boot_done.direction = digitalio.Direction.OUTPUT
        boot_done.value = False

        # Main loop for detecting key presses
        self.prev_matrix_pos = None
        self.debounce = 0


    def mux_select_row(self, row):
        if row == 0:
            index = 2
        elif row == 1:
            index = 0
        elif row == 2:
            index = 1
        else:
            index = row

        self.mux_a.value = index & 0x01
        self.mux_b.value = index & 0x02
        self.mux_c.value = index & 0x04

    def drive_col(self, col, value):
        self.kso_pins[col].value = value

    def to_voltage(self, adc_sample):
        return (adc_sample * 3.3) / 65536

    def matrix_scan(self):
        matrix_pos = None
        for col in range(MATRIX_COLS):
            self.drive_col(col, True)

        for col in range(MATRIX_COLS):
            self.drive_col(col, False)

            for row in range(MATRIX_ROWS):

                self.mux_select_row(row)

                voltage = self.to_voltage(self.adc_in.value)

                if DEBUG:
                    print(f"{col}:{row}: {voltage}V")

                if voltage < ADC_THRESHOLD:
                    if DEBUG:
                        print(f"Pressed {col}:{row} {voltage}V")

                    matrix_pos = (col, row)

                    # Handle debounce or stop multiple key presses
                    if matrix_pos:
                        break

            self.drive_col(col, True)
        if DEBUG:
            print()
        return matrix_pos


    def detect_keypress(self, onkeypress=None):
        matrix_pos = self.matrix_scan()

        if not matrix_pos:
            self.debounce = 0
        if matrix_pos and matrix_pos == self.prev_matrix_pos:
            self.debounce += 1

        if matrix_pos and (matrix_pos != self.prev_matrix_pos or self.debounce > 10 or self.debounce == 0):
            self.debounce = 0
            (col, row) = matrix_pos
            if MATRIX[row][col] is not None:
                (x, y) = MATRIX[row][col]
                if onkeypress:
                    onkeypress(x,y)

        self.prev_matrix_pos = matrix_pos
