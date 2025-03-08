import socket

HOST = '0.0.0.0'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("Servidor TCP escuchando en", HOST, PORT)
    conn, addr = s.accept()
    with conn:
        print("Conectado a", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
