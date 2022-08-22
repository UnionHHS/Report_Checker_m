import os
import hashlib

# with open('./mobile.exe', 'rb') as f:
with open('./dist/mobile.exe', 'rb') as f:
    data = f.read()

h = hashlib.sha256()
h.update(data)
hashs = h.hexdigest()
with open('./dist/version.hash', 'w', encoding='utf-8') as f:
# with open('version.hash', 'w', encoding='utf-8') as f:
    f.write(hashs)

# with open('./Git/Report_Checker_m/dist/version.hash', 'w' ,encoding='utf-8') as f:
#     f.write(hashs)