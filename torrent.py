import bencoding
from hashlib import sha1

class Torrent():
    def __init__(self):
        with open('ubuntu.torrent', 'rb') as file:
            torrent_meta = file.read()
            self._meta_info = bencoding.Decode(torrent_meta).decode()
    
    def get_name(self):
        return self._meta_info[b'info'][b'name']

    def get_announce(self):
        return self._meta_info[b'announce']

    def get_info_hash(self):
        digest = sha1(bencoding.Encode().encode(self._meta_info[b'info'])).digest()
        hexdigest = sha1(bencoding.Encode().encode(self._meta_info[b'info'])).hexdigest()
        print(hexdigest)
        return digest

    def get_piece_length(self):
        return self._meta_info[b'info'][b'piece length']

    def get_pieces(self):
        data = self._meta_info[b'info'][b'pieces']
        offset = 0
        pieces = []
        while offset < len(data):
            pieces.append(data[offset:offset + 20])
            offset += 20

        return pieces

    def is_multi_file(self) -> bool:
        return b'files' in self._meta_info[b'info']

    def get_created_by(self):
        return self._meta_info[b'created by']

    def __str__(self) -> str:
        return 'File Name: {0} \n' \
        'Created By: {1} \n' \
        'Info Hash: {2} \n' \
        'Pieces: {3} \n'.format(self.get_name(), self.get_created_by(), self.get_info_hash, self.get_pieces)
    