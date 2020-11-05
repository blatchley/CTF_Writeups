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

def rotationsort(arr, p1, p2, q1, q2):
    n = len(arr)
    statedict = {}
    for elem in arr:
        statedict[elem] = 0
    k1 = p2 - p1 % n
    k2 = q2 - q1 % n
    k3 = k1 + k2
    solution = ""
    copiedlist = [elem for elem in arr]
    copiedlist.sort()
    permutedlist = []
    for i in range(n):
        permutedlist.append(copiedlist[(i*(k3)) % n])
    permutedvals = {}
    for j in range(n):
        permutedvals[permutedlist[j]] = j
    smallest = copiedlist[0]
    print("smallest")
    print(smallest)
    print(n)
    solution = ""
    a, b, c, d = p1, p2, q1, q2
    swappos = d - k3
    while True:
        if (arr[0] == smallest) and (arr == copiedlist):
            print("returning")
            # print(arr)
            return solution
        elif statedict[arr[b]] == 1 and (statedict[arr[a]] == 6):
            arr = switch(arr,a,b)
            solution = solution + "a "
            statedict[arr[a]] = 0
            statedict[arr[b]] = 2
        elif statedict[arr[d]] == 7 and statedict[arr[c]] == 2:
            solution = solution + "b "
            arr = switch(arr,c,d)
            statedict[arr[d]] = 0
            statedict[arr[c]] = 0
        elif arr[d] > smallest:
            if permutedvals[arr[swappos]] > permutedvals[arr[d]]:
                if (statedict[arr[d]] + statedict[arr[c]] + statedict[arr[swappos]]) == 0:
                    solution = solution + "b "
                    arr = switch(arr,c,d) 
                    statedict[arr[d]] = 7
                    statedict[arr[c]] = 1
                    statedict[arr[swappos]] = 6
        arr = rotate(arr)
        solution = solution + "c "

print("starting")
sock = socket()
sock.connect(('challenges.ctfd.io', 30267))
welcome = str(sock.recv(1024))
print("received welcome")
t = Telnet()
t.sock = sock
sock.send(bytes(str(5) + "\n", "utf-8"))
chal12 = str(sock.recv(4096))
print(chal12)
chal1 = chal12.split("alphabetical order:\\n\\n")[1].split("\\n\\n")
suffix = chal1[1].split("vegetable in position")
ingredients = [x.strip() for x in chal1[0].split(",")]
print(ingredients)
print(len(ingredients))
p1 = 29
p2 = 64
q1 = 85
q2 = 173
solution = rotationsort(ingredients, p1, p2, q1 ,q2).strip()
print("solution length")
print(len(solution))
sock.send(bytes(solution + "\n", "utf-8"))
chal2 = str(sock.recv(4096))
print(chal2)