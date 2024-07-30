import socket
import threading

from concurrent.futures import ThreadPoolExecutor
CONNECTION_QUEUE_SIZE = 10
BUFFER_SZ = 1024


SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8080


def get_all_data(client_connection: socket.socket) -> bytes:
    # todo: check how much data did the client send
    buffer = b''
    while True:
        request_data = client_connection.recv(BUFFER_SZ)
        if not request_data:
            # no more data to read
            return buffer
        buffer += request_data


def serve_client(client_connection: socket.socket):
    message_data = get_all_data(client_connection)
    # after getting all the data, close the connection
    client_connection.close()
    print(f'Received from client: {message_data}')
    # todo: process the data / save it


def start_server():
    # create the socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket on the ip
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    # if the number of connections exceeds CONNECTION_QUEUE_SIZE, they will be refused
    server_socket.listen(CONNECTION_QUEUE_SIZE)

    thread_pool = ThreadPoolExecutor(max_workers=5)

    while True:
        client_connection, address = server_socket.accept()
        print(f'Received connection from {address}')
        thread_pool.submit(serve_client, client_connection)


if __name__ == '__main__':
    start_server()
