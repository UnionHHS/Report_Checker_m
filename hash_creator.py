import os,sys
import socket
import ctypes
import hashlib
import time, zipfile, traceback
import atexit

# server_loc = ('172.30.1.58',19520)
server_loc = ('192.168.120.100',19520)

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
        with zipfile.ZipFile(f'./log_file.zip','w') as zf:
            for folder, sfolder, files in os.walk('./log'):
                for i in files:
                    zf.write(os.path.join(folder, i), os.path.relpath(os.path.join(folder, i), './log'), compress_type = zipfile.ZIP_DEFLATED)
    else:
        with open(f"./log/log_{date}.log",'a',encoding='utf8') as f:
            f.writelines(f"{times} = [{types}] {data}\n")

def HASH_CHECKER():
    log_writer("I","[Patcher] Hash File Created")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
            sc.connect(server_loc)
            sc.send("version".encode())
            data = sc.recv(4096)
            data = data.decode('utf-8')
            with open('./version', 'w', encoding='utf-8') as f:
                f.write(data)
            # return data
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, "프로그램 업데이트를 실패했습니다.\n개발자에게 연락 후 나스 폴더에서 새로 받아주시길 바랍니다!", "오류", 16)
        log_writer("E","[Patcher] Hash File Create Fail", e)

def soc_t():
    try:
        log_writer("I",f"[Patcher] Connect Server = {server_loc}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
            sc.connect(server_loc)
            # with open('./version', 'r', encoding='utf-8') as f:
            #     hada = f.read()
            sc.send("main ready".encode())
            size_data = sc.recv(4096)
            size_data = size_data.decode('utf-8')
            print(f'파일 크기 = {size_data}Bytes')
            data_transferred = 0
            with open("./bin/mobile.exe", 'wb') as f:
                log_writer("I","[Patcher] Recv File")
                try:
                    data = sc.recv(1024)
                    while data:
                        f.write(data)
                        data_transferred += len(data)
                        data = sc.recv(1024)
                except Exception as e:
                    print(e)
            print('파일 %s 받기 완료. 전송량 %d' %("FILE", data_transferred))
            log_writer("I","[Patcher] Update Complete")
            sc.close()
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, "프로그램 업데이트를 실패했습니다.\n개발자에게 연락 후 나스 폴더에서 새로 받아주시길 바랍니다!", "오류", 16)
        log_writer("E","[Patcher] Update Failed", e)

def runs():
    os.popen(r".\bin\mobile.exe")

atexit.register(runs)
try:
    if not os.path.isdir("./log"):
        os.mkdir('./log')
    log_writer('I',f"[Patcher] Update Check Target Server = {server_loc}")
    
    with open('./version', 'r', encoding='utf-8') as f:
        hada = f.read()
    if hada == '':
        raise "Update Failed Run Normal Mode"
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(server_loc)
    soc.send(hada.encode('utf-8'))
    data = soc.recv(1024)
    if data.decode('utf-8') == 'Version Changed':
        log_writer('I',"[Patcher] Update Start")
        ctypes.windll.user32.MessageBoxW(0, "프로그램 업데이트가 있습니다.\n업데이트를 시작합니다.", "알림", 0)
    else:
        log_writer("I","[Patcher] Not Avilable Update")
    try:
        log_writer("I","[Patcher] Main Process Kill Seq")
        os.system('taskkill /f /im mobile.exe')
        os.remove(r'.\bin\mobile.exe')
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, "프로그램 업데이트를 실패했습니다.\n개발자에게 연락 후 나스 폴더에서 새로 받아주시길 바랍니다!", "오류", 16)
        log_writer("E","[Patcher] Kill Failed")

    try:
        log_writer("I","[Patcher] Update Run")
        soc_t()
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, "프로그램 업데이트를 실패했습니다.\n개발자에게 연락 후 나스 폴더에서 새로 받아주시길 바랍니다!", "오류", 16)
        log_writer("I","[Patcher] Update Fail")
    

    try:
        log_writer("I","[Patcher] Version Hash File Re Write")
        HASH_CHECKER()

    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, "프로그램 업데이트를 실패했습니다.\n개발자에게 연락 후 나스 폴더에서 새로 받아주시길 바랍니다!", "오류", 16)
        log_writer("E","[Patcher] Verion Hash File Re Write Fail")

except Exception as e:
    log_writer('E',"[Patcher] Update Process Error!", e)
    ctypes.windll.user32.MessageBoxW(0, "프로그램 에러가 발생하였습니다.\n폴더내 생성된 압축파일을 개발자한테 전달 부탁드립니다.", "오류", 16)


    