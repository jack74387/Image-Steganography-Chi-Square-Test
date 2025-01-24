from PIL import Image

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    return [format(ord(i), '08b') for i in data]

# Calculate Hamming Code (12,8)
def calculate_hamming(bits):
    p1 = int(bits[0]) ^ int(bits[1]) ^ int(bits[3]) ^ int(bits[4]) ^ int(bits[6])
    p2 = int(bits[0]) ^ int(bits[2]) ^ int(bits[3]) ^ int(bits[5]) ^ int(bits[6])
    p4 = int(bits[1]) ^ int(bits[2]) ^ int(bits[3]) ^ int(bits[7])
    p8 = int(bits[4]) ^ int(bits[5]) ^ int(bits[6]) ^ int(bits[7])
    return f"{p1}{p2}{bits[0]}{p4}{bits[1]}{bits[2]}{bits[3]}{p8}{bits[4]}{bits[5]}{bits[6]}{bits[7]}"

# Correct a single-bit error using Hamming Code (12,8)
def correct_hamming(bits):
    p1 = int(bits[0]) ^ int(bits[2]) ^ int(bits[4]) ^ int(bits[6]) ^ int(bits[8]) ^ int(bits[10])
    p2 = int(bits[1]) ^ int(bits[2]) ^ int(bits[5]) ^ int(bits[6]) ^ int(bits[9]) ^ int(bits[10])
    p4 = int(bits[3]) ^ int(bits[4]) ^ int(bits[5]) ^ int(bits[6]) ^ int(bits[11])
    p8 = int(bits[7]) ^ int(bits[8]) ^ int(bits[9]) ^ int(bits[10]) ^ int(bits[11])
    error_position = p1 * 1 + p2 * 2 + p4 * 4 + p8 * 8

    if error_position > 0:
        print(f"Error detected at position {error_position}, correcting it.")
        # Flip the bit at the error position (1-based index)
        error_position -= 1  # Convert to 0-based index
        corrected_bits = list(bits)
        corrected_bits[error_position] = '0' if bits[error_position] == '1' else '1'
        return ''.join(corrected_bits)
    return bits

# Pixels are modified according to the
# Hamming (12,8) encoded data and returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extract 4 pixels (12 RGB values)
        pix = [value for value in imdata.__next__()[:3] +
                            imdata.__next__()[:3] +
                            imdata.__next__()[:3] +
                            imdata.__next__()[:3]]

        # Encode the data using Hamming (12,8)
        hamming_code = calculate_hamming(datalist[i])

        # Modify the pixels based on the Hamming code
        for j in range(12):
            if (hamming_code[j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (hamming_code[j] == '1' and pix[j] % 2 == 0):
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
        yield pix[9:12]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
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

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = "stego-image/" + input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode data from image
def decode():
    img = "stego-image/" + input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    try:
        while True:
            # Extract 4 pixels (12 RGB values)
            pixels = [value for value in imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3]]

            # Extract the Hamming code
            binstr = ''
            for i in pixels[:12]:
                binstr += '0' if i % 2 == 0 else '1'

            # Correct any errors in the Hamming code
            corrected_binstr = correct_hamming(binstr)

            # Decode the Hamming (12,8) code
            data_bits = corrected_binstr[2] + corrected_binstr[4:7] + corrected_binstr[8:12]
            data += chr(int(data_bits, 2))

    except StopIteration:
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
