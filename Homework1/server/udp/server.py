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
        data, address = sock.recvfrom(4)  # Ping
        print(data, address)

        # Send to the client the port for a new socket connection that will be served by the spawn thread
        client_port = random.randint(10000, 60000)
        print("Port for a new socket connection that will be served by the spawn thread :{}".format(client_port))
        client_port_bytes = get_byte_data("H", client_port)
        sock.sendto(client_port_bytes, address)

        # ACK for the new port
        data, address = sock.recvfrom(1)
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_sock.bind((address[0], client_port))
        print("Client received the new port")

        request_handler = RequestHandler(client_sock, (address[0], client_port))
        request_handler.start()


if __name__ == '__main__':
    main()
