import usb_cdc

class Comms:
    def __init__(self):
        # Enable both REPL and Data serial
        #usb_cdc.enable(console=True, data=True)
        print(usb_cdc.data)
        self.serial = usb_cdc.data

    def send_to_host(self, message: str):
        """Send a message to the host."""
        if self.serial and self.serial.connected:
            self.serial.write(f"{message}\n".encode('utf-8'))

    def receive_from_host(self) -> str:
        """Receive a message from the host, if available."""
        if self.serial and self.serial.in_waiting > 0:
            return self.serial.readline().decode('utf-8').strip()
        return None