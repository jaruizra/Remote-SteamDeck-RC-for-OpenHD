#!/usr/bin/python3

import sys
import sdl2
import sdl2.ext
import socket

# Ip of the rpi ground
HOST = ""

D_PAD = []

# funcion para detectar los nombres
def detectar_nombre(event):
    # mirar que sea evento tipo dpad y guardar el nombre
    if event.type == sdl2.SDL_JOYHATMOTION:
        if event.jhat.which not in D_PAD:
            D_PAD.append(event.jhat.which)
            print("DPAD es = "event.jhat.which)


def main():
    # Initialize SDL2 with the joystick
    if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
        # print error that sdl2 got
        print("No se pudo inicializar SDL:", sdl2.SDL_GetError().decode())
        return 1    # return with error

    # get number of joysticks
    num_joysticks = sdl2.SDL_NumJoysticks()
    # Verify number of joysticks
    if num_joysticks < 1:
        print("No se encontró ningún joystick conectado.")
        sdl2.SDL_Quit() # Close SDL2
        return 1    # return with error

    # Abre el primer joystick (índice 0)
    joystick = sdl2.SDL_JoystickOpen(0)
    # Check opening error
    if not joystick:
        print("No se pudo abrir el joystick:", sdl2.SDL_GetError().decode())
        sdl2.SDL_Quit() # Close SDL2
        return 1    # return with error

    # Get joystick name
    joystick_name = sdl2.SDL_JoystickName(joystick)
    # Check error
    if joystick_name is not None:
        # get name
        joystick_name = joystick_name.decode("utf-8")
    else:
        joystick_name = "Desconocido"

    print("Joystick:", joystick_name)
    print("Número de ejes:", sdl2.SDL_JoystickNumAxes(joystick))
    print("Número de botones:", sdl2.SDL_JoystickNumButtons(joystick))

    # Habilita la recepción de eventos de joystick
    sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)

    # Get first event
    event = sdl2.SDL_Event()

    # Bucle infinito de busqueda
    running = True
    while running:
        # Get more events
        while sdl2.SDL_PollEvent(event) != 0:
            """
            #if event.type == sdl2.SDL_JOYAXISMOTION:
                #print("Eje", event.jaxis.axis, "movido a", event.jaxis.value)
            if event.type == sdl2.SDL_JOYBUTTONDOWN:
                print("Botón", event.jbutton.button, "presionado")

            elif event.type == sdl2.SDL_JOYBUTTONUP:
                print("Botón", event.jbutton.button, "liberado")

            elif event.type == sdl2.SDL_QUIT:
                running = False
            """
            detectar_nombre(event)

        # Pequeño retardo para no saturar la CPU
        sdl2.SDL_Delay(1000)

    # Cierra el joystick y finaliza SDL2
    sdl2.SDL_JoystickClose(joystick)
    sdl2.SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
