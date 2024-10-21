import serial
import time

# Adjust the serial port to the one your macropad is connected to
# On Linux or Mac, it might be something like '/dev/tty.usbmodemXYZ' or '/dev/ttyACM0'
# On Windows, it might be 'COM3' or similar
serial_port = '/dev/ttyACM0'
baud_rate = 115200  # Common for CircuitPython devices

# Open the serial connection
with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
    # Wait for the serial port to initialize
    time.sleep(2)

    # Send a message to the macropad
    message = "Hello from host!"
    ser.write(f"{message}\n".encode('utf-8'))

    # Optionally, wait for a response
    time.sleep(1)  # Wait for the macropad to process and respond
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print(f"Received from macropad: {response}")
