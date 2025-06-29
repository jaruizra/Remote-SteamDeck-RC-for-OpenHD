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
    # Create the udp socket
    sock = init_udp_socket()
    sock.bind((UDP_IP, UDP_PORT))
    # Create the virtual joystick device
    device = create_virtual_joystick()
    
    print(f"Listening on UDP {UDP_IP}:{UDP_PORT}...")
    print("Virtual joystick created. Press Ctrl+C to stop.")

    try:
        # Main listening loop
        while True:
            sock.settimeout(0.05)
            try:
                # Block and wait for one packet to arrive.
                data, addr = sock.recvfrom(BUFFER_SIZE)

                # Ensure the packet has the correct size before processing.
                if len(data) == PACKET_SIZE:
                    last_packet_time = time.time()
                    # Unpack the binary data using the defined format.
                    unpacked_data = struct.unpack(PACKET_FORMAT, data)
                    
                    # Extract the axis and button values.
                    # We ignore the sequence number at index 0 - sequence number
                    axes = unpacked_data[1:7]
                    buttons = unpacked_data[7:17]
            
            except socket.timeout:
                pass
            
            # Check if we exceeded the timeout
            if time.time() - last_packet_time > TIMEOUT_SEC:
                # Use the old axes but zero out the first 4 (joysticks)
                axes_to_send = last_axes.copy()
                axes_to_send[0:4] = [0]*4
                buttons_to_send = last_buttons  # Keep last button states
            else:
                # Use last valid data
                axes_to_send = last_axes
                buttons_to_send = last_buttons

            # --- Emit all events to the virtual device ---
            # syn=False batches them until we call device.syn() at the end.
            device.emit(uinput.ABS_X, axes[0], syn=False)
            device.emit(uinput.ABS_Y, axes[1], syn=False)
            device.emit(uinput.ABS_RX, axes[2], syn=False)
            device.emit(uinput.ABS_RY, axes[3], syn=False)
            # L2 Trigger
            device.emit(uinput.ABS_Z, axes[4], syn=False)
            # R2 Trigger 
            device.emit(uinput.ABS_RZ, axes[5], syn=False) 
            
            # Map the 10 received buttons to their uinput events
            device.emit(uinput.BTN_SOUTH, buttons[0], syn=False) # A
            device.emit(uinput.BTN_EAST,  buttons[1], syn=False) # B
            device.emit(uinput.BTN_NORTH, buttons[2], syn=False) # X
            device.emit(uinput.BTN_WEST,  buttons[3], syn=False) # Y
            device.emit(uinput.BTN_TL,    buttons[4], syn=False) # L1
            device.emit(uinput.BTN_TR,    buttons[5], syn=False) # R1

            # D-Pad logic using the 4 d-pad buttons
            # buttons[6] = Up
            # buttons[7] = Down
            # buttons[8] = Left
            # buttons[9] = Right
            hat_y = buttons[7] - buttons[6]  # Down - Up
            hat_x = buttons[9] - buttons[8]  # Right - Left
            device.emit(uinput.ABS_HAT0Y, hat_y, syn=False)
            device.emit(uinput.ABS_HAT0X, hat_x, syn=False)

            # Apply all the batched events at once.
            device.syn()

    except KeyboardInterrupt:
        print("\nShutting down receiver...")

    finally:
        # Clean up resources.
        sock.close()
        print("Socket closed and virtual device released.")

if __name__ == "__main__":
    main()