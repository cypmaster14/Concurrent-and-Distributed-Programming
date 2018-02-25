import socket
import time

from settings import *
from utils import get_byte_data, get_message


def stream_send_file(sock, server_address, message_block, file_size):
    message_sent = 0
    bytes_send = 0
    start_transimision = time.time()

    print("Stream a file of size:{}".format(file_size))
    print("Message block:{}".format(message_block))


def stop_and_wait_send_file(sock, server_address, message_block, file_size):
    pass


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP_ADDRESS, UDP_PORT)

    sock.sendto("ping".encode("utf-8"), server_address)

    new_port, address = sock.recvfrom(2)
    new_port = get_message("H", new_port)
    print("New port:{}".format(new_port))

    sock.sendto("0".encode("utf-8"), server_address)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
    client_server_address = (address[0], new_port)

    print(address, client_server_address)

    client_socket.bind(client_server_address)
    print(client_server_address)

    option = STREAMING_OPTION
    option_bytes = get_byte_data("i", option)
    print("Send to server the option:{}".format(option))
    client_socket.sendto(option_bytes, client_server_address)

    file_size = 50 * ONE_KILOBYTE
    file_size_bytes = get_byte_data("q", file_size)
    print("Send to server the file size:{}".format(file_size))
    client_socket.sendto(file_size_bytes, client_server_address)

    print(client_socket)

    message_block, client_server_address = client_socket.recvfrom(2)
    message_block = get_message("h", message_block)
    print("Server will accept blocks of size:{}".format(message_block))

    if option_bytes == STREAMING_OPTION:
        stream_send_file(client_socket, client_server_address, message_block, file_size)
    else:
        stop_and_wait_send_file(client_socket, client_server_address, message_block, file_size)


if __name__ == '__main__':
    main()
