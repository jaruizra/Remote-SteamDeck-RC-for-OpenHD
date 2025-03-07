import sys
import pygame

pygame.init()  # Initializes all of pygame's modules.
pygame.display.set_mode((200, 200))  # Create a small window to capture events.
pygame.joystick.init()  # Initialize joystick module

# Get a list of joystick objects
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print("Available joysticks:", joysticks)

if joysticks:
    joystick = joysticks[0]
    joystick.init()  # Ensure the joystick is initialized
    print("Using joystick:", joystick.get_name())
else:
    print("No joysticks found.")
    sys.exit()

# Map event types to a descriptive event category name
event_categories = {
    pygame.JOYAXISMOTION: "Axis Movement",
    pygame.JOYBUTTONDOWN: "Button Press",
    pygame.JOYBUTTONUP: "Button Release",
    pygame.JOYHATMOTION: "Hat Movement"
}

print("Waiting for input... (Press ESC to quit)")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type in event_categories:
            category = event_categories[event.type]
            # Compose a message with the event name, category, and details
            if event.type == pygame.JOYAXISMOTION:
                print(f"{category}: Axis {event.axis}, Value {event.value}")
            elif event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
                print(f"{category}: Button {event.button}")
            elif event.type == pygame.JOYHATMOTION:
                print(f"{category}: Hat {event.hat}, Value {event.value}")