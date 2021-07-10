from pynput import keyboard
import threading
import socket
#import paho.mqtt.client as mqtt


charQueue = []

def on_press(key):
    print(key)
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        charQueue.append(key.char)
    except AttributeError:
        #print('special key {0} pressed'.format(key))
        charQueue.append(str(key))
    
def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        return False


def func1():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    
def func2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 8091))
        while True:
            if len(charQueue) != 0:
                charSend = charQueue.pop(0)
                s.sendall(charSend.encode('utf-8'))
    


thread1 = threading.Thread(target=func1)
thread2 = threading.Thread(target=func2)
thread1.start()
thread2.start()

#listener.start()