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

try:
    from steamdeck_input_api import Joystick
except ImportError:
    print("Error: Could not import the Joystick class.", file=sys.stderr)
    print("Please ensure 'steamdeck_input_api.py' is in the same directory.", file=sys.stderr)
    sys.exit(1)

# --- Configuration ---
VIRTUAL_JOYSTICK_INDEX = 1
REFRESH_RATE_HZ = 60
REFRESH_DELAY_SEC = 1 / REFRESH_RATE_HZ

def generate_dashboard_layout(joystick):
    """
    Generates a rich layout object by interpreting the layout of the
    VIRTUAL joystick created by joystick_receiver.py.
    """
    def scale_trigger(value):
        """Scales a joystick axis from -32768..32767 to 100..0 (reversed)."""
        # Clamp the value to the expected range
        value = max(-32768, min(value, 32767))
        # Apply reversed linear scaling
        return int(((32767 - value) / 65535) * 100)

    def create_table(data_dict, title):
        table = Table(title=title, expand=True, show_header=False, border_style="dim")
        table.add_column("Item", style="cyan", no_wrap=True)
        table.add_column("Value", justify="right")
        for item, value in data_dict.items():
            # Special display for scaled triggers
            if "L2" in item or "R2" in item:
                table.add_row(item, f"[yellow]{value:3d}%[/]")
            # Standard display for buttons
            elif isinstance(value, int) and value in (0, 1):
                state = "[bold green]Pressed[/]" if value else "[red]Off[/]"
                table.add_row(item, state)
            # Standard display for joystick axes
            else:
                color = "green" if value > 1000 else "red" if value < -1000 else "white"
                table.add_row(item, f"[{color}]{value:+6d}[/]")
        return Panel(table, title=f"[bold cyan]{title}[/]", border_style="cyan")

    # --- Manually create dictionaries with transformations ---

    # Joysticks (LX, LY, RX, RY) with inversions
    virtual_joystick_state = {
        "LX": joystick.axis_values.get(0, 0),
        "LY": -joystick.axis_values.get(1, 0),  # Invert LY
        "RX": -joystick.axis_values.get(4, 0),  # Invert RX
        "RY": joystick.axis_values.get(3, 0),
    }

    # Face Buttons (A, B, X, Y)
    virtual_face_buttons = {
        "A (South)": joystick.button_values.get(0, 0),
        "B (East)":  joystick.button_values.get(1, 0),
        "X (West)":  joystick.button_values.get(3, 0),
        "Y (North)": joystick.button_values.get(2, 0),
    }

    # Shoulder Buttons (L1/R1) and Triggers (L2/R2) with scaling
    virtual_shoulder_state = {
        "L1 (TL)": joystick.button_values.get(4, 0),
        "R1 (TR)": joystick.button_values.get(5, 0),
        "L2 (Z)":  scale_trigger(joystick.axis_values.get(2, 0)),
        "R2 (RZ)": scale_trigger(joystick.axis_values.get(5, 0)),
    }

    # The virtual D-Pad is a HAT switch, which SDL reads as axes (6 and 7).
    hat_x = joystick.axis_values.get(6, 0)
    hat_y = joystick.axis_values.get(7, 0)
    virtual_dpad_state = {
        "Up": 1 if hat_y < 0 else 0,
        "Down": 1 if hat_y > 0 else 0,
        "Left": 1 if hat_x < 0 else 0,
        "Right": 1 if hat_x > 0 else 0,
    }

    # --- Create panels using our new dictionaries ---
    joystick_panel = create_table(virtual_joystick_state, "Joysticks")
    face_button_panel = create_table(virtual_face_buttons, "Face Buttons")
    dpad_panel = create_table(virtual_dpad_state, "D-Pad")
    shoulder_panel = create_table(virtual_shoulder_state, "Shoulders")
    
    left_column = Columns([face_button_panel, dpad_panel])
    
    return Columns([joystick_panel, left_column, shoulder_panel])

def main():
    """Main execution function to run the test dashboard."""
    joystick = None
    print("Attempting to connect to virtual joystick...")
    print(f"Make sure the receiver is running and the virtual joystick is at index {VIRTUAL_JOYSTICK_INDEX}.")

    try:
        joystick = Joystick(index=VIRTUAL_JOYSTICK_INDEX, num_axes=8, num_buttons=10)
        
        print("\nConnection successful! Displaying dashboard...")
        
        with Live(generate_dashboard_layout(joystick), screen=True, vertical_overflow="visible") as live:
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
