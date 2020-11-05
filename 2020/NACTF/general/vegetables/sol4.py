from socket import socket
from telnetlib import Telnet
import string, itertools, hashlib
import sys
from collections import deque

def switch(arr, p, q):
    arr[p], arr[q] = arr[q], arr[p]
    return arr

def rotate(arr):
   return arr[1:] + arr[:1]

def applyscript(arr,p,q,script):
    orders = script.split()
    print(orders)
    for order in orders:
        if order == "s":
            arr = switch(arr,p,q)
        elif order == "c":
            arr = rotate(arr)
    return arr

def rotationsort(arr, p1, p2):
    n = len(arr)
    k = p2 - p1 % n
    solution = ""
    copiedlist = [elem for elem in arr]
    copiedlist.sort()
    permutedlist = []
    for i in range(n):
        permutedlist.append(copiedlist[(i*k) % n])
    permutedvals = {}
    for j in range(n):
        permutedvals[permutedlist[j]] = j
    smallest = copiedlist[0]
    print("smallest")
    print(smallest)
    print(n)
    solution = ""
    a, b = p1, p2
    while True:
        if (arr[0] == smallest) and (arr == copiedlist):
            print("returning")
            print(arr)
            return solution
        elif arr[b] > smallest:
            if permutedvals[arr[a]] > permutedvals[arr[b]]:
                solution = solution + "s c "
                arr = switch(arr,a,b)         
                arr = rotate(arr)
            else:
                solution = solution + "c "
                arr = rotate(arr)
        else:
            arr = rotate(arr)
            solution = solution + "c "


print("starting")
sock = socket()
sock.connect(('challenges.ctfd.io', 30267))
welcome = str(sock.recv(1024))
print("received welcome")
t = Telnet()
t.sock = sock
sock.send(bytes(str(4) + "\n", "utf-8"))
chal12 = str(sock.recv(4096))
print(chal12)
# sys.exit()
chal1 = chal12.split("alphabetical order:\\n\\n")[1].split("\\n\\n")
# print("received challenge 1")
# print(chal1)
suffix = chal1[1].split("vegetable in position")
ingredients = [x.strip() for x in chal1[0].split(",")]
pos1 = int(suffix[1].split("with the")[0].strip())
pos2 = int(suffix[2].strip())
print(pos1)
print(pos2)
# sys.exit()
solution = rotationsort(ingredients, pos1, pos2).strip()
print("solution length")
print(len(solution))
# print("sending " + solution)
sock.send(bytes(solution + "\n", "utf-8"))
chal2 = str(sock.recv(4096))
print(chal2)
