from os import listdir, remove
import socket
import pickle
from os.path import isfile, join, basename, exists
import hashlib


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
        [remove(file) for file in output_files if exists(file)]
    return output_hashes


# Client object definition
class Client:

    # initial arguments
    def __init__(self, port, host, directory):
        self.host = host
        self.port = port
        self.directory = directory
        self.s = None
        self.current_hashes = None
        self.file_names = None
        self.files_to_send = None
        self.sense = None

    # sends a given variable to client
    def send_variable(self, v):
        self.s.send(pickle.dumps(v))

    def flag_partial(self, shared_names):
        files = [basename(i) for i in shared_names]
        self.connect()
        self.send_variable(files)
        encoded_hashes_sizes = self.s.recv(4096)
        segment_hashes = pickle.loads(encoded_hashes_sizes)
        self.files_to_send = self.partial_check(shared_names, segment_hashes)
        if len(self.files_to_send) > 0:
            self.send_file_list()
        self.s.close()

    def check_directory(self):
        files = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        all_hashes = [hash_file(join(self.directory, f)) for f in files]
        self.files_to_send = [join(self.directory, files[i]) for i in range(len(files)) if all_hashes[i] not in self.current_hashes]
        [self.current_hashes.append(hash_file(join(self.directory, f))) for f in self.files_to_send]

    # check whether a segmented file contains any overlap with the like file on the server
    def partial_check(self, filenames, server_seg_hashes):
        partials = []
        chunks = [i[1] for i in server_seg_hashes]
        for i in range(len(filenames)):
            seg_hashes = segment_hashes(filenames[i], chunks[i] // self.sense)
            overlap = False
            for h in server_seg_hashes[i][0]:
                if h in seg_hashes:
                    overlap = True
                else:
                    continue
            partials.append(overlap)
        return [filenames[i] for i in range(len(filenames)) if not partials[i]]

    #
    def connect(self):
        self.s = socket.socket()
        self.s.connect((self.host, self.port))

    # send all files in a list to the server using the send_file method
    def send_file_list(self):
        for i in self.files_to_send:
            self.send_file(i)

    # connect to server and send a given file as a byte stream
    def send_file(self, file):
        num_retries = 5
        for i in range(num_retries):
            try:
                self.connect()
                buffer_size = 4096
                self.s.send(f"{file}".encode())
                with open(file, "rb") as f:
                    while True:
                        bytes_read = f.read(buffer_size)
                        if not bytes_read:
                            break
                        self.s.sendall(bytes_read)
                    f.close()
                print(f"{file} has been transferred")
                self.s.close()
                break
            except ConnectionResetError:
                continue

    # retrieve hashes and file names of server directory
    def retrieve_starting_variables(self):
        self.connect()
        self.current_hashes = pickle.loads(self.s.recv(4096))
        self.file_names = pickle.loads(self.s.recv(4096))
        self.sense = pickle.loads(self.s.recv(4096))
        self.s.close()
