from inputs import get_gamepad

while True:
    print("1")
    events = get_gamepad()  # Blocks until an event is available
    print("1")
    for event in events:
        print("1")
        print(f"Type: {event.ev_type}, Code: {event.code}, State: {event.state}")
