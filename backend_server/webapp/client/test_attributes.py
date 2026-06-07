import time
from websocket_client import WebSocketGameClient
import threading

def on_message(msg: str):
    print(f"RECEIVED: {msg}")

client = WebSocketGameClient("ws://localhost:8080/ws/chat", on_message_callback=on_message)
print("Registering...")
try:
    client.register("http://localhost:8080/api/auth/register", "testuser", "testpass")
except Exception as e:
    pass # probably already exists

print("Logging in...")
client.login("http://localhost:8080/api/auth/login", "testuser", "testpass")
print("Connecting...")
client.connect()

time.sleep(1)
print("Creating room...")
client.send({"messageType": "CREATENEWROOM_REQUEST", "roomId": "room123", "playerName": "testuser"})

time.sleep(1)
print("Setting attributes...")
client.send({"messageType": "SETFACTION_REQUEST", "faction": "Hegemonia", "status": "ACTIVE"})

time.sleep(2)
client.close()
