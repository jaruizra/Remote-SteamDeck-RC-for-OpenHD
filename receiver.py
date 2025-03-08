#!/usr/bin/python3
import socket

def main():
    # Configuración del servidor: escucha en todas las interfaces en el puerto 5005.
    TCP_IP = "100.110.183.73"
    TCP_PORT = 5005
    BUFFER_SIZE = 1024  # Tamaño del buffer para recibir datos

    # Crear socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(1)  # Escucha 1 conexión entrante
    print(f"Servidor escuchando en {TCP_IP}:{TCP_PORT}...")

    # Aceptar una conexión entrante
    conn, addr = server_socket.accept()
    print("Conexión recibida de:", addr)

    try:
        while True:
            # Recibir datos
            data = conn.recv(BUFFER_SIZE)
            if not data:
                # Se cierra la conexión si no hay más datos
                print("Conexión cerrada por el cliente.")
                break

            # Decodificar y procesar el mensaje recibido
            message = data.decode("utf-8")
            print("Mensaje recibido:", message)
    except KeyboardInterrupt:
        print("Interrupción por teclado. Cerrando servidor...")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    main()
