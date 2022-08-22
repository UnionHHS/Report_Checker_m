import hashlib
from time import sleep

with open('mobile.exe', 'rb') as f:
    data = f.read()
    h = hashlib.sha256()
    h.update(data)
    text = h.hexdigest()

with open(f'version.hash','w', encoding='utf-8') as f:
    f.write(text)



def soc_t():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
        sc.connect(("192.168.50.134",19520))
        sc.send("text".encode())
        size_data = sc.recv(4096)
        size_data = size_data.decode('utf-8')
        print(size_data)
        sc.send("ready".encode())
        data_transferred = 0
        data = sc.recv(1024)
        if not data:
            print("오류발생")
        with open("./FILE.exe", 'wb') as f:
            try:
                data = sc.recv(1024)
                while data:
                    f.write(data)
                    data_transferred += len(data)
                    data = sc.recv(1024)
            except Exception as e:
                print(e)
        print('파일 %s 받기 완료. 전송량 %d' %("FILE", data_transferred))
        sc.close()
    