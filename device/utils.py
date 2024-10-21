import microcontroller
import supervisor

def jump_to_bootloader():
    microcontroller.on_next_reset(microcontroller.RunMode.UF2)
    microcontroller.reset()

def reboot():
    supervisor.reload()