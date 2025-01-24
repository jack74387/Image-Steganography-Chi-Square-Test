# PIL module is used to extract
# pixels of image and modify it
from PIL import Image

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
        # print(f"Character: {i}, ASCII: {ord(i)}, Binary: {format(ord(i), '08b')}")
    return newd

# Calculate parity bit (even parity)
def calculate_parity(bits):
    return sum(int(bit) for bit in bits) % 2

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        # Modify the first 8 bits based on the data
        for j in range(8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        # Set the ninth bit as the parity bit (even parity)
        parity_bit = calculate_parity(datalist[i])
        if parity_bit == 0 and pix[8] % 2 != 0:
            pix[8] -= 1
        elif parity_bit == 1 and pix[8] % 2 == 0:
            if pix[8] != 0:
                pix[8] -= 1
            else:
                pix[8] += 1

        # print(f"Encoding Data: {datalist[i]}, Parity Bit: {parity_bit}, Pixels: {pix[:9]}")

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def encode():
    img = "cover-image/" + input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    file_name = "text/" + input("Enter the file name to read data from (with extension) : ")
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("The specified file does not exist.")

    if len(data) == 0:
        raise ValueError('Data file is empty')
    
    print(len(data))
    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = "stego-image/" + input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def decode():
    img = "stego-image/" + input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())
    count = 0

    try:
        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3]]

            # Extract the first 8 bits
            binstr = ''
            for i in pixels[:8]:
                binstr += '0' if i % 2 == 0 else '1'

            # Verify the parity bit
            parity_bit = pixels[8] % 2
            calculated_parity = calculate_parity(binstr)

            # Debugging output
            # print(f"Binary: {binstr}, Parity Bit: {parity_bit}, Calculated Parity: {calculated_parity}")

            if parity_bit != calculated_parity:
                count = count + 1
                print(count, "Parity check failed.", f"Binary: {binstr}, Parity Bit: {parity_bit}, Calculated Parity: {calculated_parity}")

            # Convert binary to character and append to data
            data += chr(int(binstr, 2))

    except StopIteration:
        # Return the decoded data when all pixels are processed
        return data


# Main Function
def main():
    a = int(input(":: Welcome to Steganography ::\n"
                        "1. Encode\n2. Decode\n"))
    if a == 1:
        encode()

    elif a == 2:
        print("Decoded Word : " + decode())
    else:
        raise Exception("Enter correct input")

# Driver Code
if __name__ == '__main__':

    # Calling main function
    main()
