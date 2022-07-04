import socket

input_file_name = 'commands.txt'


class CommandObj:
    def __init__(self, command, filename, host, port):
        self.command = command
        self.filename = filename
        self.host = host
        self.port = port


# function to change input command to http request msg
def construct_http_req_pckt(command_item):
    if command_item.command == 'GET':
        http_string_pckt = command_item.command + ' ' + command_item.filename + ' HTTP/1.1\r\nHost: ' + command_item.host + ':' + command_item.port + '\r\n\r\n'

    if command_item.command == 'POST':
        f = open(command_item.filename[1:], 'r')
        file_contents = f.read()
        f.close()
        http_string_pckt = command_item.command + ' ' + command_item.filename + ' HTTP/1.1\r\nHost: ' + command_item.host + ':' + command_item.port + '\r\n\r\n' + file_contents + '\r\n'

    return http_string_pckt


commandList = []

f = open(input_file_name).readlines()
for line in f:
    row = line.split(' ')
    # if port number not specified, assume it is 80
    if len(row) == 3:
        row.append("80")
    command, filename, host, port = [i.strip() for i in row]
    commandObj = CommandObj(command, filename, host, port)
    commandList = commandList + [commandObj]

i = 0
# make new TCP connection for each command
while i < len(commandList):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((commandList[i].host, int(commandList[i].port)))

        req_pckt = construct_http_req_pckt(commandList[i])
        print(req_pckt)

        # convert from string to bytes and send data to server
        s.sendall(req_pckt.encode('utf-8'))

        data = s.recv(1024)

        resp_pckt = data.decode('utf-8')
        print(resp_pckt)

        if commandList[i].command == 'GET':
            resp_pckt_list = resp_pckt.split()

            if resp_pckt_list[1] == '200':
                resp_pckt_list2 = resp_pckt.split('\r\n\r\n')
                file_contents = resp_pckt_list2[1]

                # write into file and save in directory
                f = open('requestedFile.txt', 'w')
                f.write(file_contents)
                f.close()
    i += 1
