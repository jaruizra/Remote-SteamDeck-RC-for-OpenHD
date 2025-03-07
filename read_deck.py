import sys
import sdl2
import sdl2.ext

def main():
    # Inicializa SDL2 con el subsistema de joystick
    if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
        print("No se pudo inicializar SDL:", sdl2.SDL_GetError().decode())
        return 1

    # Verifica la cantidad de joysticks conectados
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

    # Obtiene e imprime información básica del joystick
    joystick_name = sdl2.SDL_JoystickName(joystick)
    if joystick_name is not None:
        joystick_name = joystick_name.decode("utf-8")
    else:
        joystick_name = "Desconocido"

    print("Joystick:", joystick_name)
    print("Número de ejes:", sdl2.SDL_JoystickNumAxes(joystick))
    print("Número de botones:", sdl2.SDL_JoystickNumButtons(joystick))

    # Habilita la recepción de eventos de joystick
    sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)

    running = True
    event = sdl2.SDL_Event()
    while running:
        # Procesa todos los eventos pendientes
        while sdl2.SDL_PollEvent(event) != 0:
            if event.type == sdl2.SDL_JOYAXISMOTION:
                print("Eje", event.jaxis.axis, "movido a", event.jaxis.value)
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                print("Botón", event.jbutton.button, "presionado")
            elif event.type == sdl2.SDL_JOYBUTTONUP:
                print("Botón", event.jbutton.button, "liberado")
            elif event.type == sdl2.SDL_QUIT:
                running = False

        # Pequeño retardo para no saturar la CPU
        sdl2.SDL_Delay(1000)

    # Cierra el joystick y finaliza SDL2
    sdl2.SDL_JoystickClose(joystick)
    sdl2.SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
