from inputs import devices
from inputs import get_gamepad


for device in devices.gamepads:
    print("Device Name:", device.name)
    print("Available attributes and methods:", dir(device))

print("!")
while True:
    events = get_gamepad()  # This waits for events from any gamepad device
    print("!")
    for event in events:
        print(f"Type: {event.ev_type}, Code: {event.code}, State: {event.state}")
