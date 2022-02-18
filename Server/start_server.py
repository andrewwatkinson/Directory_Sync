import argparse as ap
from server import Server


# function to retrieve command line input and provide a help prompt if needed
def get_args():
    parser = ap.ArgumentParser(description='Server Program to receive files from a client')
    parser.add_argument("directory", help="destination directory for file transfer", type=str)
    parser.add_argument("--p", help="port the server should listen on", type=int)
    parser.add_argument("--s", help="sensitivity of partial copy detection from 2 to 10 where higher is more sensitive", type=int)
    args = parser.parse_args()
    directory = args.directory
    # create default inputs for optional arguments
    if args.p:
        p = args.p
    else:
        p = 5001
    if args.s:
        se = args.s
    else:
        se = 2
    return directory, p, se


if __name__ == "__main__":
    # try accept used to allow for graceful shutdown of server
    try:
        direc, port, sense = get_args()
        s = Server(direc, port, sense)
        s.send_starting_variables()
        while True:
            s.receive_server()
    except KeyboardInterrupt:
        print("Server Stopping")
