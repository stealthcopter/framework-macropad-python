
**Disclaimer**: I think these instructions should be accurate enough to follow along, but I may have missed things? good luck!


# Install prerequisites

```bash
sudo apt install python3-pip build-essential git git-lfs gettext cmake gcc-arm-none-eabi python3-venv
```

# Clone repo and init

```bash
git clone https://github.com/adafruit/circuitpython.git
cd circuitpython

# Check out the specific commit from the PR
git checkout 029c7a0caa075550fc5618b7c71075fb13937a13

# Create virtual env so we dont mess up our system
python3 -m venv .venv
source .venv/bin/activate

# Install deps
pip3 install --upgrade -r requirements-dev.txt
pip3 install --upgrade -r requirements-doc.txt

# Fetch submodules
cd ports/raspberrypi
make fetch-port-submodules

# Build mpy (for cross compiling) - only need to do this once 
cd ../..
make fetch-tags
make -C mpy-cross
```

# Build the actual firmware for your device

Now you're ready to build the firmware, but first we need to make a quick modification to `circuitpython/ports/raspberrypi/boards/framework_inputmodule/pins.c` as it's missing from the PR for some reason. I had to reverse engineer the pins from the QMK firmware source code, so I hope I've got them right:

```c
#include "shared-bindings/board/__init__.h"

STATIC const mp_rom_map_elem_t board_module_globals_table[] = {
    CIRCUITPYTHON_BOARD_DICT_STANDARD_ITEMS

    // SLEEP#
    { MP_ROM_QSTR(MP_QSTR_GP0), MP_ROM_PTR(&pin_GPIO0) },   // From original pins.c file (known)

    // INTB (ADC input pin from matrix.c)
    { MP_ROM_QSTR(MP_QSTR_GP28), MP_ROM_PTR(&pin_GPIO28) }, // From matrix.c (defined as ADC_CH2_PIN)

    // SDB
    { MP_ROM_QSTR(MP_QSTR_GP29), MP_ROM_PTR(&pin_GPIO29) }, // From original pins.c file (known)

    // PWM for backlight control
    { MP_ROM_QSTR(MP_QSTR_GP25), MP_ROM_PTR(&pin_GPIO25) }, // From info.json and config.h (backlight control)

    // Capslock
    { MP_ROM_QSTR(MP_QSTR_GP24), MP_ROM_PTR(&pin_GPIO24) }, // From original pins.c file (known)

    // LED Controller I2C
    { MP_ROM_QSTR(MP_QSTR_SDA), MP_ROM_PTR(&pin_GPIO26) },  // From original pins.c file (I2C SDA)
    { MP_ROM_QSTR(MP_QSTR_SCL), MP_ROM_PTR(&pin_GPIO27) },  // From original pins.c file (I2C SCL)
    { MP_ROM_QSTR(MP_QSTR_I2C), MP_ROM_PTR(&board_i2c_obj) },  // From original pins.c file (I2C)

    // Add GP6 and GP7
    { MP_ROM_QSTR(MP_QSTR_GP6), MP_ROM_PTR(&pin_GPIO6) },   // From your CircuitPython script and matrix.c (unused row pins)
    { MP_ROM_QSTR(MP_QSTR_GP7), MP_ROM_PTR(&pin_GPIO7) },   // From your CircuitPython script and matrix.c (unused row pins)

    // KSO Pins (Key Scan Output) - from matrix.c (KSO0 to KSO15 are defined in matrix.c)
    { MP_ROM_QSTR(MP_QSTR_KSO0), MP_ROM_PTR(&pin_GPIO8) },  // From matrix.c (KSO0)
    { MP_ROM_QSTR(MP_QSTR_KSO1), MP_ROM_PTR(&pin_GPIO9) },  // From matrix.c (KSO1)
    { MP_ROM_QSTR(MP_QSTR_KSO2), MP_ROM_PTR(&pin_GPIO10) }, // From matrix.c (KSO2)
    { MP_ROM_QSTR(MP_QSTR_KSO3), MP_ROM_PTR(&pin_GPIO11) }, // From matrix.c (KSO3)
    { MP_ROM_QSTR(MP_QSTR_KSO4), MP_ROM_PTR(&pin_GPIO12) }, // From matrix.c (KSO4)
    { MP_ROM_QSTR(MP_QSTR_KSO5), MP_ROM_PTR(&pin_GPIO13) }, // From matrix.c (KSO5)
    { MP_ROM_QSTR(MP_QSTR_KSO6), MP_ROM_PTR(&pin_GPIO14) }, // From matrix.c (KSO6)
    { MP_ROM_QSTR(MP_QSTR_KSO7), MP_ROM_PTR(&pin_GPIO15) }, // From matrix.c (KSO7)

    // Additional KSO pins (from matrix.c)
    { MP_ROM_QSTR(MP_QSTR_KSO8), MP_ROM_PTR(&pin_GPIO21) }, // From matrix.c (KSO8)
    { MP_ROM_QSTR(MP_QSTR_KSO9), MP_ROM_PTR(&pin_GPIO20) }, // From matrix.c (KSO9)
    { MP_ROM_QSTR(MP_QSTR_KSO10), MP_ROM_PTR(&pin_GPIO19) }, // From matrix.c (KSO10)
    { MP_ROM_QSTR(MP_QSTR_KSO11), MP_ROM_PTR(&pin_GPIO18) }, // From matrix.c (KSO11)
    { MP_ROM_QSTR(MP_QSTR_KSO12), MP_ROM_PTR(&pin_GPIO17) }, // From matrix.c (KSO12)
    { MP_ROM_QSTR(MP_QSTR_KSO13), MP_ROM_PTR(&pin_GPIO16) }, // From matrix.c (KSO13)
    { MP_ROM_QSTR(MP_QSTR_KSO14), MP_ROM_PTR(&pin_GPIO23) }, // From matrix.c (KSO14)
    { MP_ROM_QSTR(MP_QSTR_KSO15), MP_ROM_PTR(&pin_GPIO22) }, // From matrix.c (KSO15)

    // MUX pins (Multiplexer control) - defined in framework.h and matrix.c
    { MP_ROM_QSTR(MP_QSTR_MUX_ENABLE), MP_ROM_PTR(&pin_GPIO4) }, // From framework.h and matrix.c (MUX_ENABLE = GP4)
    { MP_ROM_QSTR(MP_QSTR_MUX_A), MP_ROM_PTR(&pin_GPIO1) },      // From matrix.c (MUX_A = GP1)
    { MP_ROM_QSTR(MP_QSTR_MUX_B), MP_ROM_PTR(&pin_GPIO2) },      // From matrix.c (MUX_B = GP2)
    { MP_ROM_QSTR(MP_QSTR_MUX_C), MP_ROM_PTR(&pin_GPIO3) },      // From matrix.c (MUX_C = GP3)

    { MP_ROM_QSTR(MP_QSTR_BOOT_DONE), MP_ROM_PTR(&pin_GPIO5) }, // From framework.h (BOOT_DONE_GPIO GP5)

    // FIXME: Double-check other hardware mappings or schematic
};
MP_DEFINE_CONST_DICT(board_module_globals, board_module_globals_table);
```

Now you can actually build the firmware:

```bash
cd ports/raspberrypi
make BOARD=framework_inputmodule
```



