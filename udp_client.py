import socket
import time

HOST = '0.0.0.0'  # Cambia por la IP del servidor
PORT = 5000
N = 100000

latencias = []

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(1.0)  # Timeout de 1 segundo
    for i in range(N):
        mensaje = b'ping'
        inicio = time.perf_counter()
        s.sendto(mensaje, (HOST, PORT))
        try:
            respuesta, addr = s.recvfrom(1024)
            fin = time.perf_counter()
            rtt = fin - inicio
            latencias.append(rtt)
        except socket.timeout:
            print("Timeout en paquete", i)
            latencias.append(1.0)  # O maneja de otra forma
        # Opcional: imprimir cada RTT
        # print(f"RTT {i}: {rtt*1000:.2f} ms")

promedio = sum(latencias) / N
print(f"Latencia promedio (RTT) con UDP: {promedio*1000:.2f} ms")
