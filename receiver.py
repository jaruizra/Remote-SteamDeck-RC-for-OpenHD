#!/usr/bin/python3
"""
A network receiver that listens for joystick data over UDP and creates a
virtual joystick on the local machine using the 'uinput' library.

This script must be run with root privileges (e.g., 'sudo python3 receiver.py')
to have permission to create a virtual input device.
"""

import sys
import os
import socket
import json
import time

try:
    import uinput
except ImportError:
    print("Error: The 'python-uinput' library is required.")
    print("Please install it using: pip install python-uinput")
    sys.exit(1)

# --- Network Configuration ---
# The IP address to listen on. "0.0.0.0" means listen on all available interfaces.
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Max size of the received message

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
    Create a virtual joystick with 4 axes and 4 buttons.
    Axes range: 0 to 32767
    """
    axis_capabilities = (
        uinput.ABS_X + (-32767, 32767, 0, 0),
        uinput.ABS_Y + (-32767, 32767, 0, 0),
        uinput.ABS_Z + (-32767, 32767, 0, 0),
        uinput.ABS_RZ + (-32767, 32767, 0, 0),
    )
    button_capabilities = (
        uinput.BTN_A,
        uinput.BTN_B,
        uinput.BTN_X,
        uinput.BTN_Y,
    )
    events = axis_capabilities + button_capabilities
    device = uinput.Device(events, name="Virtual Joystick")
    return device

def manage_data(sock, device, axis, buttons):
    # receive data from socket
    data, addr = sock.recvfrom(BUFFER_SIZE)

    # decode data from bytes to utf-8
    message = data.decode('utf-8')
    
    # Parse the JSON message to extract the joystick state
    try:
        state = json.loads(message)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return
    
    # add those values to axis
    for i in range(4):
        axis[i] = state["axis"].get(str(i), 0)

    # add those values to buttons
    for i in range(4):
        buttons[i] = state["buttons"].get(str(11 + i), 0)

    # Emit button events
    device.emit(uinput.BTN_A, buttons[0], syn=False)
    device.emit(uinput.BTN_B, buttons[1], syn=False)
    device.emit(uinput.BTN_X, buttons[2], syn=False)
    device.emit(uinput.BTN_Y, buttons[3], syn=False)

    # Emit axis events
    device.emit(uinput.ABS_X, axis[0], syn=False)
    device.emit(uinput.ABS_Y, axis[1], syn=False)
    device.emit(uinput.ABS_Z, axis[2], syn=False)
    device.emit(uinput.ABS_RZ, axis[3], syn=False)

    # Synchronize events
    device.syn()
    
    # print receive data
    #print(message)
    

def main():
    # Create the udp socket
    sock = init_udp_socket()
    print(f"Listening on UDP port {UDP_PORT}...")

    # create joystick
    device = create_virtual_joystick()
    print("Virtual joystick created.")
    
    # Initial states
    axis = [0, 0, 0, 0]  # For ABS_X, ABS_Y, ABS_Z, ABS_RZ
    buttons = [0, 0, 0, 0]  # For BTN_A, BTN_B, BTN_X, BTN_Y

    try:
        # bucle
        while True:
            manage_data(sock, device, axis, buttons)
            
    # close conexion at the end 
    except KeyboardInterrupt:
        print("Exiting receiver...")

    finally:
        # close udp socket connection
        sock.close()

# Main program
if __name__ == "__main__":
    main()
