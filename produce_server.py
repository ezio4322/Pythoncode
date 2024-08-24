import socket
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor

pages_path = '/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/accessible'


CONNECTION_QUEUE_SIZE = 10
BUFFER_SZ = 1024


SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8080


def serve_client(client_connection: socket.socket):
    request_data = client_connection.recv(1024).decode()
    request_lines = request_data.split('\n')
    first_line_list = request_lines[0].split()
    http_method = first_line_list[0]
    path = first_line_list[1][1:]
    if http_method == 'GET':
        if os.path.isfile(os.path.join(pages_path, path)):
            response = 'HTTP/1.1 200 OK\n\n' + existing_page(path)
        elif path[:6] == 'adding':
            response = 'HTTP/1.1 200 OK\n\n' + product_submitted()
            validate_product(path[6:])
        else:
            response = 'HTTP/1.1 404 Page Not Found\n\n' + page_not_found()
    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET' + method_not_allowed()
    client_connection.sendall(response.encode())
    client_connection.close()
    print('connection closed')


def existing_page(path):
    with open(os.path.join(pages_path, path)) as f:
        content = f.read()
    return content


def page_not_found():
    with open('/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/not_found.html') as f:
        content = f.read()
    return content


def method_not_allowed():
    with open('/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/not_allowed.html') as f:
        content = f.read()
    return content


def product_submitted():
    with open('/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/format_submitted.html') as f:
        content = f.read()
    return content


def timeout(client_connection: socket.socket):
    time.sleep(3)
    request_data = client_connection.recv(1024).decode()
    if request_data[:23] != '<socket.socket [closed]':
        with open('/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/gateway_timeout.html') as f:
            content = f.read()
        response = 'HTTP/1.1 504 Gateway Timeout\n\n' + content
        client_connection.sendall(response.encode())
        client_connection.close()


def validate_product(path):
    if path[0] != '?':
        return
    segments = path[1:].split('&')
    if len(segments) != 3:
        return
    name = segments[0].split('=')
    price = segments[1].split('=')
    count = segments[2].split('=')
    if (len(name) != 2) | (len(price) != 2) | (len(count) != 2):
        return
    if (name[0] != 'pname') | (price[0] != 'price') | (count[0] != 'count'):
        return
    if not count[1].isnumeric():
        return
    name[1] = name[1].replace('+', ' ')
    price[1] = price[1].replace('+', ' ')
    new_element = {'pname': name[1], 'price': price[1], 'count': count[1]}
    with open('/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/json_products', mode='a') as f:
        f.write(f'{json.dumps(new_element)}\n')
    with open('/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/products_html', mode='a') as f:
        f.write(f'  <tr>\n   <td>{name[1]}</td>\n    <td>{price[1]}</td>\n   <td>{count[1]}</td>\n  </tr>\n')
    with open('/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/products_html', mode='r') as f:
        content = f.read()
    with open('/home/cosmin/Desktop/pyth/projects/pyPJ1/server_stuff/accessible/pages/products.html', mode='w') as f:
        f.write(f'{content}\n</table>\n\n</body>\n</html>')


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen(CONNECTION_QUEUE_SIZE)

    thread_pool = ThreadPoolExecutor(max_workers=10)

    while True:
        client_connection, address = server_socket.accept()
        print(f'Received connection from {address}')
        thread_pool.submit(serve_client, client_connection)
        thread_pool.submit(timeout, client_connection)


if __name__ == '__main__':
    start_server()
