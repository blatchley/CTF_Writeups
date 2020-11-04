import random
from functools import reduce
from textwrap import wrap

ct = ""
with open("enc.txt") as file: # Use file to refer to the file object
   ct = file.read()
   
chunks = [[int(j) for j in ct[i:i + 15]] for i in range(0, len(ct), 15)]
solution = ""
for chunk in chunks:
    for i in range(len(chunk)):
        # test each possible bit for the corruption
        candidate = [x for x in chunk]
        candidate[i] = int(not candidate[i])
        parity = []
        for j in range(4):
            parity.append(candidate[2 ** j - 1])
        for j in range(4):
            candidate[2 ** j - 1] = 0

        paritycalc = reduce(lambda a, b: a ^ b, [j + 1 for j, bit in enumerate(candidate) if bit])
        paritycalc = list(reversed(list(str(format(paritycalc, "04b")))))
        paritycalc = [int(x) for x in paritycalc]
        # if parity matches, we fixed the error
        if paritycalc == parity:
            indexes = [0,1,3,7]
            for d in sorted(indexes,reverse=True):
                del candidate[d]
            sol = "".join([str(x) for x in candidate])
            solution = solution + sol
            break

solution = wrap(solution,8)
flag = [chr(int(j,2)) for j in solution]
print("".join(flag))