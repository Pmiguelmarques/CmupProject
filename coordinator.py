import websockets
import asyncio 
import socket
import threading
import time
import operator

charMap = {'total': 0}
totalChar = 0
host = '127.0.0.1'
port = 8081
currentPage = ""
bl = []

async def handler(websocket, path):
    message = await websocket.recv()
    print(message)
    while True:
        message = await websocket.recv()
        print(message)
        currentPage = message


def browserThread():
    start_server = websockets.serve(handler, 'localhost', 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def findPattern():
    newDict = dict(sorted(charMap.items(), key=operator.itemgetter(1), reverse=True)[:4])
    print(list(newDict.keys()))
    if all(item in ['w','s','d','a','Key.up', 'Key.down', 'Key.left', 'Key.right'] for item in list(newDict.keys())):
        return "gaming"
    return "clear"

def inputThread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 8091))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                if(data not in charMap):
                    charMap[data] = 1
                else:
                    charMap[data] += 1

def decisionMaking():
    while True:
        charMap = {}
        totalChar = 0
        time.sleep(30)
        if currentPage in bl:
            print("NOT WORKING!")
        else:
            if findPattern() == "gaming":
                print("NOT WORKING!")
            elif findPattern() == "clear":
                print("Working")

iThread = threading.Thread(target=inputThread)
dThread = threading.Thread(target=decisionMaking)


iThread.start()
dThread.start()
asyncio.run(browserThread())





