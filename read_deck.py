#!/usr/bin/python3

import sys
import sdl2
import sdl2.ext
import socket

# Configuración del servidor TCP
TCP_IP = "100.77.204.87"  # Cambia esta IP por la de tu servidor
TCP_PORT = 5005           # Cambia el puerto según necesites

def main():
    # Conexión al servidor TCP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
        print("Conectado a", TCP_IP, "en el puerto", TCP_PORT)
    except Exception as e:
        print("Error al conectar al servidor:", e)
        return 1

    # Inicializa SDL2 para el joystick
    if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
        print("No se pudo inicializar SDL:", sdl2.SDL_GetError().decode())
        return 1

    # Verifica que haya al menos un joystick conectado
    num_joysticks = sdl2.SDL_NumJoysticks()
    if num_joysticks < 1:
        print("No se encontró ningún joystick conectado.")
        sdl2.SDL_Quit()
        return 1

    # Abre el primer joystick (índice 0)
    joystick = sdl2.SDL_JoystickOpen(0)
    if not joystick:
        print("No se pudo abrir el joystick:", sdl2.SDL_GetError().decode())
        sdl2.SDL_Quit()
        return 1

    # Imprime información básica del joystick
    joystick_name = sdl2.SDL_JoystickName(joystick)
    joystick_name = joystick_name.decode("utf-8") if joystick_name else "Desconocido"
    print("Joystick:", joystick_name)
    print("Número de ejes:", sdl2.SDL_JoystickNumAxes(joystick))
    print("Número de botones:", sdl2.SDL_JoystickNumButtons(joystick))
    print("Número de hats:", sdl2.SDL_JoystickNumHats(joystick))

    # Habilita la recepción de eventos para procesar, por ejemplo, el cierre de la ventana
    sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)
    
    running = True
    event = sdl2.SDL_Event()

    try:
        while running:
            # Procesar eventos (esto es opcional, pero permite detectar SDL_QUIT)
            while sdl2.SDL_PollEvent(event) != 0:
                if event.type == sdl2.SDL_QUIT:
                    running = False

            # Realiza el polling de los valores del joystick a 60Hz
            # Leer valores de los ejes 0, 1, 2 y 3
            axis0 = sdl2.SDL_JoystickGetAxis(joystick, 0)
            axis1 = sdl2.SDL_JoystickGetAxis(joystick, 1)
            axis2 = sdl2.SDL_JoystickGetAxis(joystick, 2)
            axis3 = sdl2.SDL_JoystickGetAxis(joystick, 3)
            # Leer estados de los botones 11, 12, 13 y 14
            button11 = sdl2.SDL_JoystickGetButton(joystick, 11)
            button12 = sdl2.SDL_JoystickGetButton(joystick, 12)
            button13 = sdl2.SDL_JoystickGetButton(joystick, 13)
            button14 = sdl2.SDL_JoystickGetButton(joystick, 14)

            # Construir un string con todos los valores
            # Puedes cambiar el formato del mensaje según tus necesidades
            message = (
                f"A0:{axis0};A1:{axis1};A2:{axis2};A3:{axis3};"
                f"B11:{button11};B12:{button12};B13:{button13};B14:{button14}"
            )
            # Enviar el mensaje por el socket TCP
            try:
                sock.send(message.encode())
            except Exception as e:
                print("Error al enviar datos:", e)

            # Opcional: imprimir el mensaje para depuración
            # print(message)

            # Retardo para aproximar 60Hz (1000ms/60 ≈ 16.67ms)
            sdl2.SDL_Delay(16)
    except KeyboardInterrupt:
        print("Interrupción por teclado. Saliendo...")

    # Cerrar recursos
    sdl2.SDL_JoystickClose(joystick)
    sdl2.SDL_Quit()
    sock.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
