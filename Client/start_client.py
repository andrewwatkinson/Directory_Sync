import argparse as ap
import os
from client import Client
from time import sleep

# function to retrieve command line input and provide a help prompt if needed
def get_args():
    parser = ap.ArgumentParser(description='Client program to send files to server')
    parser.add_argument("directory", help="destination directory for file transfer", type=str)
    parser.add_argument("--host", help="destination hostname or IP address", type=str)
    parser.add_argument("--p", help="destination port to connect on", type=str)
    args = parser.parse_args()
    if args.host:
        host = args.host
    else:
        host = "localhost"
    if args.p:
        port = args.p
    else:
        port = 5001

    return port, host, args.directory


if __name__ == '__main__':
    port, host, directory = get_args()
    c = Client(port, host, directory)
    # while loop to allow for safe restart of connect instead of error when remote system isn't responding
    while True:
        try:
            print("attempting to connect to server")
            c.retrieve_starting_variables()
            print("connection established\nPress Crtl+c to exit")
            # loop to continuously check directory and act should any changes occur
            while True:
                c.check_directory()
                if len(c.files_to_send) > 0:
                    shared_names = [i for i in c.files_to_send if os.path.basename(i) in c.file_names]
                    if len(shared_names) > 0:
                        c.flag_partial(shared_names)
                    else:
                        c.send_file_list()
                sleep(0.5)
        # exceptions to either catch common errors during loop
        except KeyboardInterrupt:
            print("Ending directory checking service")
            break
        except ConnectionRefusedError:
            print("Server is not running on remote system")
            if input("Do you wish to retry connection? y or n: ") == "y":
                continue
            else:
                print("service shutting down")
                break
        except ConnectionResetError:
            print("Connection closed by server")
            break
