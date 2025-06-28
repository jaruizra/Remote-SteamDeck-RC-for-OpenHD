#!/usr/bin/python3
"""
A modular, class-based script for reading and processing joystick input on the STEAM DECK

This script defines a `Joystick` class that encapsulates SDL initialization,
event polling, and state management. It provides a clean API with specific
"getter" methods for different parts of the controller, making it highly
reusable for other developers.
"""

import sys
import os
import sdl2

# --- Configuration Constants ---
# Note: These are common values for a Steam Deck. Adjust for your controller.
JOYSTICK_INDEX = 0          # The joystick to use (0 is the first one found)
NUM_AXES_TO_TRACK = 6       # Number of axes to monitor (Steam Deck has 6)
NUM_BUTTONS_TO_TRACK = 19   # Number of buttons to monitor (Steam Deck has 17)

class Joystick:
    """A class to manage and read data from an SDL2 joystick."""

    def __init__(self, index=0, num_axes=6, num_buttons=17):
        """
        Initializes the Joystick, including SDL and the physical device.

        Args:
            index (int): The system index of the joystick to open (0 is the first).
            num_axes (int): The number of axes to track.
            num_buttons (int): The number of buttons to track.
        """
        self._joystick = None
        self._initialize_sdl()
        self._open_joystick(index)

        # Master state dictionaries that hold the real-time data
        self.axis_values = {i: 0 for i in range(num_axes)}
        self.button_values = {i: 0 for i in range(num_buttons)}

    def _initialize_sdl(self):
        """Initializes the SDL joystick subsystem."""
        if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
            raise RuntimeError(f"SDL Init Error: {sdl2.SDL_GetError().decode()}")

    def _open_joystick(self, index):
        """Opens the physical joystick device."""
        if sdl2.SDL_NumJoysticks() < 1:
            raise RuntimeError("No joystick found. Please connect a controller.")

        self._joystick = sdl2.SDL_JoystickOpen(index)
        if not self._joystick:
            raise RuntimeError(f"Failed to open joystick {index}: {sdl2.SDL_GetError().decode()}")

        sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)
        print(f"Opened: {sdl2.SDL_JoystickName(self._joystick).decode()}")

    def update(self):
        """
        This is the core polling method. It must be called once per frame.
        It processes all pending SDL events and updates the internal state.
        """
        event = sdl2.SDL_Event()
        # Process pending SDL events and stores them in event
        while sdl2.SDL_PollEvent(event) != 0:
            # joystick and triggers
            if event.type == sdl2.SDL_JOYAXISMOTION:
                if event.jaxis.axis in self.axis_values:
                    self.axis_values[event.jaxis.axis] = event.jaxis.value
            # D-pad and buttons
            elif event.type in (sdl2.SDL_JOYBUTTONDOWN, sdl2.SDL_JOYBUTTONUP):
                if event.jbutton.button in self.button_values:
                    self.button_values[event.jbutton.button] = event.jbutton.state
            # Check for Quit event
            elif event.type == sdl2.SDL_QUIT:
                # If the window is closed, we should exit gracefully.
                self.close()
                sys.exit(0)

    # --- Getter Methods for Developers ---

    def get_dpad_state(self):
        """
        Returns the state of the D-Pad, mapped from specific buttons.
        Note: Many controllers report the D-Pad as a 'hat', not buttons.
        This function uses the button numbers you requested.
        Order: Up (11), Down (12), Left (13), Right (14)
        """
        dpad_buttons = [11, 12, 13, 14]
        return {f"button_{b}": self.button_values.get(b, 0) for b in dpad_buttons}

    def get_face_button_state(self):
        """Returns the state of the four primary face buttons (A,B,X,Y)."""
        face_buttons = [0, 1, 2, 3]
        return {f"button_{b}": self.button_values.get(b, 0) for b in face_buttons}

    def get_shoulder_state(self):
        """
        Returns the state of shoulder triggers (axes) and bumpers (buttons).
        Uses the specific axes and buttons you requested.
        """
        return {
            "L2_trigger_axis_4": self.axis_values.get(4, 0),
            "R2_trigger_axis_5": self.axis_values.get(5, 0),
            "bumper_button_9": self.button_values.get(9, 0), # Note: Often L1/R1 are 4/5
            "bumper_button_10": self.button_values.get(10, 0)
        }

    def get_joystick_movement_state(self):
        """Returns the state of the left and right joystick axes."""
        joy_axes = [0, 1, 2, 3] # LX, LY, RX, RY
        return {f"axis_{a}": self.axis_values.get(a, 0) for a in joy_axes}

    def get_joystick_full_state(self):
        """
        Returns the joystick axes plus their click-buttons.
        Uses the specific buttons you requested.
        """
        state = self.get_joystick_movement_state()
        # Note:L3/R3 (stick clicks) are buttons 9/10
        state["L3"] = self.button_values.get(7, 0)
        state["R3"] = self.button_values.get(8, 0)
        return state

    def get_back_button_state(self):
        """Returns the state of the back grip buttons."""
        back_buttons = [16, 17, 18, 19]
        return {f"button_{b}": self.button_values.get(b, 0) for b in back_buttons}

    def get_full_state(self):
        """Returns a copy of all tracked button and axis states."""
        return {
            "axes": self.axis_values.copy(),
            "buttons": self.button_values.copy()
        }

    def close(self):
        """Closes the joystick and quits SDL."""
        if self._joystick:
            sdl2.SDL_JoystickClose(self._joystick)
            self._joystick = None
        sdl2.SDL_Quit()
        print("Joystick closed and SDL resources released.")


def display_developer_dashboard(joystick):
    """A dashboard demonstrating how to use the getter methods."""
    # This function now takes the whole joystick object
    # and calls its methods to get the data it needs.

    # --- Prepare data for display by calling the new methods ---
    dpad = joystick.get_dpad_state()
    face = joystick.get_face_button_state()
    shoulders = joystick.get_shoulder_state()
    joysticks = joystick.get_joystick_full_state()

    # --- Display Logic ---
    num_lines = 10 + len(dpad) + len(face) + len(shoulders) + len(joysticks)
    # Move cursor up to overwrite (flicker-free update)
    print(f'\x1b[{num_lines}A', end='')

    print("--- DEVELOPER JOYSTICK DASHBOARD ---")
    print("\x1b[2K--- D-Pad State ---")
    for name, value in dpad.items(): print(f"\x1b[2K{name}: {value}")

    print("\x1b[2K--- Face Button State ---")
    for name, value in face.items(): print(f"\x1b[2K{name}: {value}")

    print("\x1b[2K--- Shoulder State ---")
    for name, value in shoulders.items(): print(f"\x1b[2K{name}: {value}")

    print("\x1b[2K--- Joystick Full State ---")
    for name, value in joysticks.items(): print(f"\x1b[2K{name}: {value}")


def main():
    """Main execution function."""
    joystick = None
    try:
        # Create an instance of our new Joystick class
        joystick = Joystick(
            index=JOYSTICK_INDEX,
            num_axes=NUM_AXES_TO_TRACK,
            num_buttons=NUM_BUTTONS_TO_TRACK
        )

        # Print the initial layout once to prevent cursor errors
        display_developer_dashboard(joystick)

        # Main application loop
        while True:
            # 1. Update the joystick state by polling events
            joystick.update()

            # 2. Display the data using our modular functions
            display_developer_dashboard(joystick)

            # 3. Wait a moment
            sdl2.SDL_Delay(16)

    except (RuntimeError, KeyboardInterrupt) as e:
        print(f"\nERROR: {e}", file=sys.stderr)
    finally:
        if joystick:
            joystick.close()

if __name__ == "__main__":
    main()