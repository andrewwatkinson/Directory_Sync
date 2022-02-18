# Directory Sync
Python based solution for directory synchronisation over IP

## Installation

To use this Client-Server System you will need to be running python version 3 or later.

* To use this system please transfer the Client directory to the system that contains
the source directory that you wish to monitor

* following this place the Server directory into another system with a destination directory
that you want the source to transfer files too

## Usage

Both scripts are designed to be run via a command-line interface. Each can be quired
for information on required arguments as seen below
#### Client Help output
```
>python start_client.py -h
usage: start_client.py [-h] [--host HOST] [--p P] directory

Client program to send files to server

positional arguments:
  directory    destination directory for file transfer

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  destination hostname or IP address
  --p P        destination port to connect on

```
If no host is provided then localhost is used for testing on internal transfers.

#### Server Help output
```
>python start_server.py -h
usage: start_server.py [-h] [--p P] [--s S] directory

Server Program to receive files from a client

positional arguments:
  directory   destination directory for file transfer

optional arguments:
  -h, --help  show this help message and exit
  --p P       port the server should listen on
  --s S       sensitivity of partial copy detection from 2 to 10 where higher is more sensitive

```

When Assigning a custom port please be sure this is consistent across both the server and the client
