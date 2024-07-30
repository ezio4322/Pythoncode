import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8080

if __name__ == '__main__':
    client_message = 'this is a simple message'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to a server
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    client_socket.send(client_message.encode())
    # close the connection
    client_socket.close()
