# WiFiJoystickBridge
A Python-based system for sending joystick input over WiFi using RabbitMQ, allowing one Linux PC to control another by emulating a virtual joystick.

# Libraries tested

- pyjoystick -> didnt work, only with no oled it seems
- pygame -> use by a lot of people, higher level
- inputs -> could not make it work

Final Solution.
Use OpenHD method of using sdl2, however, for testing purposes Im going to use it in python with pysdl2

Problema -> Soy va en modo admin.

Ejecutar con sudo o cambiar Udev Rules