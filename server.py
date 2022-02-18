import os
import hashlib
import socket
import pickle
from os.path import isfile, join, getsize, basename
from os import listdir


# static hash function to which will return the hash corresponding to a given file
def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as file:
        open_file = file.read()
        hasher.update(open_file)
    return hasher.hexdigest()


# static function that will split a file into temporary files and returns the hashes of these sliced files
def segment_hashes(filename, chunk_size):
    file_number = 1
    output_files = []
    with open(filename, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            with open(f'{filename}_{file_number}.temp', "wb") as chunk_file:
                chunk_file.write(chunk)
            output_files.append(f'{filename}_{file_number}.temp')
            file_number += 1
            chunk = f.read(chunk_size)
        output_hashes = [hash_file(file) for file in output_files]
        [os.remove(file) for file in output_files if os.path.exists(file)]
    return output_hashes


# Server object definition
class Server:

    # initial arguments
    def __init__(self, dir, port, sense):
        self.dir = dir
        self.port = port
        self.sense = sense
        self.host = "0.0.0.0"
        self.s = None
        self.cs = None
        self.current_hashes = None
        self.file_names = None

    # checks given directory's content and returns all file names present along with their respective hashes
    def check_directory(self):
        self.file_names = [f for f in listdir(self.dir) if isfile(join(self.dir, f))]
        self.current_hashes = [hash_file(join(self.dir, f)) for f in self.file_names]

    # attempts to connect to client and proceeds to either accept a new file or send relevant data for
    # partial copy detection
    def receive_server(self):
        buffer_size, address = self.listen()
        received = self.cs.recv(buffer_size)
        try:
            overlapping = pickle.loads(received)
            seg_files = []
            for file in overlapping:
                size = getsize(file)
                seg_files.append([segment_hashes(file, size // self.sense), size])
            encode_seg_files = pickle.dumps(seg_files)
            self.cs.send(encode_seg_files)
        except pickle.UnpicklingError:
            filename = basename(received.decode())
            with open(join(self.dir, filename), "wb") as f:
                while True:
                    bytes_read = self.cs.recv(buffer_size)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                f.close()
                print(f"{filename} has been transferred")
            self.cs.close()

    # instantiate listening service on the provided port, returning connection details on successful connection
    def listen(self):
        buffer_size = 4096
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        self.cs, address = self.s.accept()
        return buffer_size, address

    # sends a given variable to client
    def send_variable(self, v):
        self.cs.send(pickle.dumps(v))

    # retrieves hashes from check_directory function and sends filenames and hashes to client
    def send_starting_variables(self):
        self.check_directory()
        print(f"[*] Listening as {self.host}:{self.port}")
        buffer_size, address = self.listen()
        print(f"[+] {address} is connected.")
        self.send_variable(self.current_hashes)
        self.send_variable(self.file_names)
        self.send_variable(self.sense)
        self.cs.close()
        self.s.close()
