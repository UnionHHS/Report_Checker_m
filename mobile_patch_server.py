import socket
import hashlib
import os
from threading import Thread

#version checker

def HASH_CHECKER():
    with open(f'mobile.exe', 'rb') as f:
        data = f.read()
    h = hashlib.sha256()
    h.update(data)
    hash_data = h.hexdigest()
    return hash_data

def hash_diff(hada, conn):
    server_data = HASH_CHECKER()
    cliner_data = hada

    print(cliner_data)
    # conn.send(server_data.encode())
    uploader(conn)
    # if server_data != cliner_data:
    #     uploader(conn)

def uploader(conn):
    # with open('mobile.exe', 'rb') as f:
    #     data = f.read()
    file_size = str(os.path.getsize('./mobile.exe'))
    conn.send(file_size.encode())
    stat = conn.recv(1000)
    print(stat)
    if stat.decode('utf-8') == 'ready':
        with open('mobile.exe', 'rb') as f:
            try:
                data = f.read(1024)
                while data:
                    transed = conn.send(data)
                    data = f.read(1024)
            except Exception as e:
                print(e)
        print("전송완료 %s, 전송량 %d" %("mobile.exe", transed))

max_thread = 10

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind(("0.0.0.0",19520))
soc.listen(100)

while True:
    conn, addr = soc.accept()
    data = conn.recv(1500).decode('utf-8')
    Thread(target=hash_diff,args=(data,conn),daemon=True).start()
