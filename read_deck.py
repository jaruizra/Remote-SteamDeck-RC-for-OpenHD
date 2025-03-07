from inputs import devices

for device in devices.gamepads:
    print("Device Name:", device.name)
    # Try accessing an attribute named 'path' (if it exists)
    device_path = getattr(device, 'path', None)
    if device_path is not None:
        print("Device Path:", device_path)
    else:
        print("Device Path attribute not available.")
    print("Capabilities:", device.capabilities())
