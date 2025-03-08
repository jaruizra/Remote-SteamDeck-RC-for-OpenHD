import socket
import time

HOST = '0.0.0.0'  # Cambia por la IP del servidor
PORT = 5000
N = 100000

latencias = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for i in range(N):
        mensaje = b'ping'
        inicio = time.perf_counter()
        s.sendall(mensaje)
        # Espera la respuesta
        respuesta = s.recv(1024)
        fin = time.perf_counter()
        rtt = fin - inicio
        latencias.append(rtt)
        # Opcional: imprimir cada RTT
        # print(f"RTT {i}: {rtt*1000:.2f} ms")

promedio = sum(latencias) / N
print(f"Latencia promedio (RTT) con TCP: {promedio*1000:.2f} ms")
