import socket
import os
import time
import traceback
# import zipfile
from threading import Thread

def log_writer(types, data, Except=None):
    tm = time.localtime(time.time())
    date = (str(tm.tm_year)[2:] + str(tm.tm_mon).zfill(2) + str(tm.tm_mday).zfill(2))
    times = f"{tm.tm_year}-{str(tm.tm_mon).zfill(2)}-{str(tm.tm_mday).zfill(2)} {str(tm.tm_hour).zfill(2)}:{str(tm.tm_min).zfill(2)}:{str(tm.tm_sec).zfill(2)}"
    if types == 'E':
        with open(f"./log/log_{date}.log",'a',encoding='utf8') as f:
            f.writelines(f"{times} = [{types}] {data}\n")
            f.writelines("---------ERROR---------\n")
            f.writelines(traceback.format_exc())
            f.writelines("-----------------------\n")
            f.writelines("Plz Report Developer\n")
        # with zipfile.ZipFile(f'./log_file.zip','w') as zf:
        #     for folder, sfolder, files in os.walk('./log'):
        #         for i in files:
        #             zf.write(os.path.join(folder, i), os.path.relpath(os.path.join(folder, i), './log'), compress_type = zipfile.ZIP_DEFLATED)
    else:
        with open(f"./log/log_{date}.log",'a',encoding='utf8') as f:
            f.writelines(f"{times} = [{types}] {data}\n")


def HASH_CHECKER():
    # with open(f'./Git/Report_Checker_m/dist/version', 'r') as f:
    with open('./dist/version', 'r', encoding='utf-8') as f:
        data = f.read()
    return data

def hash_diff(hada, conn, addr):
    server_data = HASH_CHECKER()
    cliner_data = hada
    # print(hada)
    if cliner_data == 'main ready':
        uploader(conn, addr)
        return 0
    elif cliner_data == 'version':
        print(f"{addr}  Client Version Send : {server_data}")
        log_writer("I",f"{addr}  Client Version Send : {server_data}")
        conn.send(HASH_CHECKER().encode('utf-8'))
    elif server_data != cliner_data:
        print(f"{addr}  Client Version Update : {hada} -> {server_data}")
        log_writer("I",f"{addr}  Client Version Update : {hada} -> {server_data}")
        conn.send("Version Changed".encode('utf-8'))
    else:
        conn.send("Not Changed".encode('utf-8'))
    
def uploader(conn, addr):
    file_size = str(os.path.getsize('./dist/mobile.exe'))
    conn.send(file_size.encode('utf-8'))
    data_transferred = 0
    # with open(f'./Git/Report_Checker_m/dist/mobile.exe', 'rb') as f:
    with open('./dist/mobile.exe', 'rb') as f:
        try:
            data = f.read(1024) # 파일 읽기 여부 확인
            while data:
                data_transferred += conn.send(data) # 전송된 파일 크기가 리턴되어 data_transferred 함수에 저장
                data = f.read(1024) #파일 1024 만큼 추가 읽기
        except Exception as ex:
            print(ex)
    log_writer("I",f"{addr}  Client File Send Size : {data_transferred}")
    print(f"{addr} -> 전송완료 mobile.exe, 전송량 {data_transferred}")
    conn.close()

os.chdir('/home/f1')

if not os.path.isdir("./log"):
    os.mkdir('./log')

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind(("0.0.0.0",19520))
soc.listen(100)

while True:
    conn, addr = soc.accept()
    print(f"{addr} Connected")
    data = conn.recv(1500).decode('utf-8')
    Thread(target=hash_diff,args=(data, conn, addr),daemon=True).start()
