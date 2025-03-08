#!/usr/bin/python3
import sys
import socket

UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005
BUFFER_SIZE = 1024

def init_udp_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT))
    except Exception as e:
        print("Error binding UDP socket:", e)
        sys.exit(1)
    return sock

def main():
    sock = init_udp_socket()
    print(f"Listening on UDP port {UDP_PORT}...")
    
    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode('utf-8')
            print(f"Received from {addr}: {message}")
    except KeyboardInterrupt:
        print("Exiting receiver...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
