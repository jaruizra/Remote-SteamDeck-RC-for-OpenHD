from inputs import devices, get_gamepad

# List available gamepads/joysticks
for device in devices.gamepads:
    print("Device Name:", device.name)
    print("Capabilities:", device.capabilities())

# Read events in a loop
while True:
    events = get_gamepad()  # Waits until events are available
    for event in events:
        print(f"Type: {event.ev_type}, Code: {event.code}, State: {event.state}")
