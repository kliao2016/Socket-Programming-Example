Kevin Liao: kliao2016@gmail.com

CS 3251-B, Programming Assignment 1: Due September 24, 2018

Instructions for compiling and running client and server programs: (Note that the server should be run first)
- Client: (Code written in python 3.6.x)
    - Use the command python3 rmtcalc.py [transport type] [server name] [port number]
        - Transport type is either TCP or UDP
        - Server name is any valid server name or IPv4 address (code will find the proper IPv4
          address if a server name is used)
        - Port number is a valid port number (i.e. 13001)
- Server: (Code written in python 3.6.x)
    - Use the command python3 rmtcalc-srv.py [transport type] [port number]
        - Transport type is either TCP or UDP
        - Port number is a valid port number (i.e. 13001)

Known Limitations:
- All code assumes an input of the following format in the client:
    - [number] [operand] [number] where there are spaces between each element
- All code assumes that parameters given when running the program are valid
- Client assumes if there is no error message contained in server response, then the returned number is valid and thus just has to be printed without needing to cast to float or do any other checking
- Server needs client message to be 33 bytes long
- Client needs server response to be a total of 48 bytes long regardless of how long the success or error message is
