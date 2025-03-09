#!/usr/bin/python3
import uinput
import time

def create_virtual_joystick():
    """
    Create a virtual joystick with 4 axes and 4 buttons.
    Axes range: 0 to 32767
    """
    axis_capabilities = (
        uinput.ABS_X + (0, 32767, 0, 0),
        uinput.ABS_Y + (0, 32767, 0, 0),
        uinput.ABS_Z + (0, 32767, 0, 0),
        uinput.ABS_RZ + (0, 32767, 0, 0),
    )
    button_capabilities = (
        uinput.BTN_A,
        uinput.BTN_B,
        uinput.BTN_X,
        uinput.BTN_Y,
    )
    events = axis_capabilities + button_capabilities
    device = uinput.Device(events, name="Virtual Joystick")
    return device

def main():
    device = create_virtual_joystick()
    print("Virtual joystick created. Updating state every second...")

    # Initial states
    axes = [0, 0, 0, 0]  # For ABS_X, ABS_Y, ABS_Z, ABS_RZ
    buttons = [0, 0, 0, 0]  # For BTN_A, BTN_B, BTN_X, BTN_Y

    try:
        while True:
            # Increment each axis by 1, wrap around at 32767
            for i in range(4):
                axes[i] = (axes[i] + 1) % 32768

            # Toggle each button state (0 -> 1, 1 -> 0)
            for i in range(4):
                buttons[i] = 1 - buttons[i]

            # Emit axis events
            device.emit(uinput.ABS_X, axes[0], syn=False)
            device.emit(uinput.ABS_Y, axes[1], syn=False)
            device.emit(uinput.ABS_Z, axes[2], syn=False)
            device.emit(uinput.ABS_RZ, axes[3], syn=False)

            # Emit button events
            device.emit(uinput.BTN_A, buttons[0], syn=False)
            device.emit(uinput.BTN_B, buttons[1], syn=False)
            device.emit(uinput.BTN_X, buttons[2], syn=False)
            device.emit(uinput.BTN_Y, buttons[3], syn=False)

            # Synchronize events
            device.syn()

            # Wait for 1 second
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting virtual joystick creator...")

if __name__ == "__main__":
    main()