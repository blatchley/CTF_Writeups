from socket import socket
from telnetlib import Telnet
import string, itertools, hashlib

def switch(arr):
    return arr[1::-1] + arr[2:]

def rotate(arr):
   return arr[1:] + arr[:1]

def rotationsort(arr):
    solution = ""
    copiedlist = [elem for elem in arr]
    copiedlist.sort()
    smallest = copiedlist[0]
    ordered = False
    print("smallest")
    print(smallest)
    siz = len(arr)
    print(siz)
    solution = ""
    a, b = 0, 1
    while True:
        if arr[a] == smallest:
            if arr == copiedlist
                return solution
            thisround = "c "
            a, b = (a + 1) % (siz), (b + 1) % (siz)
        elif arr[b] > smallest and arr[a] > arr[b]:
            solution = solution + "s c "
            arr[a], arr[b] = arr[b], arr[a]              
            a, b = (a + 1) % (siz ), (b + 1) % (siz )
        else:
            a, b = (a + 1) % (siz ), (b + 1) % (siz )
            solution = solution + "c "

            
print("starting")
sock = socket()
sock.connect(('challenges.ctfd.io', 30267))
welcome = str(sock.recv(1024))
print("received welcome")
t = Telnet()
t.sock = sock
sock.send(bytes(str(3) + "\n", "utf-8"))
chal1 = str(sock.recv(4096)).split("alphabetical order:\\n\\n")[1].split("\\n\\n")[0]
print("received challenge 1")
print(chal1)
ingredients = [x.strip() for x in chal1.split(",")]
print("the ingredients are")
print(ingredients)
solution = rotationsort(ingredients).strip()
print("sending  solution")
sock.send(bytes(solution + "\n", "utf-8"))
splitstring = "That's correct!! \\xf0\\x9f\\xa5\\xac\\xf0\\x9f\\xa5\\x95\\xf0\\x9f\\x8c\\xbd\\xf0\\x9f\\x8d\\x86\\xf0\\x9f\\xa5\\xa6\\xf0\\x9f\\xa5\\x92\\xf0\\x9f\\xa5\\x91\\xf0\\x9f\\x8d\\x84\\n\\n\\xf0\\x9f\\xa5\\xac\\xf0\\x9f\\xa5\\x95\\xf0\\x9f\\x8c\\xbd\\xf0\\x9f\\x8d\\x86\\xf0\\x9f\\xa5\\xa6\\xf0\\x9f\\xa5\\x92\\xf0\\x9f\\xa5\\x91\\xf0\\x9f\\x8d\\x84 STAGE "
splitstring2 = " \\xf0\\x9f\\xa5\\xac\\xf0\\x9f\\xa5\\x95\\xf0\\x9f\\x8c\\xbd\\xf0\\x9f\\x8d\\x86\\xf0\\x9f\\xa5\\xa6\\xf0\\x9f\\xa5\\x92\\xf0\\x9f\\xa5\\x91\\xf0\\x9f\\x8d\\x84\\n"
# print("LINE 22222222222")
for i in range(2,3):
    chal1 = str(sock.recv(7000))#.split(splitstring)[-1][:-5] #.split("\\x8d\\x84\\n")[-1].split("\\n\\n")[0]
    print("received challenge ") # + str(i))
    print(chal1)
    ingredients = [x.strip() for x in chal1.split(splitstring + str(i) + splitstring2)[-1][:-5].split(",")] # [3].split("\\n\\n")]
    print("ingredients are")
    print("@@@@@@@@@@@@@@@@@@@@@@@@")
    print(ingredients)
    print("@@@@@@@@@@@@@@@@@@@@@@@@")
    solution = rotationsort(ingredients).strip()
    # print("sending " + solution)
    sock.send(bytes(solution + "\n", "utf-8"))
# chal2 = str(sock.recv(4096))
    # print(chal2)