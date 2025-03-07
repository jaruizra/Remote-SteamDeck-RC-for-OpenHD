from inputs import devices

for device in devices.gamepads:
    print("Device Name:", device.name)
    print("Available attributes and methods:", dir(device))
