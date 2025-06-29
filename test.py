#!/usr/bin/python3
"""
A test script to read from a virtual joystick and display its state.

This script is designed to be run alongside the transmitter and receiver.
It connects to the virtual joystick created by `joystick_receiver.py` and
uses the rich dashboard to confirm that inputs are being received correctly.
"""

import sys
import time
from rich.live import Live
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel

# --- Import the Joystick class from your API file ---
# This demonstrates the reusability of your class.
try:
    from steamdeck_input_api import Joystick
except ImportError:
    print("Error: Could not import the Joystick class.", file=sys.stderr)
    print("Please ensure 'steamdeck_input_api.py' is in the same directory.", file=sys.stderr)
    sys.exit(1)

# --- Configuration ---
# We want to connect to the VIRTUAL joystick. This is usually the second
# joystick on the system (index 1) if the physical one is index 0.
# You may need to change this if you have other controllers connected.
VIRTUAL_JOYSTICK_INDEX = 1
REFRESH_RATE_HZ = 60
REFRESH_DELAY_SEC = 1 / REFRESH_RATE_HZ

def generate_dashboard_layout(joystick):
    """
    Generates a rich layout object by accessing the joystick's properties.
    This function is identical to the one in the API script, showing how
    reusable components can be.
    """
    def create_table(data_dict, title):
        table = Table(title=title, expand=True, show_header=False, border_style="dim")
        table.add_column("Item", style="cyan", no_wrap=True)
        table.add_column("Value", justify="right")
        for item, value in data_dict.items():
            if isinstance(value, int) and value in (0, 1):
                state = "[bold green]Pressed[/]" if value else "[red]Off[/]"
                table.add_row(item, state)
            else:
                color = "green" if value > 1000 else "red" if value < -1000 else "white"
                table.add_row(item, f"[{color}]{value:+6d}[/]")
        return Panel(table, title=f"[bold cyan]{title}[/]", border_style="cyan")

    # --- Use the properties from the joystick object to create each panel ---
    face_button_panel = create_table(joystick.face_buttons, "Face Buttons")
    dpad_panel = create_table(joystick.dpad_state, "D-Pad")
    shoulder_panel = create_table(joystick.shoulder_state, "Shoulders")
    joystick_panel = create_table(joystick.joystick_state, "Joysticks")
    # Note: The simple receiver doesn't create back buttons, so we omit this.
    # back_button_panel = create_table(joystick.back_buttons, "Back Grips")
    
    left_column = Columns([face_button_panel, dpad_panel])
    
    return Columns([joystick_panel, left_column, shoulder_panel])

def main():
    """Main execution function to run the test dashboard."""
    joystick = None
    print("Attempting to connect to virtual joystick...")
    print(f"Make sure the receiver is running and the virtual joystick is at index {VIRTUAL_JOYSTICK_INDEX}.")

    try:
        # Create an instance of the Joystick class, telling it to open the VIRTUAL joystick.
        joystick = Joystick(index=VIRTUAL_JOYSTICK_INDEX)
        
        print("\nConnection successful! Displaying dashboard...")
        
        with Live(generate_dashboard_layout(joystick), screen=True, vertical_overflow="visible") as live:
            # The loop will exit when joystick.update() returns False (on a quit event)
            while joystick.update():
                live.update(generate_dashboard_layout(joystick))
                time.sleep(REFRESH_DELAY_SEC)

    except (RuntimeError, KeyboardInterrupt) as e:
        print(f"\nERROR: Could not connect or run dashboard. {e}", file=sys.stderr)
        print("Is the receiver script running with 'sudo'?", file=sys.stderr)
    finally:
        if joystick:
            joystick.close()

if __name__ == "__main__":
    main()
