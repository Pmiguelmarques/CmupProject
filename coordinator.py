import websockets
import asyncio 
import socket
import threading
import time
import operator
from tensorflow.keras.models import load_model
import numpy as np

keyMap = {'a':0, 
    'b':1, 
    'c':2, 
    'd':3, 
    'e':4, 
    'f':5, 
    'g':6, 
    'h':7, 
    'i':8,
    'j':9,
    'k':10,
    'l':11,
    'm':12, 
    'n':13, 
    'o':14, 
    'p':15, 
    'q':16, 
    'r':17, 
    's':18, 
    't':19, 
    'u':20, 
    'v':21, 
    'w':22,
    'x':23,
    'y':24,
    'z':25,
    '0':26,
    '1':27,
    '2':28,
    '3':29,
    '4':30,
    '5':31,
    '6':32,
    '7':33,
    '8':34,
    '9':35,
    'Key.up':36,
    'Key.down':37,
    'Key.left':38,
    'Key.right':39,
    'Key.tab':40,
    'Key.shift':41,
    'Key.enter':42,
    'Key.backspace':43
    }

#charMap = {'total': 0}
charArray = np.zeros((1,44))
totalChar = 0
host = '127.0.0.1'
port = 8081
currentPage = ""
bl = []
shutDown = False
browserSocket = set()

async def handler(websocket, path):
    browserSocket.add(websocket)
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
    #print(charArray)
    predicitons = nnModel.predict(x=charArray, verbose=0)
    if(predicitons[0][0]>predicitons[0][1]):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
        return "gaming"
    else:
        print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEe")
        return "clear"
    
    '''newDict = dict(sorted(charMap.items(), key=operator.itemgetter(1), reverse=True)[:4])
    print(list(newDict.keys()))
    if all(item in ['w','s','d','a','Key.up', 'Key.down', 'Key.left', 'Key.right'] for item in list(newDict.keys())):
        return "gaming"
    return "clear"'''

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
                if data in keyMap:
                    #print(data)
                    charArray[0][keyMap[data]] += 1
                    #print(charArray)
                '''if(data not in charMap):
                    charMap[data] = 1
                else:
                    charMap[data] += 1'''

def checkStatus(timeFrame):
    status = 0
    for i in timeFrame:
        if i == 'gaming':
            status += 1
    if(status==2):
        return True
    return False

def shutAllDown():
    print(browserSocket)
    #browserSocket.send("ola".encode("utf-8"))

def decisionMaking():
    timeFrame = []
    while True:
        charMap = {}
        totalChar = 0
        time.sleep(10)
        #shutAllDown()
        if currentPage in bl:
            print("NOT WORKING!")
        else:
            if findPattern() == "gaming":
                print("Not working")
            elif findPattern() == "clear":
                print("Working")
            charArray[0][:] = 0
        '''    
        else:
            aval = findPattern()
            print(aval)
            timeFrame.append(aval)
            if(checkStatus(timeFrame)):
                print("NOT WORKING")
            elif(len(timeFrame)==6):
                print("Working")
                timeFrame = []
        for i in keyMap:
            keyMap[i] = 0
        '''
nnModel = load_model('nn.h5')
print(nnModel.summary())
iThread = threading.Thread(target=inputThread)
dThread = threading.Thread(target=decisionMaking)


iThread.start()
dThread.start()
asyncio.run(browserThread())





