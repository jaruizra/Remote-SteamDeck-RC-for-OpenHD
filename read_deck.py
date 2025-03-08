#!/usr/bin/python3

# librerias
import sys
import socket
import json
import sdl2 # para lectura de joystick en linux
import sdl2.ext
import time

# Receiver IP
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
REFRESH_RATE_MS = 16  # 60Hz frecuencia aprox

def init_udp_socket():
    # Create a UDP socket
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def init_joystick():
    if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
        print("SDL Init error:", sdl2.SDL_GetError().decode())
        sys.exit(1)
    if sdl2.SDL_NumJoysticks() < 1:
        print("No joystick found.")
        sdl2.SDL_Quit()
        sys.exit(1)
    joystick = sdl2.SDL_JoystickOpen(0)
    if not joystick:
        print("Failed to open joystick:", sdl2.SDL_GetError().decode())
        sdl2.SDL_Quit()
        sys.exit(1)
    return joystick

def read_joystick_state(event, axis_values, button_values):
    # Process all pending SDL events
    while sdl2.SDL_PollEvent(event) != 0:
        if event.type == sdl2.SDL_JOYAXISMOTION:
            # Update axis value if axis is 0, 1, 2, or 3
            if event.jaxis.axis in axis_values:
                axis_values[event.jaxis.axis] = event.jaxis.value
                # Uncomment for debugging:
                # print(f"Axis {event.jaxis.axis} updated: {event.jaxis.value}")
        elif event.type in (sdl2.SDL_JOYBUTTONDOWN, sdl2.SDL_JOYBUTTONUP):
            # For buttons 11, 12, 13, 14, update state: 1 for down, 0 for up
            if event.jbutton.button in (11, 12, 13, 14):
                button_values[event.jbutton.button] = 1 if event.type == sdl2.SDL_JOYBUTTONDOWN else 0
                # Uncomment for debugging:
                # print(f"Button {event.jbutton.button} state: {button_values[event.jbutton.button]}")
        elif event.type == sdl2.SDL_QUIT:
            sys.exit(0)

def send_state(sock, ip, port, axis_values, button_values):
    # Prepare a JSON message with the state of axes and buttons
    data = {
        "axes": [axis_values.get(i, 0) for i in range(4)],
        "buttons": [button_values.get(i, 0) for i in (11, 12, 13, 14)]
    }
    message = json.dumps(data)
    sock.sendto(message.encode(), (ip, port))

def main():
    sock = init_udp_socket()
    joystick = init_joystick()
    # Enable joystick events
    sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)
    event = sdl2.SDL_Event()

    # Dictionaries to hold state for axes and buttons
    axis_values = {0: 0, 1: 0, 2: 0, 3: 0}
    button_values = {11: 0, 12: 0, 13: 0, 14: 0}

    try:
        while True:
            read_joystick_state(event, axis_values, button_values)
            send_state(sock, UDP_IP, UDP_PORT, axis_values, button_values)
            sdl2.SDL_Delay(REFRESH_RATE_MS)
    except KeyboardInterrupt:
        print("Exiting transmitter...")
    finally:
        sdl2.SDL_JoystickClose(joystick)
        sdl2.SDL_Quit()
        sock.close()

if __name__ == "__main__":
    main()
