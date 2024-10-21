import time

import supervisor

import config

from comms import Comms
from macropad_keys import MacropadKeys
from macropad_layers import MacropadLayer
from macropad_leds import MacropadLEDs

# Disable autoreload as my device kept resetting randomly, your milage may vary.
supervisor.runtime.autoreload = False

macropadLeds = MacropadLEDs()
macropadKeys = MacropadKeys()
macropadLayer = MacropadLayer(macropadLeds)

if config.ENABLE_HOST_COMMS:
    comms = Comms()

def loop():
    while True:
        # See if we are awake, otherwise take a nap for this cycle
        if not macropadLeds.is_awake(macropadLayer.on_wake, macropadLayer.on_sleep):
            time.sleep(config.DELAY_SLEEPING)
            continue

        # If we want host comms, lets go
        if config.ENABLE_HOST_COMMS and comms:
            pass

        # host_message = comms.receive_from_host()
        # if host_message:
        #     print(f"Received from host: {host_message}")
        #     macropadLeds.fill(random.choice(cycle))
        #     comms.send_to_host('ak')

        # Listen for key presses and send to our layer to respond
        macropadKeys.detect_keypress(macropadLayer.on_keypress)

        # This cycle is over, chill.
        time.sleep(config.DELAY)

loop()