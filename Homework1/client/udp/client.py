import socket
import time

from settings import *
from utils import get_byte_data, get_message, generate_message_block


def stream_send_file(sock, server_address, message_block, file_size):
    messages_sent = 0
    bytes_sent = 0
    start_transmission = time.time()

    print("Stream a file of size:{}".format(file_size))
    print("Message block:{}".format(message_block))

    while file_size > 0:
        if message_block <= file_size:
            size = message_block
        else:
            size = file_size

        message = generate_message_block(size).encode("utf-8")
        print(message)
        sock.sendto(message, server_address)

        print("Remains {} bytes to transfer".format(file_size))
        messages_sent += 1
        bytes_sent += size
        file_size -= size

        # time.sleep(1)

    print("File was sent")

    transmission_duration = time.time() - start_transmission
    print("Transmission duration: {}".format(transmission_duration))
    print("Number of sent messages: {}".format(messages_sent))
    print("Number of sent bytes: {}".format(bytes_sent))


def stop_and_wait_send_file(sock, server_address, message_block, file_size):
    print("Stop and wait a file of size:{}".format(file_size))
    print("Message block:{}".format(message_block))

    start_transmission = time.time()
    bytes_sent = 0
    messages_sent = 0

    while file_size > 0:
        if MESSAGE_BLOCK < file_size:
            size = message_block
        else:
            size = file_size

        message = generate_message_block(size).encode("utf-8")
        print(message)
        sock.sendto(message, server_address)

        while True:
            print("Waiting for ACK from Server")

            sock.settimeout(TIMEOUT_TIME)
            try:
                ack, address = sock.recvfrom(8)
                ack = get_message("q", ack)
                print("ACK: {}".format(ack))
            except Exception as err:
                print(err)
                print("Didn't received the AKC from server. Resend the block of message")
                sock.sendto(message, server_address)
            else:
                sock.settimeout(0)
                break

        messages_sent += 1
        bytes_sent += size
        file_size -= size
        print("Remains {} bytes to transfer".format(file_size))

        # time.sleep(1)

    print("File was sent")

    transmission_duration = time.time() - start_transmission
    print("Transmission duration: {}".format(transmission_duration))
    print("Number of sent messages: {}".format(messages_sent))
    print("Number of sent bytes: {}".format(bytes_sent))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP_ADDRESS, UDP_PORT)

    sock.sendto("ping".encode("utf-8"), server_address)
    new_port, address = sock.recvfrom(2)
    new_port = get_message("H", new_port)
    print("New port:{}".format(new_port))

    # Send to Server ACK that the new port was received
    print("Send to Server ACK that the new port was received")
    sock.sendto("ok".encode("utf-8"), server_address)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_address = (IP_ADDRESS, new_port)

    option = STOP_AND_WAIT_OPTION
    option_bytes = get_byte_data("i", option)
    print("Send to Server the option:{}".format(option))
    client_socket.sendto(option_bytes, client_address)
    time.sleep(0.5)

    file_size = 10 * ONE_MEGABYTE
    file_bytes_size = get_byte_data("q", file_size)
    print(len(file_bytes_size))
    print("Send to Server the file size:{}".format(file_size))
    client_socket.sendto(file_bytes_size, client_address)

    print("Waiting to receive the message block")
    message_block, _ = client_socket.recvfrom(2)
    message_block = get_message("H", message_block)
    print(message_block)

    if option == STREAMING_OPTION:
        stream_send_file(client_socket, client_address, message_block, file_size)
    else:
        stop_and_wait_send_file(client_socket, client_address, message_block, file_size)


if __name__ == '__main__':
    main()
