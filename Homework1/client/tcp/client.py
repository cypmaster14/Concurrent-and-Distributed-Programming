import socket
import time

from settings import *
from utils import get_byte_data, get_message, generate_message_block


def stream_send_file(sock: socket.socket, message_block: int, file_size: int):
    messages_sent = 0
    bytes_sent = 0
    start_transmission = time.time()

    print("Stream a file of size:{}".format(file_size))
    print("Message block:{}".format(message_block))

    with open(FIVE_HUNDRED_MB_FILE_LOCATION, mode="rb") as file_object:
        while True:
            message = file_object.read(message_block)
            if len(message) == 0:
                break

            sock.send(message)
            file_size -= len(message)
            print("Remains {} bytes to transfer".format(file_size))
            messages_sent += 1
            bytes_sent += len(message)

    # while file_size > 0:
    #     if message_block < file_size:
    #         size = message_block
    #     else:
    #         size = file_size
    #
    #     message = generate_message_block(size).encode("utf-8")
    #     # print(message)
    #     sock.send(message)
    #     file_size -= size
    #
    #     print("Remains {} bytes to transfer".format(file_size))
    #     messages_sent += 1
    #     bytes_sent += size
    #     # time.sleep(1)

    print("File was sent")
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    transmission_duration = time.time() - start_transmission
    print("Transmission duration: {}".format(transmission_duration))
    print("Number of sent messages: {}".format(messages_sent))
    print("Number of sent bytes: {}".format(bytes_sent))


def stop_and_wait_send_file(sock: socket.socket, message_block: int, file_size: int):
    print("Stop and wait a file of size:{}".format(file_size))
    print("Message block:{}".format(message_block))

    start_transmission = time.time()
    bytes_sent = 0
    messages_sent = 0

    with open(FIVE_HUNDRED_MB_FILE_LOCATION, mode="rb") as file_object:
        while True:
            message = file_object.read(message_block)
            if len(message) == 0:
                break

            sock.send(message)

            while True:
                print("Waiting for ACK from Server")

                sock.settimeout(TIMEOUT_TIME)
                try:
                    ack = sock.recv(8)
                    ack = get_message("q", ack)
                    print("ACK: {}".format(ack))
                except Exception as err:
                    print(err)
                    print("Didn't received the ACK from server. Resend the block of message")
                    sock.send(message)
                else:
                    sock.settimeout(0)
                    break

            messages_sent += 1
            bytes_sent += len(message)
            file_size -= len(message)
            print("Remains {} bytes to transfer".format(file_size))

    # while file_size > 0:
    #     if message_block < file_size:
    #         size = message_block
    #     else:
    #         size = file_size
    #
    #     message = generate_message_block(size).encode("utf-8")
    #     sock.send(message)
    #
    #     while True:
    #         print("Waiting for ACK from Server")
    #
    #         sock.settimeout(TIMEOUT_TIME)
    #         try:
    #             ack = sock.recv(8)
    #             ack = get_message("q", ack)
    #             print("ACK: {}".format(ack))
    #         except Exception as err:
    #             print(err)
    #             print("Didn't received the ACK from server. Resend the block of message")
    #             sock.send(message)
    #         else:
    #             sock.settimeout(0)
    #             break
    #
    #     messages_sent += 1
    #     bytes_sent += size
    #     file_size -= size
    #     print("Remains {} bytes to transfer".format(file_size))
    #
    #     # time.sleep(1)

    print("File was sent")
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    transmission_duration = time.time() - start_transmission
    print("Transmission duration: {}".format(transmission_duration))
    print("Number of sent messages: {}".format(messages_sent))
    print("Number of sent bytes: {}".format(bytes_sent))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP_ADDRESS, TCP_PORT))

    option = MECHANISM_OPTION
    option_bytes = get_byte_data("i", option)
    print("Send to server the option:{}".format(option))
    sock.send(option_bytes)

    file_size = FILE_SIZE
    requested_file_size_bytes = get_byte_data("q", file_size)
    print("Send to server the file size:{}".format(file_size))
    sock.send(requested_file_size_bytes)

    message_block = sock.recv(2)
    message_block = get_message("H", message_block)
    print("Server will accept blocks of size:{}".format(message_block))

    if option == STREAMING_OPTION:
        stream_send_file(sock, message_block, file_size)
    else:
        stop_and_wait_send_file(sock, message_block, file_size)


if __name__ == '__main__':
    main()
