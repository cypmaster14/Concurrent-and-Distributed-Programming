import socket
import threading

import time

from settings import *
from utils import get_byte_data, get_message


class RequestHandler(threading.Thread):

    def __init__(self, socket_descriptor: socket.socket, address):
        super().__init__()
        self.socket_descriptor = socket_descriptor
        self.address = address
        print("Client Address:{}".format(self.address))

    def stream_message(self, total_message_size):
        print("Receive a file of size:{}".format(total_message_size))
        print("Message block:{}".format(MESSAGE_BLOCK))

        messages_received = 0
        bytes_received = 0
        with open(FILE_NAME_UDP, mode="wb") as file_object:
            while True:
                message, _ = self.socket_descriptor.recvfrom(MESSAGE_BLOCK)
                if not message:
                    break

                file_object.write(message)
                print("Received {} bytes".format(len(message)))

                messages_received += 1
                bytes_received += len(message)
                if len(message) != MESSAGE_BLOCK:
                    break

                # time.sleep(1)

        print("File was received")

        self.socket_descriptor.close()

        print("Protocol: UDP")
        print("Number of messages read: {}".format(messages_received))
        print("Number of bytes received: {}".format(bytes_received))

    def stop_and_wait(self, total_message_size):
        print("Stop and wait a file of size:{}".format(total_message_size))
        print("Message block:{}".format(MESSAGE_BLOCK))

        messages_received = 0
        bytes_received = 0
        with open(FILE_NAME_UDP, mode="wb") as file_object:
            while True:
                self.socket_descriptor.settimeout(TIMEOUT_TIME + 1.0)
                try:
                    message, address = self.socket_descriptor.recvfrom(MESSAGE_BLOCK)
                except Exception as err:
                    print(err)
                    continue
                else:
                    self.socket_descriptor.settimeout(0)

                if not message:
                    self.socket_descriptor.settimeout(TIMEOUT_TIME + 1.0)
                    break

                file_object.write(message)
                print("Received {} bytes".format(len(message)))

                # Send ACK to Client
                messages_received += 1
                bytes_received += len(message)
                ack = bytes_received + 1
                ack_bytes = get_byte_data("q", ack)
                print("Send ACK: {} to client".format(ack))
                self.socket_descriptor.sendto(ack_bytes, address)

                if len(message) != MESSAGE_BLOCK:
                    break

                # time.sleep(1)

        print("File was received")
        self.socket_descriptor.close()

        print("Protocol: UDP")
        print("Number of messages read: {}".format(messages_received))
        print("Number of bytes received: {}".format(bytes_received))

    def run(self):
        print("Handling client requests")

        option, address = self.socket_descriptor.recvfrom(4)
        self.address = address
        option = get_message("i", option)
        print("Option:{}".format(option))

        requested_message_size, _ = self.socket_descriptor.recvfrom(8)
        requested_message_size = get_message("q", requested_message_size)
        print("Requested message size:{}".format(requested_message_size))

        message_block_size_bytes = get_byte_data("H", MESSAGE_BLOCK)
        print("Sending to client the message block size.")
        time.sleep(0.5)
        self.socket_descriptor.sendto(message_block_size_bytes, self.address)

        if option == STREAMING_OPTION:
            self.stream_message(requested_message_size)
        else:
            self.stop_and_wait(requested_message_size)
