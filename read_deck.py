from inputs import get_gamepad

while True:
    events = get_gamepad()  # Blocks until an event is available
    for event in events:
        print(f"Type: {event.ev_type}, Code: {event.code}, State: {event.state}")
