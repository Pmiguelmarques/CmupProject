import websockets
import asyncio 
import socket
import threading
import time


host = '127.0.0.1'
port = 8081

async def handler(websocket, path):
    while True:
        message = await websocket.recv()
        print(message)


def browserThread():
    start_server = websockets.serve(handler, 'localhost', 8081)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    

def inputThread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 8081))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)


bThread = threading.Thread(target=browserThread)
iThread = threading.Thread(target=inputThread)

iThread.start()

