import socket

import logging
import os
import json
from datetime import date


from concurrent.futures import ThreadPoolExecutor

CONNECTION_QUEUE_SIZE = 10
BUFFER_SZ = 1024

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8080

LOG_FILE_PATH = '/home/cosmin/Logs/'


def create_logger(filename):
    formatter = logging.Formatter('[%(asctime)s] [%(thread)d] [%(process)d] : %(message)s')
    file_handler = logging.FileHandler(filename=filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(filename)
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


def get_all_data(client_connection: socket.socket, address) -> bytes:
    buffer = b''
    while True:
        request_data = client_connection.recv(BUFFER_SZ)
        if not request_data:
            server_logger.info(f'{address}  Client sent:  {len(buffer)}  bytes worth of data')
            return buffer
        buffer += request_data


def serve_client(client_connection: socket.socket, address):
    message_data = get_all_data(client_connection, address)
    client_connection.close()
    dc_message = json.loads(message_data)
    if not data_validation(dc_message):
        print('invalid format')
        server_logger.info('Invalid data')
    else:
        print('valid format')
        server_logger.info('Valid format')
        directory_name = 'time-' + str(date.today())
        file_name = 'user-' + str(dc_message['host'])
        p_path = os.path.join(LOG_FILE_PATH, 'TID', directory_name, file_name)
        create_file(p_path)
        encoded_message = json.dumps(dc_message['keys'])
        with open(p_path, mode='a') as f:
            f.write(f'{encoded_message}\n')


def start_server():
    # create the socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket on the ip
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    # if the number of connections exceeds CONNECTION_QUEUE_SIZE, they will be refused
    server_socket.listen(CONNECTION_QUEUE_SIZE)

    thread_pool = ThreadPoolExecutor(max_workers=10)

    while True:
        client_connection, address = server_socket.accept()
        print(f'Received connection from {address}')
        server_logger.info(f'Client connected to server {address}')
        thread_pool.submit(serve_client, client_connection, address)


def create_file(file_location):
    if not os.path.exists(file_location):
        p_path, f_name = os.path.split(file_location)
        os.makedirs(p_path, exist_ok=True)
        p_path = os.path.join(p_path, f_name)
        with open(p_path, mode='w'):
            print('Log file created')


def data_validation(data):
    if (len(data) == 2) & ('host' in data.keys()) & ('keys' in data.keys()):
        return True
    return False


if __name__ == '__main__':
    server_logger = create_logger(os.path.join(LOG_FILE_PATH, 'ServerLogs.txt'))
    start_server()
