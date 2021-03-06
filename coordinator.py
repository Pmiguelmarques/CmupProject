import websockets
import asyncio 
import socket
import threading
import time
from tensorflow.keras.models import load_model
import numpy as np
from tkinter import *
from queue import Queue
from PIL import ImageTk, Image
from tkinter.font import BOLD, Font


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
shutDown = False
browserSocket = set()

# Browser and popup specifics
q = Queue()
q_messages_to_browser = Queue()
visited_pages = []
wl = []
bl = []
initialization = True

async def handler(websocket, path):

    browserSocket.add(websocket)
   
    while True:

        # check if there are messages to be transmitted to the browser, that is, the urls in the blacklist
        if not q_messages_to_browser.empty():
            
            while not q_messages_to_browser.empty():
                to_send = q_messages_to_browser.get()
                print("to send " + to_send)
                await websocket.send(to_send)
                

        message = await websocket.recv()

        print(message)

        if message != 'Connected':

            if message not in visited_pages:

                visited_pages.append(message)
        
        
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

def checkStatus(timeFrame):
    status = 0
    for i in timeFrame:
        if i == 'gaming':
            status += 1
    if(status==2):
        return True
    return False


def decisionMaking():

    global visited_pages
    global wl
    global bl
    global initialization

    # Read the allowed sites from the corresponding file

    if initialization:

        print("Reading file with the allowed sites")
        f = open("allowed_sites.txt", "r")
        for line in f:
            wl.append(line.strip())
        
        initialization = False

    print("Allowed websites")
    print(wl)

    working = False

    timeFrame = []

    while True:

        charMap = {}
        totalChar = 0
        time.sleep(60)

        print("Visited pages")
        print(visited_pages)

        # Browser forming blacklist to be sent to the extension
        #********************************

        if len(visited_pages) != 0:

            for page in visited_pages:
                
                accepted = False

                for acceptable_page in wl:

                    if acceptable_page.lower() in str(page).lower():
                        
                            accepted = True

                if not accepted:

                    if page not in bl:

                        bl.append(page)           
                        
                        
        visited_pages = []

        #*******************************

        aval = findPattern()
        timeFrame.append(aval)
        
        if checkStatus(timeFrame):
            print("NOT WORKING")
            timeFrame = []
            working = False

            q.put(working)

            for not_allowed_page in bl:
                q_messages_to_browser.put(not_allowed_page)
            
            bl = []

        elif len(timeFrame) == 6:
            print("GOOD JOB")
            timeFrame = []
            working = True

            q.put(working)
            
            for not_allowed_page in bl:
                print("not allowed " + not_allowed_page)
                q_messages_to_browser.put(not_allowed_page)
            
            bl = []

        charArray[0][:] = 0

        

class GUIBuilder(object):
    def __init__(self, root, message, render):
        root.title("Work Status")
        root.geometry("400x400")
        bold20 = Font(root, size=20, weight=BOLD)
        label = Label(root, text=message, font=bold20).pack(side = TOP, pady = 10)
        img = Label(root, image=render)
        img.image = render
        img.pack(side = TOP)

def show_popup():  

    while True:

        work_flag = q.get()

        root = Tk()

        message =""

        #work_flag = True

        if work_flag == True:
            message = "Continue the good job!"

            load = Image.open("good_job.jpg")

        else:
            message = "Get back to work!"

            load = Image.open("warning_sign.jpg")


        image = load.resize((250, 250))

        render = ImageTk.PhotoImage(image)

        gui_builder = GUIBuilder(root, message, render)

        root.mainloop()


nnModel = load_model('nn.h5')
print(nnModel.summary())
iThread = threading.Thread(target=inputThread)
dThread = threading.Thread(target=decisionMaking)
gui_thread = threading.Thread(target=show_popup)

gui_thread.daemon = True
gui_thread.start()
iThread.start()
dThread.start()


asyncio.run(browserThread())









