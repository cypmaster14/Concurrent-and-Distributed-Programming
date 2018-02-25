import socket

from request_handler import RequestHandler
from settings import IP_ADDRESS, TCP_PORT


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP_ADDRESS, TCP_PORT))
    sock.listen(1)

    print("Waiting for connections at: {}:{}".format(IP_ADDRESS, TCP_PORT))
    while True:
        (connection, address) = sock.accept()
        print(connection)
        print("Client connected:", address)
        request_handler = RequestHandler(connection)
        request_handler.start()


if __name__ == '__main__':
    main()
