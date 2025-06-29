#!/usr/bin/python3
"""
A network transmitter that reads controller state using the Joystick class
and sends it over UDP.

This script imports the `Joystick` class from `steamdeck_input_api.py` and uses
it to get the full state of the controller, which is then serialized to JSON
and broadcasted on the network.
"""

# librerias
import sys
import socket
import time
import struct
import os

# --- Assumes your main script is named steamdeck_input_api.py ---
try:
    from steamdeck_input_api import Joystick
except ImportError:
    print("Error: Could not import the Joystick class.")
    print("Please ensure 'steamdeck_input_api.py' is in the same directory.")
    sys.exit(1)

def check_root_permissions():
    """Exits the script if it's not run as root."""
    if os.geteuid() != 0:
        print("Error: This script must be run as root to create a virtual device.")
        print("Please use 'sudo python3 joystick_receiver.py'")
        sys.exit(1)

# --- Network Configuration ---
# The destination IP address for the UDP packets.
# Change this to the IP address of the receiving computer.UDP_IP = "100.121.21.44"
UDP_IP = "192.168.3.1"
UDP_PORT = 5005

# --- Performance Configuration ---
TRANSMIT_RATE_HZ = 100  # Increased rate for lower latency
TRANSMIT_DELAY_SEC = 1 / TRANSMIT_RATE_HZ

# --- Binary Protocol Definition ---
# !: Network byte order (standard)
# L: Sequence number (unsigned long, 4 bytes)
# h: 6 axes (short, 2 bytes each)
# B: 10 buttons (unsigned char, 1 byte each)
PACKET_FORMAT = "!LhhhhhhBBBBBBBBBB"

def init_udp_socket():
    # Create the UDP socket
    # ipv4 values of Ip and Datagram(udp) mode
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def gather_controller_data(joystick):
    """
    Gathers the 18 specific channels from the joystick object

    Args:
        joystick (Joystick): The initialized joystick object

    Returns:
        tuple: A tuple containing two lists (axes, buttons)
    """
    # Get data from the joystick properties
    js_state = joystick.joystick_state
    shoulder_state = joystick.shoulder_state
    face_buttons = joystick.face_buttons
    dpad = joystick.dpad_state

    # Collect the 6 analog axes in the correct order
    axes = [
        js_state.get("LX", 0),
        js_state.get("LY", 0),
        js_state.get("RX", 0),
        js_state.get("RY", 0),
        shoulder_state.get("L2", 0),
        shoulder_state.get("R2", 0)
    ]

    # Collect the 11 most important digital buttons
    buttons = [
        face_buttons.get("A", 0),
        face_buttons.get("B", 0),
        face_buttons.get("X", 0),
        face_buttons.get("Y", 0),
        shoulder_state.get("L1", 0),
        shoulder_state.get("R1", 0),
        dpad.get("Up", 0),
        dpad.get("Down", 0),
        dpad.get("Left", 0),
        dpad.get("Right", 0),
    ]

    return axes, buttons

def pack_and_send_data(sock, seq_num, axes, buttons):
    """
    Packs the collected data into a binary message and sends it via UDP.

    Args:
        sock (socket): The UDP socket object.
        seq_num (int): The current packet sequence number.
        axes (list): The list of 6 axis values.
        buttons (list): The list of 1 button values.
    """
    try:
        # Pack the data into a binary message according to the defined format.
        # The '*' operator unpacks the lists into individual arguments.
        message = struct.pack(PACKET_FORMAT, seq_num, *axes, *buttons)
        
        # Send the data over the network.
        sock.sendto(message, (UDP_IP, UDP_PORT))

    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    """
    Main execution function. Initializes the joystick and the network socket,
    then enters a loop to read and transmit data.
    """
    check_root_permissions()
    # Create the udp socket
    sock = init_udp_socket()
    # Initialize variables
    joystick = None
    sequence_number = 0

    try:
        # 1. Create an instance of the Joystick class.
        # This handles all the SDL initialization and setup.
        joystick = Joystick()
        print(f"Transmitting joystick data to {UDP_IP}:{UDP_PORT}...")
        print("Press Ctrl+C to stop.")
        
        # 2. Start the main transmission loop.
        while True:
            # ALWAYS call .update() once per loop to poll for new events.
            joystick.update()

            # Get the specific channel to send
            axes, buttons = gather_controller_data(joystick)

            # Pack and send the data over the network.
            pack_and_send_data(sock, sequence_number, axes, buttons)

            # Increment sequence number for the next packet.
            # It wraps around automatically at the max value for an unsigned long
            sequence_number = (sequence_number + 1) % 4294967295

            # Wait a moment to maintain the desired transmission rate.
            time.sleep(TRANSMIT_DELAY_SEC)

    # Handle errors
    except (RuntimeError, KeyboardInterrupt) as e:
        # Handle errors from the Joystick class or a Ctrl+C press.
        print(f"\nShutting down transmitter... Reason: {e}")
    
    finally:
        # 4. Clean up all resources when the script exits.
        if joystick:
            joystick.close()
        sock.close()
        print("Socket closed.")

# Main program
if __name__ == "__main__":
    main()
