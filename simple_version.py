#!/usr/bin/python3
"""
A script to read joystick input using SDL2, display a real-time dashboard
of its state in the terminal.
"""

# Standard library imports
import sys
import os

# Third-party imports
import sdl2

# --- Configuration Constants ---
JOYSTICK_INDEX = 0      # The joystick to use (0 is the first one found)
NUM_AXES = 6            # Number of axes to monitor (Steam Deck has 6)
NUM_BUTTONS = 19        # Number of buttons to monitor (Steam Deck has 17)
REFRESH_RATE_HZ = 60    # Target refresh rate for the display
REFRESH_DELAY_MS = 1000 // REFRESH_RATE_HZ # Calculate delay in milliseconds

# lectura y salida
REFRESH_RATE_MS = 16  # 60Hz frecuencia aprox

def init_joystick(joystick_index):
    """
    Initializes the SDL2 library and opens a specific joystick

    Args:
        joystick_index (int): The index of the joystick to open

    Returns:
        sdl2.SDL_Joystick: The opened joystick object

    Raises:
        SystemExit: If SDL fails to initialize or no joystick is found.
    """
    # Initiate a joystick subsystem
    if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
        # Error
        print("SDL Init error:", sdl2.SDL_GetError().decode())
        sys.exit(1)

    # Check error in the number of joystick connected
    if sdl2.SDL_NumJoysticks() < 1:
        # Error
        print("No joystick found.")
        sdl2.SDL_Quit()
        sys.exit(1)

    # I get the first joystick to use
    joystick = sdl2.SDL_JoystickOpen(joystick_index)

    # Check error to open the joystick
    if not joystick:
        # Error
        print("Failed to open joystick:", sdl2.SDL_GetError().decode())
        sdl2.SDL_Quit()
        sys.exit(1)
    
    print(f"Successfully opened joystick: {sdl2.SDL_JoystickName(joystick).decode()}")

    # I return the joystick I conencted to
    return joystick

def poll_joystick_events(axis_values, button_values):
    # Process pending SDL events and stores them in event
    event = sdl2.SDL_Event()

    while sdl2.SDL_PollEvent(event) != 0:

        # joystick and triggers
        if event.type == sdl2.SDL_JOYAXISMOTION:
            # Check if we are tracking this axis
            if event.jaxis.axis in axis_values:
                axis_values[event.jaxis.axis] = event.jaxis.value
            # Uncomment for debugging:
            #print(f"Axis {event.jaxis.axis} updated: {value}")

        # D-pad and buttons
        elif event.type in (sdl2.SDL_JOYBUTTONDOWN, sdl2.SDL_JOYBUTTONUP):
            if event.jbutton.button in button_values:
                button_values[event.jbutton.button] = event.jbutton.state
            # Uncomment for debugging:
            #print(f"Button {event.jbutton.button} state: {value}")

        # Check for Quit event
        elif event.type == sdl2.SDL_QUIT:
            # Quit with error
            sys.exit(0)

def display_dashboard(buttons, axes, is_first_run=False):
    """
    Render one frame of the joystick dashboard, overwriting the previous one
    """

    num_lines = 1 + 1 + 1 + len(buttons) + 1 + 1 + len(axes)
    if not is_first_run:
        # move to beginning of the first line of previous frame
        print(f'\033[{num_lines}F', end='', flush=True)

    print("--- SIMPLE JOYSTICK DASHBOARD --- (Press Ctrl+C to quit)")

    # Display Button States
    print('--- BUTTONS ---')
    for bid, val in buttons.items():
        # The :2 formats the number to take up 2 spaces for alignment
        print(f'Button {bid:2}: {"Pressed" if val else "Released"}')

    # Display Axis States
    print('\n--- AXES ---')
    for aid, val in axes.items():
        # The :6 formats the number to take up 6 spaces for alignment
        print(f'Axis   {aid:2}: {val:+6d}')

def main():
    """Main execution function."""
    
    # Initialize to None
    joystick = None

    try:
        # open a joystick
        joystick = init_joystick(JOYSTICK_INDEX)

        # Enable processing of joystick events with sdl event handling mechanism
        # this makes sdl2 to generate events -> for the event loop I created
        sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)

        # Dictionaries to hold state for axes and buttons
        axis_values = {i: 0 for i in range(NUM_BUTTONS)}
        button_values = {i: 0 for i in range(NUM_AXES)}

        # Print the initial layout once to prevent cursor errors
        display_dashboard(button_values, axis_values, is_first_run=True)

        # Main loop
        while True:
            # First, update the state from any new events
            poll_joystick_events(axis_values, button_values)

            # Now, display the complete, updated state
            display_dashboard(button_values, axis_values)

            # Wait a moment before the next refresh
            sdl2.SDL_Delay(REFRESH_DELAY_MS)
    
    # Handle graceful shutdown on Ctrl+C
    except KeyboardInterrupt:
        print("Exiting transmitter...")
    
    # This block ALWAYS runs, ensuring resources are released
    # even if an error occurs.
    finally:
        if joystick:
            # close sdl joystick
            sdl2.SDL_JoystickClose(joystick)
        # quit sdl2
        sdl2.SDL_Quit()

# Main program
if __name__ == "__main__":
    main()
