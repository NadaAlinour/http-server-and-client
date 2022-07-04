import socket
import os.path
import types
from os import path
import threading
import time


HOST = "127.0.0.1"
PORT = 80

errMsg = 'HTTP/1.1 404 Not Found\r\n\r\n'
okMsg = 'HTTP/1.1 200 OK\r\n\r\n'


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", addr)

    # messages logic here
    def run(self):

        while True:
            data = self.csocket.recv(2048)

            if not data:
                break

            # data received is the http request in bytes, convert to string and parse
            req_pckt = data.decode('utf-8')
            # print received command
            print(req_pckt)

            # get command and filename
            req_pckt_list = req_pckt.split(" ")
            command = req_pckt_list[0]
            filename = req_pckt_list[1]

            filename2 = filename[1:]

            if command == 'GET':

                # check if file exists
                if path.exists(filename2):
                    # found: read file, construct pckt
                    # "HTTP/1.0 200 OK\r\n\r\n\file-contents"
                    print('File found\n')
                    f = open(filename2, 'r')
                    file_contents = f.read()
                    f.close()
                    respMsg = okMsg + file_contents + '\r\n'
                    data = respMsg.encode('utf-8')

                else:
                    print('File not found\n')
                    data = errMsg.encode('utf-8')

            if command == 'POST':
                # get payload (after two break lines in string packet), decode and write into file and send ok msg
                req_pckt_list2 = req_pckt.split('\r\n\r\n')
                # display the file
                file_contents = req_pckt_list2[1]
                print("File contents to be uploaded: ", file_contents)
                # write into file and store in directory
                f = open('uploadedFile.txt', 'w')
                f.write(file_contents)
                f.close()
                data = okMsg.encode('utf-8')

            self.csocket.sendall(data)

            # persistent connection
            print("Waiting for another request..\n")
            time.sleep(10)

        # close connection
        print("connection closed by : ", addr)
        self.csocket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server started..")
    print("Waiting for client request..")
    s.listen()
    while True:
        conn, addr = s.accept()
        newthread = ClientThread(addr, conn)
        newthread.start()


