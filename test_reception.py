#!/usr/bin/python3
import sdl2
import sdl2.ext
import time

def main():
    # Initialize SDL2 and joystick subsystem
    sdl2.ext.init()
    sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)

    # Get the number of joysticks
    num_joysticks = sdl2.SDL_NumJoysticks()
    print(f"Number of joysticks: {num_joysticks}")

    if num_joysticks == 0:
        print("No joysticks found.")
        return

    # List all joysticks
    for i in range(num_joysticks):
        name = sdl2.SDL_JoystickNameForIndex(i).decode('utf-8')
        print(f"Joystick {i}: {name}")

    # Find the virtual joystick by name
    virtual_joystick_index = None
    for i in range(num_joysticks):
        name = sdl2.SDL_JoystickNameForIndex(i).decode('utf-8')
        if name == "Virtual Joystick":
            virtual_joystick_index = i
            break

    if virtual_joystick_index is None:
        print("Virtual Joystick not found.")
        return

    # Open the virtual joystick
    joystick = sdl2.SDL_JoystickOpen(virtual_joystick_index)
    if not joystick:
        print("Failed to open virtual joystick.")
        return

    print("Connected to Virtual Joystick.")

    try:
        while True:
            
            # Update joystick state
            sdl2.SDL_PumpEvents()

            # Read axis states (4 axes)
            axes = [sdl2.SDL_JoystickGetAxis(joystick, i) for i in range(4)]

            # Read button states (4 buttons)
            buttons = [sdl2.SDL_JoystickGetButton(joystick, i) for i in range(4)]

            # Print the states
            print(f"Axes: {axes}, Buttons: {buttons}")

            # Wait for 1 second
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting joystick reader...")
    finally:
        sdl2.SDL_JoystickClose(joystick)
        sdl2.ext.quit()

if __name__ == "__main__":
    main()