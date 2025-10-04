'''
Currently, this web server handles only one HTTP request at a time which in
practice is not efficient for handling multiple connections but it gives us a
starting point for looking at the HTTP protocol.
'''

# Import socket module
from socket import *

import sys                                  # In order to terminate the program
import getopt                               # for processsing of args from cmd
import os                                   # file API <-allows you to acess
                                            # the file system
import re                                   # regular expression library
                                            # <- handy for string processing
from datetime import datetime, timedelta    # for managing times - Handy things


def main(argv):

    serverPort = 6789

    # Get the port number at start up, but will default to 6789
    try:
        opts, args = getopt.getopt(argv,"hp:",["port="])
    except getopt.GetoptError:
        print ('webserver.py -p <port number>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('webserver.py -p <port number>')
            sys.exit()
        elif opt in ("-p", "--port"):
            serverPort = int(arg)

    print('Server is running on port ', serverPort)

    # Create a TCP server socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_STREAM is used for TCP)
    # This sets up a TCP sockect
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Bind the socket to server address and server port
    serverSocket.bind(("", serverPort))

    # Listen to at most 1 connection at a time
    serverSocket.listen(1)

    # Server should be up and running and listening to the incoming connections
    # keep looping forever
    while True:
        print('The server is ready to receive data....')

        # Set up a new connection from the client
        connectionSocket, addr = serverSocket.accept()

        # If an exception occurs during the execution of try clause
        # the rest of the clause is skipped
        # If the exception type matches the word after except
        # the except clause is executed
        """
        Things to check:
            1. type of request - Is it supported or unsupported
            2. the resource that is being looked for
            3. the path (assuming that the root is in the same directory as the
            server)
            4. check the encoding type
            5. generate a response header with the correct information - You
            will need to think about the structure of what this need to be based
            on the requirements for the lab.
            6. send the response

        TIP:
            -check out what spilt() does to a Python string as you might find
            it useful.

        Remember:
            -The socket connections have been taken care of for you; all you
            need to concentrate on is the L5 protocol for HTTP.
        """
        try:
            # Receives the request message from the clientself.
            # It will wait until data has been recieved from client
            # The decode(encoding='UTF-8') ensurse that the data is interpreted
            # as ASCII
            message = connectionSocket.recv(1024).decode(encoding='UTF-8')
            # print the HTTP request type of message - for diagnoistics
            print(message)  # this should print out what was received from the
                            # client

            responseHeader = ""       # this is your empty response
            # Start your coding here!!



            request_method = message.split(' ')[0] # Get the request method (e.g., GET, POST)
            path = message.split(' ')[1]         # Get the requested file path
            print("Requested path:", path)  # just checking

            t_types = ['.html', '.htm', '.css', '.js', '.json'] #text types allowed
            b_types = ['.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf'] #binary types allowed

            # Only handle GET requests for this assignment
            if request_method != "GET":
                # Send HTTP response message for method not allowed (405)
                connectionSocket.send("HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode('UTF-8'))
                connectionSocket.send("<html><head></head><body><h1>405 Method Not Allowed</h1></body></html>\r\n".encode('UTF-8'))
                connectionSocket.close()
                return
            
            if path == "/":    # if nothing is specified after the /, return index.html
                path = "/index.html"  # Default to index.html if root is requested    

            filename = path.lstrip("/") #take off leadung /

            if os.path.isfile(filename):
                # Open and read the HTML file
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    body = f.read().encode('UTF-8')

                # Build simple HTTP 200 OK header
                responseHeader = "HTTP/1.1 200 OK\r\n"
                responseHeader += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
                responseHeader += "Server: Keirs_Server/1.0\r\n"
                responseHeader += "Content-Type: text/html\r\n"
                responseHeader += f"Content-Length: {len(body)}\r\n"
                responseHeader += "Connection: close\r\n\r\n"
                
                
                # Send header and body
                connectionSocket.send(responseHeader.encode('UTF-8'))
                connectionSocket.send(body)
                connectionSocket.close()

            else:
                # File not found → triggers your existing IOError block
                raise IOError
            
            # This line forces the application to through a IO exception
            # You will want to remove it, once you have tested your application

            # Things to do...
            # Extract the path of the requested object from the message
            # You will need to extract out the request method and the path
            # The first part of the HTTP header is the request method
            # The path is the second part of HTTP header - You will need to do
            # further processing on the path to check the criteria of what is
            # permitted, etc
            # IMPORTANT:  Start with the most basic request for index.html



            # Check the type of file being requested....
            # you will need to get the type of filename so you can set the
            # correct mime encoding type


            # if this is a binary file (ie png, jpg, pdf) is must be encoded for
            # proper transfer and you need to think about the length....


            #once everything is done, send the response header back
          

            # Send the content of the requested file to the connection socket

            #send something else to indicate the end of the response header

            # Close the client connection socket
     

        except IOError:
                # Send HTTP response message for file not found
                # this will always need to be run, if a file can't be Found
                # assuming it is a valid type
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode(encoding='UTF-8'))
                connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode(encoding='UTF-8'))
                # Close the client connection socket
                connectionSocket.close()


    serverSocket.close()
    # Terminate the program after sending the corresponding data
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
