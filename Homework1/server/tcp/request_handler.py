import socket
import threading
import time

from settings import *
from utils import get_byte_data, get_message, generate_message_block


class RequestHandler(threading.Thread):
    def __init__(self, socket_descriptor: socket.socket):
        threading.Thread.__init__(self)
        self.socket_descriptor = socket_descriptor

    def stream_message(self, total_message_size):
        print("Receive a file of size:{}".format(total_message_size))
        print("Message block:{}".format(MESSAGE_BLOCK))

        messages_received = 0
        bytes_received = 0
        with open(FILE_NAME, mode="wb") as file_object:
            while True:
                message = self.socket_descriptor.recv(MESSAGE_BLOCK)
                if not message:
                    break

                file_object.write(message)
                print("Received {} bytes".format(len(message)))

                messages_received += 1
                bytes_received += len(message)
                time.sleep(1)

        print("File was received")
        self.socket_descriptor.close()

        print("Protocol: TCP")
        print("Number of messages read: {}".format(messages_received))
        print("Number of bytes received: {}".format(bytes_received))

    def stop_and_wait(self, total_message_size):
        print("Stop and wait a file of size:{}".format(total_message_size))
        print("Message block:{}".format(MESSAGE_BLOCK))

        messages_received = 0
        bytes_received = 0
        with open(FILE_NAME, mode="wb") as file_object:
            while True:
                message = self.socket_descriptor.recv(MESSAGE_BLOCK)
                if not message:
                    break

                file_object.write(message)
                print("Received {} bytes".format(len(message)))

                # Send ACK to Client
                messages_received += 1
                bytes_received += len(message)
                ack = bytes_received + 1
                ack_bytes = get_byte_data("q", ack)
                print("Send ACK: {} to client".format(ack))
                self.socket_descriptor.send(ack_bytes)

                time.sleep(1)

        print("File was received")
        self.socket_descriptor.close()

        print("Protocol: TCP")
        print("Number of messages read: {}".format(messages_received))
        print("Number of bytes received: {}".format(bytes_received))

    def run(self):
        print("Handling client request")

        option = self.socket_descriptor.recv(4)
        option = get_message("i", option)
        print("Option:{}".format(option))

        requested_message_size = self.socket_descriptor.recv(8)
        requested_message_size = get_message("q", requested_message_size)
        print("Requested message size:{}".format(requested_message_size))

        message_block_bytes = get_byte_data("h", MESSAGE_BLOCK)
        print("Sending to client the message block size.")
        self.socket_descriptor.send(message_block_bytes)

        if option == STREAMING_OPTION:
            self.stream_message(requested_message_size)
        else:
            self.stop_and_wait(requested_message_size)
