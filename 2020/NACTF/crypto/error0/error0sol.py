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