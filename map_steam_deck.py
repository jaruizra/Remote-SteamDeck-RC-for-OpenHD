#!/usr/bin/python3

# librerias
import sys
import socket
import json
import sdl2
import sdl2.ext
import time

# lectura y salida
REFRESH_RATE_MS = 16  # 60Hz frecuencia aprox

def init_joystick():
    # initiate a joystick subsystem
    if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
        # error
        print("SDL Init error:", sdl2.SDL_GetError().decode())
        sys.exit(1)
    # check the number of joystick connected
    if sdl2.SDL_NumJoysticks() < 1:
        #error
        print("No joystick found.")
        sdl2.SDL_Quit()
        sys.exit(1)

    # I get the firsrt joystick to use
    joystick = sdl2.SDL_JoystickOpen(0)
    # error to open the joystick
    if not joystick:
        print("Failed to open joystick:", sdl2.SDL_GetError().decode())
        sdl2.SDL_Quit()
        sys.exit(1)
    # I return the joystick I conencted to
    return joystick

def read_joystick_state(event, axis_values, button_values):
    # Process pending SDL events and stores them in event
    while sdl2.SDL_PollEvent(event) != 0:

        #print("The event is = " + str(event.type))

        # joystick and triggers
        if event.type == sdl2.SDL_JOYAXISMOTION:
            value = event.jaxis.value
            # Uncomment for debugging:
            print(f"Axis {event.jaxis.axis} updated: {value}")

        # d-pad y botones
        elif event.type in (sdl2.SDL_JOYBUTTONDOWN, sdl2.SDL_JOYBUTTONUP):
            print("The event is = " + str(event.jbutton.button))
            value = event.jbutton.state
            # Uncomment for debugging:
            print(f"Button {event.jbutton.button} state: {value}")

        # caso de salida, salgo sin error
        elif event.type == sdl2.SDL_QUIT:
            # sale con error
            sys.exit(0)
            

def send_state(sock, ip, port, axis_values, button_values):
    # Prepare a JSON message with the state of axes and buttons
    data = {
        "axis": axis_values,
        "buttons": button_values
    }
    # create the message to share in a json string
    message = json.dumps(data)
    # convert json to byte throught the udp socket
    sock.sendto(message.encode(), (ip, port))

def main():
    # open a joystick
    joystick = init_joystick()

    # Enable processing of joystick events with sdl event handling mechanism
    # this makes sdl2 to generate events -> for the event loop I created
    sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)

    # create an sdl_event objet/instance -> read data will be stored
    event = sdl2.SDL_Event()

    # Dictionaries to hold state for axes and buttons
    axis_values = {0: 0, 1: 0, 2: 0, 3: 0}
    button_values = {11: 0, 12: 0, 13: 0, 14: 0}


    try:
        # bucle
        while True:
            # read values
            read_joystick_state(event, axis_values, button_values)
            # delay in the reading of events
            sdl2.SDL_Delay(REFRESH_RATE_MS)
    
    # close conexion at the end
    except KeyboardInterrupt:
        print("Exiting transmitter...")
    
    finally:
        # close sdl joystick
        sdl2.SDL_JoystickClose(joystick)
        # quit sdl2
        sdl2.SDL_Quit()

# Main program
if __name__ == "__main__":
    main()
