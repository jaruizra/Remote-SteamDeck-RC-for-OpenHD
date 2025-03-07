#include <SDL2/SDL.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_JOYSTICK | SDL_INIT_GAMECONTROLLER) < 0) {
        fprintf(stderr, "Error al inicializar SDL: %s\n", SDL_GetError());
        return 1;
    }

    int num_joysticks = SDL_NumJoysticks();
    printf("Número de joysticks conectados: %d\n", num_joysticks);

    for (int i = 0; i < num_joysticks; i++) {
        if (SDL_IsGameController(i)) {
            SDL_GameController *controller = SDL_GameControllerOpen(i);
            if (controller) {
                printf("Controlador %d abierto: %s\n", i, SDL_GameControllerName(controller));
            } else {
                printf("No se pudo abrir el controlador %d: %s\n", i, SDL_GetError());
            }
        } else {
            SDL_Joystick *joystick = SDL_JoystickOpen(i);
            if (joystick) {
                printf("Joystick %d abierto: %s\n", i, SDL_JoystickName(joystick));
            }
        }
    }

    SDL_Event event;
    while (1) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_JOYAXISMOTION) {
                printf("Movimiento de eje: %d en joystick %d, valor: %d\n",
                       event.jaxis.axis, event.jaxis.which, event.jaxis.value);
            }
            if (event.type == SDL_JOYBUTTONDOWN) {
                printf("Botón presionado: %d en joystick %d\n",
                       event.jbutton.button, event.jbutton.which);
            }
            // Otros eventos pueden ser manejados aquí...
        }
    }

    SDL_Quit();
    return 0;
}
