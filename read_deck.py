#!/usr/bin/python3
"""
A network transmitter that reads controller state using the Joystick class
and sends it over UDP.

This script imports the `Joystick` class from `steamdeck_input_api.py` and uses
it to get the full state of the controller, which is then serialized to JSON
and broadcasted on the network.
"""

if os.geteuid() != 0:
    print("Error: This script must be run as root. Please use 'sudo'.")
    sys.exit(1)

# librerias
import sys
import socket
import json
import time

# --- Assumes your main script is named steamdeck_input_api.py ---
try:
    from joystick_script import Joystick
except ImportError:
    print("Error: Could not import the Joystick class.")
    print("Please ensure 'joystick_script.py' is in the same directory.")
    sys.exit(1)


# --- Network Configuration ---
# The destination IP address for the UDP packets.
# Change this to the IP address of the receiving computer.UDP_IP = "100.121.21.44"
UDP_IP = "192.168.3.1"
UDP_PORT = 5005

# --- Performance Configuration ---
TRANSMIT_RATE_HZ = 60
TRANSMIT_DELAY_SEC = 1 / TRANSMIT_RATE_HZ

def init_udp_socket():
    # Create the UDP socket
    # ipv4 values of Ip and Datagram(udp) mode
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main():
    """
    Main execution function. Initializes the joystick and the network socket,
    then enters a loop to read and transmit data.
    """
    # Create the udp socket
    sock = init_udp_socket()

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

            # Get the specific states you requested from the controller.
            # Each of these is a fast dictionary read.
            data_to_send = {
                "joysticks": joystick.joystick_state,
                "face_buttons": joystick.face_buttons,
                "shoulders": joystick.shoulder_state,
                "dpad": joystick.dpad_state
            }

            # Serialize the combined dictionary to a JSON string.
            # We use separators=(',', ':') for a more compact message.
            message = json.dumps(data_to_send, separators=(',', ':'))

            # Send the data over the network. The string must be encoded to bytes.
            sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))

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
