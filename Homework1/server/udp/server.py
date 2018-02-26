import socket
import random
from settings import *
from utils import get_byte_data
from request_handler import RequestHandler


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP_ADDRESS, UDP_PORT))

    print("Waiting clients at: {}:{}".format(IP_ADDRESS, UDP_PORT))
    while True:
        data, address = sock.recvfrom(4)
        print(data, address)

        # Send to the client the port for a new socket connection that will be served by the spawn thread
        client_port = random.randint(10000, 60000)
        print("Port for a new socket connection that will be served by the spawn thread :{}".format(client_port))
        client_port_bytes = get_byte_data("H", client_port)
        sock.sendto(client_port_bytes, address)

        client_address = (IP_ADDRESS, client_port)

        data, address = sock.recvfrom(2)
        print("Message received", data, address)
        print("Client received the new port")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind(client_address)
        request_handler = RequestHandler(client_socket, client_address)
        request_handler.start()


if __name__ == '__main__':
    main()
