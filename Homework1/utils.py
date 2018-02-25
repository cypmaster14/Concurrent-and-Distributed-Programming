import string
import struct
from multiprocessing import Queue
from random import *

def get_byte_data(message_format, message):
    return struct.pack(message_format, message)


def get_message(message_format, message):
    return struct.unpack(message_format, message)[0]


def generate_message_block(size):
    all_characters = string.ascii_letters + string.punctuation + string.digits
    message_block = "".join(choice(all_characters) for _ in range(size))
    return message_block
