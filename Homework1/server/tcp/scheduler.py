from multiprocessing import Queue

from request_handler import RequestHandler

global clients_queue


class Scheduler(object):

    def __init__(self):
        pass

    def start(self):
        global clients_queue
        print("Waiting for clients")
        while True:
            client_connection = clients_queue.get(block=True)
            print("Schedule client request")
            request_handler = RequestHandler(client_connection)
            request_handler.start()


if __name__ == '__main__':
    global clients_queue
    clients_queue = Queue()
    scheduler = Scheduler()
    scheduler.start()
