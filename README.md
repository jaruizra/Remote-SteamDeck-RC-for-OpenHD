# OpenHD RC - WiFi Joystick Bridge

OpenHD RC is a Python-based system that reads joystick inputs, specifically from a Steam Deck, and transmits them over a WiFi network to be used as a remote control for OpenHD. This allows for a highly responsive, low-latency control solution using custom hardware.

The system uses SDL2 (via the `pysdl2` library) to capture high-resolution joystick data and transmits it efficiently using a custom binary format over UDP. The receiver script then creates a virtual joystick on the remote machine, which can be directly read by QOpenHD.

## Key Features

- **17-Channel RC Transmitter**: Captures and transmits 17 distinct channels, covering all axes, buttons, and triggers of the Steam Deck, making it fully compatible with OpenHD's RC system.
- **Low-Latency UDP Transmission**: Utilizes a custom-packed binary struct for minimal data overhead and real-time performance, ideal for remote control applications.
- **Virtual Joystick Emulation**: The receiver script creates a virtual `uinput` device, allowing any Linux-based system (including a Raspberry Pi running OpenHD) to recognize the transmitted data as a standard joystick.
- **Designed for Steam Deck**: The input mapping is specifically tailored for the Steam Deck, but the modular code allows for easy adaptation to other controllers.
- **Fail-Safe Mechanism**: Includes a timeout feature that centers the primary flight controls if the connection is lost, preventing flyaways.

## System Architecture

The project is composed of two main components:

- **Transmitter (`read_deck.py`)**:
    - Runs on the device with the physical joystick (e.g., a Steam Deck).
    - Uses the `steamdeck_input_api.py` module to read all joystick inputs via `pysdl2`.
    - Gathers data from 17 specific channels.
    - Packs the data into a compact binary format using a custom `struct`.
    - Transmits the data to a specified IP address and port over UDP.

- **Receiver (`joystick_receiver.py`)**:
    - Runs on the remote machine (e.g., a Raspberry Pi with OpenHD).
    - Listens for incoming UDP packets on the specified port.
    - Unpacks the binary data to reconstruct the joystick state.
    - Creates a virtual joystick using the `python-uinput` library.
    - Emits joystick events that can be read by any application, such as QOpenHD.

## Communication Protocol

- **Transport**: UDP
- **Port**: `5005` (configurable)
- **Payload**: A custom binary struct designed for efficiency.

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

## Communication Protocol

- **Transport**: UDP
- **Port**: `5005` (configurable)
- **Payload**: A custom binary struct designed for efficiency.

The data is packed in the following format:
- **Format String**: `!LhhhhhhBBBBBBBBBB`
- **Contents**:
    - `L`: Sequence Number (Unsigned Long)
    - `h` (x6): Six 16-bit signed integers for the analog axes (LX, LY, RX, RY, L2, R2).
    - `B` (x10): Ten 8-bit unsigned integers for the digital buttons (A, B, X, Y, L1, R1, D-Pad Up/Down/Left/Right).

## Installation and Usage

### Prerequisites

- Two Linux-based machines (e.g., a Steam Deck and a Raspberry Pi).
- Python 3 and `pip` installed on both machines.
- A network connection (WiFi or Ethernet) between the two devices.

## 1. Install Required Packages

Install Git and Python Pip:

```bash
sudo apt update
sudo apt install git python3-pip -y
```

## 2. Clone the Project Repository

Clone your project repository (replace <repository-url> with your repository's URL):

```bash
git clone <repository-url>
cd <repository-directory>
```

## 3. Install Python Dependencies

Install the dependencies package:

```bash
sudo pip install -r requirements.txt
```
 
## 4. Verify uinput Module Availability

Check if the uinput module is loaded:

```bash
lsmod | grep uinput
```

- If you see no output: The module is not loaded; proceed to the next step.

## 5. Load the uinput Module Manually

Enable the module manually:

```bash
sudo modprobe uinput
```

Then, verify again:

lsmod | grep uinput

- If there is still no output: Additional steps may be required (e.g., verifying your kernel configuration or setting up udev rules).

## 6. Run the Program

Finally, execute the program on the steam deck:

```bash
sudo ./read_deck.py
```

Then, execute the program where the OpenHD Ground is located:

```bash
sudo ./joystick_receiver.py
```

### 6.1 Optional

If you want to test if its working. Run on the device where OpenHD Ground is located the following script:

```bash
sudo ./test.py
```

## Contributing

Contributions are welcome! Fork the repository and submit pull requests with detailed descriptions of your changes.

Or suggest improvements in the issues tab
