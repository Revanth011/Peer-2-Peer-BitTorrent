'''
Bytes in Python are represented as sequences of integers (each in the range 0 to 255)
Parsing the .torrent file
Connecting to the tracker

info - 
    - length
    - name
    - piece length
    - pieces


    
'''

from collections import OrderedDict
from hashlib import sha1
import json

class Decode():
    TOKEN_INT = b'i'
    TOKEN_LIST = b'l'
    TOKEN_DICT = b'd'
    TOKEN_END = b'e'
    TOKEN_STRING_COLON = b':'

    def __init__(self, data) -> None:
        self.index = 0
        self.data = data

    def decode(self):

        byte_char = self.data[self.index : self.index + 1]

        if byte_char is None:
            raise EOFError('Unexpected end-of-file')
        if byte_char == self.TOKEN_INT:
            return self.decode_integer()
        elif byte_char in b'0123456789':
            return self.decode_string()
        elif byte_char == self.TOKEN_LIST:
            return self.decode_list()
        elif byte_char == self.TOKEN_DICT:
            return self.decode_dictionary()

    def decode_dictionary(self) -> bytes:
        dict = OrderedDict()
        self.index += 1

        while self.data[self.index : self.index + 1] != self.TOKEN_END:
            key = self.decode()
            self.index += 1
            value = self.decode()

            dict[key] = value
            self.index += 1
        
        return dict
    
    def decode_string(self) -> bytes:
        colon_i = self.data.index(self.TOKEN_STRING_COLON, self.index)
        str_len = self.data[self.index : colon_i]
        str_byte = self.data[colon_i + 1 : colon_i + 1 + int(str_len)]

        self.index = colon_i + int(str_len)
        return str_byte

    def decode_integer(self) -> int:
        self.index += 1
        byte_int = b''
        while self.data[self.index : self.index + 1] != self.TOKEN_END:
            byte_int += self.data[self.index : self.index + 1]
            self.index += 1
        
        return int(byte_int)
        
    def decode_list(self) -> bytes:
        self.index += 1
        list_bytes = []
        while self.data[self.index : self.index + 1] != self.TOKEN_END:
            list_bytes.append(self.decode())
            self.index += 1
        return list_bytes
    
class Encode():

    def encode(self, data):
        self.data = data
        if type(self.data) == str:
            return self._encode_string(data)
        elif type(self.data) == int:
            return self._encode_int(data)
        elif type(self.data) == list:
            return self._enocode_list(data)
        elif type(self.data) == bytes:
            return self._encode_bytes(data)
        elif type(self.data) == dict or type(data) == OrderedDict:
            return self._encode_dict(data)
        else:
            return None

    def _encode_int(self, value) -> bytes:
        return str.encode('i' + str(value) + 'e')
    
    def _encode_string(self, value) -> bytes:
        return str.encode(str(len(value)) + ":" + value)
    
    def _enocode_list(self, list) -> bytes:
        result = b'l'
        result += b''.join([ self.encode(val) for val in list])
        result += b'e'
        return result
    
    def _encode_bytes(self, data) -> bytes:
        result = str.encode(str(len(data)))
        result += b':'
        result += data
        return result
    
    def _encode_dict(self, dict) -> bytes:
        result = b'd'
        for k ,v in dict.items():
            key = self.encode(k)
            val = self.encode(v)

            result += key + val
        result += b'e'
        return result


if __name__ == "__main__" :

    with open('ubuntu.torrent', 'rb') as file:
        torrent_meta = file.read()
        
        # decoded_data = Decode(torrent_meta).decode()
        # encoded_data = Encode().encode(decoded_data)

        # print(encoded_data)
