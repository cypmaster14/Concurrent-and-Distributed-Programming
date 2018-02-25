import socket
import threading

from settings import *
from utils import get_byte_data, get_message


class RequestHandler(threading.Thread):

    def __init__(self, socket_descriptor: socket.socket, address):
        super().__init__()
        self.socket_descriptor = socket_descriptor
        self.address = address
        print("Client Address:{}".format(self.address))

    def stream_message(self, total_message_size):
        pass

    def stop_and_wait(self, total_message_size):
        pass

    def run(self):
        print("Handling client requests ")

        option, _ = self.socket_descriptor.recvfrom(4)
        option = get_message("i", option)
        print("Option:{}".format(option))

        requested_message_size, _ = self.socket_descriptor.recvfrom(8)
        requested_message_size = get_message("q", requested_message_size)
        print("Requested message size:{}".format(requested_message_size))

        message_block_size_bytes = get_byte_data("h", MESSAGE_BLOCK)
        print("Sending to client the message block size.")
        self.socket_descriptor.sendto(message_block_size_bytes, self.address)

        if option == STREAMING_OPTION:
            self.stream_message(requested_message_size)
        else:
            self.stop_and_wait(requested_message_size)
