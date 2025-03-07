from inputs import devices

for device in devices.gamepads:
    print("Device Name:", device.name)
    print("Device Path:", device.fn)
    print("Capabilities:", device.capabilities())

