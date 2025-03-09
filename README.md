# WiFiJoystickBridge

WiFiJoystickBridge is a Python-based system that transmits joystick input over WiFi, allowing one Linux PC to control another by emulating a virtual joystick. This project leverages SDL2 (via PySDL2) for capturing joystick events and uses UDP sockets for real-time, low-latency communication.

## Overview

The goal of WiFiJoystickBridge is to overcome the limitations of several joystick libraries by providing a real-time solution for remote control. After testing multiple libraries, SDL2 with PySDL2 was chosen for its reliability and low-level control capabilities.

> **Note:** Currently, the system requires administrative privileges. Run the application using `sudo` or update your Udev rules to grant non-root access to the joystick device.

## Features

- **Real-Time Data Transmission:**  
  Capture and send the state of four axes and four buttons over WiFi using UDP.
- **Virtual Joystick Emulation:**  
  Send joystick inputs from one Linux PC to another by emulating a virtual joystick.
- **Modular and Extensible:**  
  The project is designed to be easily improved and it has mapping of Steam Deck controls

## Tested Libraries

During development, several libraries were evaluated:

- **pyjoystick:**  
  *Issues:* Only seen functioned with the Steam Deck non-OLED version.
- **pygame:**  
  *Pros:* Widely used and higher-level.  
  *Cons:* Did not offer the low-level control required.
- **inputs:**  
  *Issues:* Could not be configured to work as needed.

**Final Solution:**  
The final implementation uses SDL2 (via PySDL2) to capture joystick inputs, combined with UDP sockets for transmitting data.

## Communication Method

- **UDP Sockets:**  
  The system packages joystick state (axes and buttons) in JSON format and transmits it over UDP. This method ensures low latency and simplicity.

## Installation

1. **Dependencies:**  
   Make sure you have Python 3 installed. Install the required Python libraries:
   ```bash
   pip install pysdl2
   (Install any additional dependencies as needed.)
   ```

2. **Running the Application:**  
    To run the transmitter or receiver, execute the corresponding script.  
    Run with administrative privileges (`sudo`) or configure Udev rules for joystick access.

## Project Structure

- **Transmitter:**  
  Captures joystick events using SDL2, packages the data as JSON, and sends it via UDP.
- **Receiver:**  
  Listens for UDP messages, decodes the JSON data, and processes the joystick state.

## TODO List

- **Input Mapping:**  
  Map all Steam Deck inputs using SDL2.
- **Data Organization:**  
  Structure input data into dictionaries grouping related buttons together.
- **Code Modularization:**  
  Refactor code into classes for better integration with other systems.

**Optional Enhancements:**
- **ZeroMQ Integration:**  
  Considering migrating to ZeroMQ to take advantage of its pub/sub model for scalable messaging.

## Contributing
Contributions are welcome! Fork the repository and submit pull requests with detailed descriptions of your changes.

Or suggest improvements in the issues tab