# Directory Sync
Python based solution for directory synchronisation over IP
* Time spent on project so far 5.5 hours

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

When Assigning a custom port please be sure this is consistent across both the server and the client.

The Sensitivity setting is used to dictate the number of segments that are checked
to efficiently detect whether a file is partially similar to a file already in the
destination directory. Larger values may decrease speed of execution with very large files.

## Current Features
* Detection of new files in source and subsequent transfer of these files
* Multiple transfers of the same files is prevented using a hashing based method with hash algorithm chosen to reduce likelihood of collision errors
* partial file similarity detection (with limitations discussed below)

## Shortcomings / Features to add
### Shortcomings
* sub-directories are not accounted for in the source directory, therefore, all files are copied
to the root of the of the destination directory
* partial file similarity checking uses segmented files for hash comparison, this
leads to the potential for missed instances of similarity where data is added at the beginning of a file, thus changing all following hash values and providing a false positive

### Features to add
* Add ability to replicate sub directories that are present in source folder when transferred to Server
* Allow for detection of easy to parse text files for more accurate partial similarity detection in these instances
