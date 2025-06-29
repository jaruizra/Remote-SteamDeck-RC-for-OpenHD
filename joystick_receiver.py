#!/usr/bin/python3
"""
A network receiver that listens for joystick data over UDP and creates a
virtual joystick on the local machine using the 'uinput' library.

This script must be run with root privileges (sudo python3 receiver.py')
to have permission to create a virtual input device.
"""

import sys
import os
import socket
import time
import struct

try:
    import uinput
except ImportError:
    print("Error: The 'python-uinput' library is required.")
    print("Please install it using: pip install python-uinput")
    sys.exit(1)

# --- Network Configuration ---
# The IP address to listen on. "0.0.0.0" means listen on all available interfaces.
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Max size of the received message

PACKET_FORMAT = "!LhhhhhhBBBBBBBBBB"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

TIMEOUT_SEC = 1.0  # For example

def check_root_permissions():
    """Exits the script if it's not run as root."""
    if os.geteuid() != 0:
        print("Error: This script must be run as root to create a virtual device.")
        print("Please use 'sudo python3 joystick_receiver.py'")
        sys.exit(1)

def init_udp_socket():
    # Create the UDP socket
    # ipv4 values of Ip and Datagram(udp) mode
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # bbind to the ip:port transmitter
        sock.bind((UDP_IP, UDP_PORT))
    
    # control exceptions
    except Exception as e:
        print("Error binding UDP socket:", e)
        # outputs with error
        sys.exit(1)
    
    # return the socket conexion
    return sock

def create_virtual_joystick():
    """
    Creates a virtual joystick. Note: L3/R3 clicks are removed as they
    are no longer in the new protocol.
    """
    # Define the events our virtual controller will support.
    events = (
        # Face Buttons & Shoulder Buttons
        uinput.BTN_SOUTH, uinput.BTN_EAST, uinput.BTN_NORTH, uinput.BTN_WEST,
        uinput.BTN_TL, uinput.BTN_TR,
        # Axes
        uinput.ABS_X + (-32767, 32767, 0, 0),
        uinput.ABS_Y + (-32767, 32767, 0, 0),
        uinput.ABS_RX + (-32767, 32767, 0, 0),
        uinput.ABS_RY + (-32767, 32767, 0, 0),
        uinput.ABS_Z + (-32767, 32767, 0, 0),
        uinput.ABS_RZ + (-32767, 32767, 0, 0),
        # D-Pad Hat
        uinput.ABS_HAT0X + (-1, 1, 0, 0),
        uinput.ABS_HAT0Y + (-1, 1, 0, 0),
    )
    try:
        # Create the virtual device.
        return uinput.Device(events, name="Virtual Networked Controller")
    except Exception as e:
        print(f"Error creating virtual device: {e}")
        print("Ensure the 'uinput' kernel module is loaded (`sudo modprobe uinput`).")
        sys.exit(1)

def main():
    """Main execution function."""
    check_root_permissions()
    # init_udp_socket() already binds the socket.
    sock = init_udp_socket()
    device = create_virtual_joystick()
    
    print(f"Listening on UDP {UDP_IP}:{UDP_PORT}...")
    print("Virtual joystick created. Press Ctrl+C to stop.")

    # Initialize state variables before the loop
    last_packet_time = time.time()
    last_axes = [0] * 6
    last_buttons = [0] * 10

    try:
        while True:
            sock.settimeout(0.05)
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)

                if len(data) == PACKET_SIZE:
                    last_packet_time = time.time()
                    unpacked_data = struct.unpack(PACKET_FORMAT, data)
                    
                    # Update the last known state
                    last_axes = list(unpacked_data[1:7])
                    last_buttons = list(unpacked_data[7:18])
            
            except socket.timeout:
                pass
            
            if time.time() - last_packet_time > TIMEOUT_SEC:
                axes_to_send = last_axes.copy()
                axes_to_send[0:4] = [0] * 4  # Zero out joysticks
                buttons_to_send = last_buttons # Keep last button states
            else:
                axes_to_send = last_axes
                buttons_to_send = last_buttons

            # --- Emit all events to the virtual device ---
            # Use the variables that contain the failsafe logic
            device.emit(uinput.ABS_X, axes_to_send[0], syn=False)
            device.emit(uinput.ABS_Y, axes_to_send[1], syn=False)
            device.emit(uinput.ABS_RX, axes_to_send[2], syn=False)
            device.emit(uinput.ABS_RY, axes_to_send[3], syn=False)
            device.emit(uinput.ABS_Z, axes_to_send[4], syn=False)
            device.emit(uinput.ABS_RZ, axes_to_send[5], syn=False) 
            
            device.emit(uinput.BTN_SOUTH, buttons_to_send[0], syn=False)
            device.emit(uinput.BTN_EAST,  buttons_to_send[1], syn=False)
            device.emit(uinput.BTN_WEST, buttons_to_send[2], syn=False)
            device.emit(uinput.BTN_NORTH,  buttons_to_send[3], syn=False)
            device.emit(uinput.BTN_TL,    buttons_to_send[4], syn=False)
            device.emit(uinput.BTN_TR,    buttons_to_send[5], syn=False)
            
            hat_y = buttons_to_send[6] - buttons_to_send[7]
            hat_x = buttons_to_send[9] - buttons_to_send[8]
            device.emit(uinput.BTN_DY, hat_y, syn=False)
            device.emit(uinput.BTN_DX, hat_x, syn=False)

            device.syn()

    except KeyboardInterrupt:
        print("\nShutting down receiver...")

    finally:
        sock.close()
        print("Socket closed and virtual device released.")

if __name__ == "__main__":
    main()