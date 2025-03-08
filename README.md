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


# Metodo de envio

- probar con un boton.
- probar a mandar cuando sube solo.


- Solo quiero mandar la info de 4 canales, que es throttle, yaw, pith y roll

- Tengo que al enviarlo mandarlo para que quede entre valores de (-32768 to 32767), del tipo Sint16(int16_t). De este modo cuando llegue ya está perfecto para emular y que coja el valor que yo quiero.