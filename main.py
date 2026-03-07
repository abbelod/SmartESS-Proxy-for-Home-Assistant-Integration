import socket, time
from datetime import datetime

HOST = "0.0.0.0"
PORT = 502

GET_DATA_HEX = "3D0C00010003001100"

def hex_to_bytes(h):
    return bytes.fromhex(h)

def bytes_to_hex(b):
    return " ".join(f"{x:02X}" for x in b)

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"{datetime.now()} - Client connected: {addr[0]}")

        try:
            conn.settimeout(10)

            while True:
                conn.sendall(hex_to_bytes(GET_DATA_HEX))
                print(f"{datetime.now()} - Sent init: {GET_DATA_HEX}")
                data = conn.recv(4096)
                if not data:
                    raise ConnectionResetError("Client disconnected")

                print(
                    f"{datetime.now()} - RX: {bytes_to_hex(data)}"
                )
                time.sleep(1)

        except (socket.timeout, ConnectionResetError, BrokenPipeError) as e:
            print(f"{datetime.now()} - Connection lost: {e}")

        finally:
            conn.close()
            print(f"{datetime.now()} - Waiting for new client...\n")

if __name__ == "__main__":
    run_server()
