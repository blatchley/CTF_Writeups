#!/usr/bin/python3
import qrcode  # https://github.com/lincolnloop/python-qrcode
import random
import os
from PIL import Image
from randcrack import RandCrack # https://github.com/tna0y/Python-random-module-cracker
from textwrap import wrap
# import zxing # only needed to read data from output inside the script. Requires Java

def main():
    # Generate placeholder image with hidden data which generates a QR code of 444x444
    # Was useful for size information, formats etc. Not really needed
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=12,
        border=4,
    )
    qr.add_data("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    m, n = img.size

    # load share 2
    share2 = Image.open('share2.png')

    # Calculate randomness bitstream from last 624 * 32 bits of padding
    # We know the last 48 * 444 pixels were white, so can deduce random bits used from only share2.png
    bitstream = []
    for idx in range(48 * 444):
        i, j = idx//n + 444 - 48, idx % n
        if share2.getpixel((2*j, 2*i)):
            bitstream.append(0)
        else:
            bitstream.append(1)
    bitstream = "".join([str(x) for x in bitstream])


    # Load bitstream, and use cracker to simulate mersene twister state
    rc = RandCrack()

    # As getrandbits Generates sets of 32 bit integers, and puts the first ones generated at the end of the sequence of bits,
    # we need to invert the sequence so we give the last bits (the first generated) to randcracker in the right order
    splitstream = wrap((bitstream), 32)
    splitstream.reverse()

    # Seed the mersene twister cracker with 624 32 bit integers
    for i in range(624):
        val = int(splitstream[i],2)
        rc.submit(val)

    # Predict randomness for all remaining pixels in source image
    newlist = bin(rc.predict_getrandbits(444 * 444))[2:].zfill(444 * 444)

    # Add the calculated randomness back onto the end of the approximated randomness
    splitstream2 = newlist[-(444*444 - (32 * 624)):] + bitstream[-(32 * 624):]
  
    # Given the known randomness, we can reconstruct the original image from share2.png
    original = []
    for k in range(444 * 444):
        # l = k + 444*444 - 1 % (444*444)
        i, j = k//n, k % n
        if share2.getpixel((2*j, 2*i)):
            if int(splitstream2[k]):
                original.append(0)
            else:
                original.append(255)
        else:
            if int(splitstream2[k]):
                original.append(255)
            else:
                original.append(0)

    # Save the resulting data back into an image
    res = Image.new("L", img.size, 255)
    res.putdata(original)
    res.save('result3.png')
    
    # # Read data out of image, and print to console. Optional QoL step using zxing
    # # Can also just use any qr code reader app or service on result3.png
    # reader = zxing.BarCodeReader()
    # barcode = reader.decode("result3.png")
    # print(barcode.parsed)

if __name__ == '__main__':
    main()
