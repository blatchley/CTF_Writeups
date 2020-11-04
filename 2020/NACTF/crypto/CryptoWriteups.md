# Crypto
*Solutions and write-ups by killerdog of team Kalmarunionen*

For the most part the crypto in this CTF was pretty simple. I solved all of them for our team other than the PRNG challenge.


## Caesars Challenge
`anpgs{q3p1cu3e1at_e0px5!}`

From the name I assumed this was a caesar cipher, and the text even gave us the offset.

Putting this into a caesar cipher decoder with offset 13 gives the flag. (My go to for lazy caesar solves: https://www.dcode.fr/caesar-cipher)


## Yams
`Uexummq lm Vuycnqjc. Hqjc ie qmud xjas: fycfx{waY5_sp3_Y0yEw_w9vU91}`

Given the spacing and format of the ciphertext, it's clearly a substitution cipher. The hint points us towards a vignere cipher.

First logical thought from the description was that YAMS must be the password to the vignere cipher. [Solving using cyberchef](https://gchq.github.io/CyberChef/#recipe=Vigen%C3%A8re_Decode('YAMS')&input=VWV4dW1tcSBsbSBWdXljbnFqYy4gSHFqYyBpZSBxbXVkIHhqYXM6IGZ5Y2Z4e3dhWTVfc3AzX1kweUV3X3c5dlU5MX0) gives the flag.


## Oligar's Tricky RSA
`c = 97938185189891786003246616098659465874822119719049`

`e = 65537`

`n = 196284284267878746604991616360941270430332504451383`

This is literally just RSA with small primes.

My first step with RSA is always to [factordb the modulus](http://factordb.com/index.php?query=196284284267878746604991616360941270430332504451383) and it trivially decomposed into two primes, p and q.

From there just calculate d = e^-1 mod ((p-1)(q-1))

And the plaintext is c^d mod n. Decoding to ascii giving the flag.

## Error 0
My first assumption was that the noise level would be <70%. If this is true then there should be the value in each index at least 65% of the time. (30% + 0.5 * 70% = 65%).

Dividing message length by 101 gave 232 bit chunks, so I wrote a script which split the ciphertext into 232 bit strings, and counted the number of occurences of each character in each index. Then output a string which had the most common character in each index.

This gave the flag 

```python
from textwrap import wrap

data = ""
with open("enc.txt") as file: 
   data = file.read()
messages = wrap(data,232)

cleaned = []
for i in range(232):
   val = 0
   for message in messages:
      val += int(message[i])
   cleaned.append(val)

output = ""
for num in cleaned:
   if num > 60:
      output = output + "1"
   else:
      output = output + "0"

flag =  bytearray.fromhex(str(hex(int(output, 2)))[2:]).decode()
print(flag)
```

## ERROR 1
We are given some code which inserts checksum digits/a hamming code into the ciphertext, and then a random bit in each chunk is flipped. There's probably a theoretical way of solving this, but the sizes are small enough that I just went with a trivial bruteforce.

This uses two facts. We know that exactly one bit is flipped in each chunk of 15 bits in the ciphertext, and we assume that if we flip one bit at random again in each chunk, that chunks hamming code will only verify if the bit we flipped was the initial bit which was flipped. (That is, it's unlikely that we flip a second bit, and this produces a chunk where the new plaintext/hamming code also verify.)

My script is pretty simple. For verification, I strip the hamming code values out from the known indexes in the message, then create a new hamming code for that message using the same code they gave, before comparing the two hamming codes. If I've correctly fixed the message, the hamming codes will match. Otherwise there will be two inconsistent bits in the message/hamming code values, and it won't match.

I then try flipping each bit for each chunk until i find the version of the chunks where the hamming codes match, concatenate those, and get the flag.

```python
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

```

## ERROR 2
redacted due to boring admins