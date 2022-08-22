import socket
import os
from threading import Thread

def HASH_CHECKER():
    with open(f'./Git/Report_Checker_m/dist/version', 'r') as f:
    # with open('./dist/version', 'r', encoding='utf-8') as f:
        data = f.read()
    return data

def hash_diff(hada, conn):
    server_data = HASH_CHECKER()
    cliner_data = hada
    print(hada)
    if cliner_data == 'main ready':
        uploader(conn)
        return 0
    elif cliner_data == 'version':
        conn.send(HASH_CHECKER().encode('utf-8'))
    elif server_data != cliner_data:
        conn.send("Version Changed".encode('utf-8'))
    else:
        conn.send("Not Changed".encode('utf-8'))
    
def uploader(conn):
    file_size = str(os.path.getsize('./mobile.exe'))
    conn.send(file_size.encode('utf-8'))
    data_transferred = 0
    with open(f'./Git/Report_Checker_m/dist/mobile.exe', 'rb') as f:
    # with open('./dist/mobile.exe', 'rb') as f:
        try:
            data = f.read(1024) # 파일 읽기 여부 확인
            while data:
                data_transferred += conn.send(data) # 전송된 파일 크기가 리턴되어 data_transferred 함수에 저장
                data = f.read(1024) #파일 1024 만큼 추가 읽기
        except Exception as ex:
            print(ex)
    print("전송완료 %s, 전송량 %d" %("mobile.exe", data_transferred))
    conn.close()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind(("0.0.0.0",19520))
soc.listen(100)

while True:
    conn, addr = soc.accept()
    data = conn.recv(1500).decode('utf-8')
    Thread(target=hash_diff,args=(data,conn),daemon=True).start()
