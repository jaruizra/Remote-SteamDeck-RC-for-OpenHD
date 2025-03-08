import socket

HOST = '0.0.0.0'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print("Servidor UDP escuchando en", HOST, PORT)
    while True:
        data, addr = s.recvfrom(1024)
        if not data:
            continue
        s.sendto(data, addr)
