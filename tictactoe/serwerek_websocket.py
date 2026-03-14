import socket
import threading
import json

# Uruchom z terminala: python3 serverek_na_portach.py
# Potam jak z dwoch innych terminali uruchomisz gre (pytohon3 tictactoe/main_jeden_gracz.py) to beda sie nawzajem widziec i grac ze soba


HOST = "127.0.0.1"
PORT = 9000

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)
print(f"Server started on {HOST}:{PORT}")

def handle_client(client):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                clients.remove(client)
                client.close()
                break

            messages = data.decode().split("\n")
            for msg in messages:
                if not msg.strip():
                    continue

                for c in clients:
                    if c != client:
                        c.send((msg + "\n").encode())

        except ConnectionResetError:
            clients.remove(client)
            client.close()
            break

while True:
    client, addr = server.accept()
    print(f"Connected: {addr}")
    clients.append(client)
    threading.Thread(target=handle_client, args=(client,), daemon=True).start()