TODO: Make this better

tl;dr:
1. Boot into bootloader
2. Copy firmware over
3. Python fun times.

# Boot your device into the bootloader

## 1. Reboot and Press keys

- Reboot the device
- Press keys 2 and 6 repeatedly
- It will then boot into the bootloader

Note you can reboot the device in a few ways, physically removing it is one option. Altho, that's kind of annoying, another sneaky way is to use the configurator at `keyboard.frame.work` and add a reboot button to the keyboard and then press it, magic.

## 2. Using the REPL

If you have a serial USB connection to the REPL already you can easily trigger a reboot into the bootloader

```python
import microcontroller
microcontroller.on_next_reset(microcontroller.RunMode.UF2)
microcontroller.reset()
```

Not so useful if this is your first time, but handy once circuit python is installed.

# Install Firmware

You should have a new USB device appear on your laptop, all you have to do is copy the `firmware.uf2` over to it, and it will install the firmware and reboot.

# Connecting to the REPL

Once it's installed another new USB device will appear, this is where we can start chucking Python onto the device that will run. You can also connect over a USB serial connection to get into an interactive REPL (Python interpreter) which is super handy for debugging.

```bash
screen /dev/ttyACM0 115200
```

Note if you do not have permissions, this will terminate immediate, check you have install the [udev rules](https://docs.qmk.fm/faq_build#linux-udev-rules).

Also, if you accidentally kill your screen session and cant seem to connect again, try `screen -list` to see what sessions are still running and `screen -r sessionname` to reconnect.
