from hashlib import sha256
from base64 import b64encode, b64decode
from json import  loads, dumps
from binascii import unhexlify

class Block:
    def __init__(self, data: bytes, previous_hash: bytes):
        self.data = data
        self.previous_hash = previous_hash
        self._sha256 = sha256(self.data + self.previous_hash)
        self.next = None

    def hash(self):
        return self._sha256.digest()

    def encode(self):
        
        data_dict = {
            'data': b64encode(self.data).decode('utf-8'),
            'previous': self.previous_hash.hex()
        }

        return dumps(data_dict)
    
    def append_next(self, next):
        self._next = next
        return self._next

    def __str__(self):
        return self.encode()

    @staticmethod
    def decode(b):
        data_dict = loads(b)
        data = b64decode(data_dict['data'])
        previos_hash = unhexlify(data_dict['previous'])

        return Block(data, previos_hash)

    @staticmethod
    def genesis_block(data: bytes):
        prev_hash = sha256((b'\x00' * 32)).digest()
        return Block(data, prev_hash)