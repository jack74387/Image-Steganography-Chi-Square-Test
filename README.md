# Image-Steganography-Chi-Square-Test
This repository contains research progress on various methods of image-based steganography, with a focus on experiments involving LSB (Least Significant Bit) encoding and analysis. The report highlights three experimental methods for data hiding: parity bit manipulation, Hamming code (12, 8), and LSB embedding.
## experiments
### three ways of image steganography
1. LSB Encoding
    - Overview
        - Hide data by modifying the least significant bit of pixel channels (R, G, B).
        - Encode data as 0 (even) or 1 (odd).
        - Use 3 pixels to encode one byte.
        - Maintain the 9th bit unchanged.
    - Result
        - The chi-square values increased significantly for the stego images, indicating higher detectability when more data was hidden.
2. Parity Bit Encoding
    - Overview
        - Hide data across 3 pixels, with the 9th bit as the even parity bit.
    - Result
        -  Chi-square values were slightly reduced compared to LSB-only encoding, suggesting slightly improved undetectability.
3. Hamming Code (12, 8)
    - Overview
        -  Use error-correcting codes to encode data redundantly and improve robustness.
        - Encode a byte using 4 pixels with 12 bits.
        - Apply Hamming Code (12, 8) for error correction.
    - Result
        - Hamming Code yielded lower chi-square values, making the stego images less detectable compared to parity bit and LSB methods.
### Setup
```bash
pip install pillow
pip install numpy opencv-python scipy
```
### Usage
- Eecode
    1. Prepare your cover image and place it in the `cover-image` directory.
    2. Create a text file containing the message you want to hide and place it in the `text` directory.
    3. Run the program and select the **Encode** option:
        ```bash
        python steganography.py
        ```
    4. Follow the prompts:
        - Enter the name of the cover image (with extension) located in `cover-image`.
        - Enter the name of the text file containing your message (with extension) located in `text`.
        - Provide a name for the new image (with extension) where the hidden message will be stored. The program saves the stego image in the `stego-image` directory.
- Decode
    1. Place the stego image (image with hidden message) in the `stego-image` directory.
    2. Run the program and select the **Decode** option:
        ```bash
        python steganography.py
        ```
    3. Enter the name of the stego image (with extension).
    4. The program will extract and display the hidden message.
- Analysis
    1. Run the program
        ```bash
        python chi-square-test.py
        ```
    2. Input Required Data
        - **Raw Image**: Enter the path to the original (cover) image without any hidden data.
        - **Secret Image**: Enter the path to the image suspected of containing hidden data.
## References
- [Image-Based Steganography Using Python](https://www.geeksforgeeks.org/image-based-steganography-using-python/)
- the source of cover image -> [dataset](https://sipi.usc.edu/database/database.php?volume=misc)
- the source of hiding text -> [J.K. Rowling - HP 1 - Harry Potter and the Sorcerer Stone](https://bbs.luobotou.org/bstra/thread-50013-1-1.html)