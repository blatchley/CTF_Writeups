# Crypto
*Solutions and write-ups by killerdog of team Kalmarunionen*

Writeups for some of the general skills challenges which I solved.



## Zip Madness
Used a basic python script which invokes 7z to folders in a chain, deleting the extra zip files, until there was only the last layer left, which i could manually unzip and read flag.

```python
import requests
import subprocess
import re
import sys
import time
from random import randrange
import os

fileindex = 1000
while fileindex > 2:
    direction = ""
    with open("direction.txt") as f:
        direction = f.readline().strip()
    os.remove("direction.txt")
    target = str(fileindex) + direction + ".zip"
    p =  subprocess.Popen(['7z', 'x', '-y', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate() 
    if out[1] != b'': 
        raise Exception(out[1].decode('UTF-8'))
    os.remove(str(fileindex) + "left.zip")
    os.remove(str(fileindex) + "right.zip")
    fileindex -= 1
```


## World trip
Found a python library which allowed location lookup by coordinates. I was confused for a while by the syntax of the flag, as the last many characters are just random. But then a teammate realised you could just wrap the output in nactf{..} and submitted it, and it worked. 

The script takes a while to run, as the endpoint isn't very fast. Also beware 

```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="jame234s2")
location = geolocator.reverse("52.509669, 13.376294")

locations = ""
with open("enc.txt") as f:
    locations = f.read()

loclist = locations[1:][:-1].split(")(")
# print(loclist)
print("performing lookups")
output = [geolocator.reverse((loc),language="en-gb").raw["address"]["country"] for loc in loclist]
print(output)
flag = "nactf{"
for country in output:
    flag = flag + country[0]
flag = flag + "}"
print(flag)
```

## Vegetables 1
Just connect to endpoint and manually work out the bubble sort solution, and send it.

## Vegetables 2
I manually coded a simple bubblesort algorithm, and each time the algorithm made a swap, i concatenated the swap index onto a solution string. Finally i sent that string back to the server once the list was sorted.

I've lost the file i used for this, may readd later.

## Vegetables 3
We can now only rotate and swap the elements at 0 and 1.

The first thing to note here is we need some fixed point, so that we don't keep swapping forever. I sort the list and save the smallest element, and this will now be our fixed point. We now cycle through the list, swapping if the element in index 0 is bigger than the one in index 1, as long as the element in index 1 is NOT the smallest element.

Every time we reach the smallest element in index 0, we check if the list is sorted yet by checking if we performed any swaps on the previous rotation.

The code for this exercise is pretty quick and dirty, i refined it a lot more for 4 and 5.

A copy of the sorting functionality is below, for full script with my (very very ugly) networking code, see [the code](vegetables\sol3.py)

```python
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
    thisround = ""
    a, b = 0, 1
    while True:
        if arr[a] == smallest:
            if ordered == True:
                return solution
            ordered = True
            solution = solution + thisround
            thisround = "c "
            a, b = (a + 1) % (siz), (b + 1) % (siz)
        elif arr[b] > smallest and arr[a] > arr[b]:
            ordered = False
            thisround = thisround + "s c "
            arr[a], arr[b] = arr[b], arr[a]              
            a, b = (a + 1) % (siz ), (b + 1) % (siz )
        else:
            a, b = (a + 1) % (siz ), (b + 1) % (siz )
            thisround = thisround + "c "
```

## Vegetables 4
We can now only swap between indexes `i` and `j`. The first thing we note is that the array has a consistent length of 211, which is prime. This is important because this means we can reach any element from any other element, in `n` jumps of `k` rotations, where `k = j - i`. 

This follows from the fact that for a prime order group of order `N`, for any elements `a`, `b`, there exists a value `n` less than `N`, such that the congruence `a + n*k = b (mod N)` holds. This means we can move any element to any other position in a number of swaps less than 211.

The complication here is deciding what metric to use for comparisons. Simply using size doesn't work, as some elements will have to wrap around the array many times to reach their real place. The solution i arrived at was to note that when we fix the smallest element as before, if we want to bubble sort, then the element which comes "after" the smallest element is the element in position `k`, as this is the element which will be compared to the smallest when the smallest is in one of the swap locations.

This means if we get the `k`'th smallest element into the position `k` after the smallest element, then it will never have to move again, and will never be asked to move, and the next element we want to get into position is the `2k`'th smallest element. We can generalise this to looping around the array using a modulus, and we instantiate this by taking the list, sorting it, then creating a new list which lists them in "order to sort", going [smallest, k'th smallest, 2k'th smallest...], then recording the elements indexes in this array and sorting by those indexes. This gives us a good heuristic for sorting, as we're kind of using an isomorphism into a group where the two swap locations are adjacent~ (kind of.)

I also realised at this point that local computation was not at all the bottleneck, i made the logic simpler by removing indexes and actually rotating the array. This runs almost instantly and produces outputs of ~70k characters, which are easily under the server limit.

sorting code below, see [code](vegetables\sol4.py) for full solution including very ugly network code.
```python
def switch(arr, p, q):
    arr[p], arr[q] = arr[q], arr[p]
    return arr

def rotate(arr):
   return arr[1:] + arr[:1]

def rotationsort(arr, p1, p2):
    # Traverse through 1 to len(arr) 
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
    ordered = False
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
```

## Vegetables 5
trivial generalisation redacted due to boring admins
boo
hiss