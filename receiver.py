#!/usr/bin/python3
import sys
import socket

UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005
BUFFER_SIZE = 1024

def init_udp_socket():
    # Create the UDP socket
    # ipv4 values of Ip and Datagram(udp) mode
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # bbind to the ip:port transmitter
        sock.bind((UDP_IP, UDP_PORT))
    
    # control exceptions
    except Exception as e:
        print("Error binding UDP socket:", e)
        # outputs with error
        sys.exit(1)
    
    # return the socket conexion
    return sock

def manage_data(sock):
    # receive data from socket
    data, addr = sock.recvfrom(BUFFER_SIZE)

    # decode data from bytes to utf-8
    message = data.decode('utf-8')

    # print receive data
    print(message)
    

def main():
    # Create the udp socket
    sock = init_udp_socket()

    print(f"Listening on UDP port {UDP_PORT}...")
    
    try:
        # bucle
        while True:
            manage_data(sock)
            
    # close conexion at the end 
    except KeyboardInterrupt:
        print("Exiting receiver...")

    finally:
        # close udp socket connection
        sock.close()

# Main program
if __name__ == "__main__":
    main()
