import random
from functools import reduce
from itertools import permutations 
from textwrap import wrap
import sys

parityposlist = permutations([x for x in range(15)], 4)
ct = ""
with open("enc.txt") as file: # Use file to refer to the file object
   ct = file.read()

chunks = [[int(j) for j in ct[i:i + 15]] for i in range(0, len(ct), 15)]

for i, parity_pos in enumerate(parityposlist):
    if i % 1000 == 0:
        print("progress: " + str(i) + " out of 33000")
    solution = ""
    for chunk in chunks:
        chunksolved = 0
        try:
            for i in range(len(chunk)):
                # test each possible bit for the corruption
                candidate = [x for x in chunk]
                candidate[i] = int(not candidate[i])
                parity = []
                for j in range(4):
                    parity.append(candidate[parity_pos[j]])
                for d in sorted(parity_pos,reverse=True):
                    del candidate[d]
                for j in range(4):
                    candidate.insert(2 ** j - 1, 0)
                paritycalc = reduce(lambda a, b: a ^ b, [j + 1 for j, bit in enumerate(candidate) if bit])
                paritycalc = list(reversed(list(str(format(paritycalc, "04b")))))
                paritycalc = [int(x) for x in paritycalc]
                # if parity matches, we fixed the error
                if paritycalc == parity:
                    chunksolved += 1
                    for d in sorted([0,1,3,7],reverse=True):
                        del candidate[d]
                    sol = "".join([str(x) for x in candidate])
                    solution = solution + sol
            if (not (chunksolved == 1)):
                break
        except:
            break

    if len(solution) == 440:
        solution = wrap(solution,8)
        try:
            flag = "".join([chr(int(j,2)) for j in solution])
            if flag.startswith("nactf"):
                print(flag)
                break
        except:
            continue