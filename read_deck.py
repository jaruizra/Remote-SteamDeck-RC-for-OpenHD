import pygame

pygame.joystick.init()

# Get a list of joystick objects
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

print("Available joysticks:", joysticks)

if joysticks:
    # For example, use the first joystick
    joystick = joysticks[0]
    joystick.init()  # Ensure the joystick is initialized
    print("Joystick instance ID:", joystick.get_instance_id())

    # el nombre
    print("Joystick instance ID:", joystick.get_name())

else:
    print("No joysticks found.")
