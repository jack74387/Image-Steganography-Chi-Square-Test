import numpy as np
import cv2
from scipy.stats import chi2

# Function to calculate LSB counts for a single channel
def calculate_lsb_counts(channel_data):
    lsb_0_count = 0
    lsb_1_count = 0

    # Count LSBs
    for value in channel_data:
        lsb = value & 1
        if lsb == 0:
            lsb_0_count += 1
        else:
            lsb_1_count += 1

    return lsb_0_count, lsb_1_count

# Function to calculate chi-square statistic given LSB counts
def calculate_chi_square(lsb_0_count, lsb_1_count):
    
    # Expected frequency (uniform distribution)
    expected_count = (lsb_0_count + lsb_1_count) / 2

    # Calculate chi-square statistic
    chi_square_stat = ((lsb_0_count - expected_count) ** 2 / expected_count) + \
                      ((lsb_1_count - expected_count) ** 2 / expected_count)

    return chi_square_stat

# Separate RGB channels
def extract_channels(data):
    r_channel = [pixel[0] for pixel in data]
    g_channel = [pixel[1] for pixel in data]
    b_channel = [pixel[2] for pixel in data]
    return r_channel, g_channel, b_channel

# Load the image
raw_image_text = "cover-image/" + input("Enter raw image:")
raw_image = cv2.imread(raw_image_text)
raw_image_rgb = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
secret_image_text = "stego-image/" + input("Enter secret image:")
secret_image = cv2.imread(secret_image_text)
secret_image_rgb = cv2.cvtColor(secret_image, cv2.COLOR_BGR2RGB)

# Flatten the image data to extract all pixels
height, width, _ = raw_image_rgb.shape
raw_data = raw_image_rgb.reshape((height * width, 3))

height, width, _ = secret_image_rgb.shape
secret_data = secret_image_rgb.reshape((height * width, 3))

# Extract raw and secret channels
raw_r, raw_g, raw_b = extract_channels(raw_data)
secret_r, secret_g, secret_b = extract_channels(secret_data)

# Calculate LSB counts for each channel
raw_r_lsb_0, raw_r_lsb_1 = calculate_lsb_counts(raw_r)
raw_g_lsb_0, raw_g_lsb_1 = calculate_lsb_counts(raw_g)
raw_b_lsb_0, raw_b_lsb_1 = calculate_lsb_counts(raw_b)
secret_r_lsb_0, secret_r_lsb_1 = calculate_lsb_counts(secret_r)
secret_g_lsb_0, secret_g_lsb_1 = calculate_lsb_counts(secret_g)
secret_b_lsb_0, secret_b_lsb_1 = calculate_lsb_counts(secret_b)

# Calculate chi-square statistics for each channel
raw_r_chi = calculate_chi_square(raw_r_lsb_0, raw_r_lsb_1)
raw_g_chi = calculate_chi_square(raw_g_lsb_0, raw_g_lsb_1)
raw_b_chi = calculate_chi_square(raw_b_lsb_0, raw_b_lsb_1)
secret_r_chi = calculate_chi_square(secret_r_lsb_0, secret_r_lsb_1)
secret_g_chi = calculate_chi_square(secret_g_lsb_0, secret_g_lsb_1)
secret_b_chi = calculate_chi_square(secret_b_lsb_0, secret_b_lsb_1)

# Combine LSB counts for all channels
raw_combined_lsb_0 = raw_r_lsb_0 + raw_g_lsb_0 + raw_b_lsb_0
raw_combined_lsb_1 = raw_r_lsb_1 + raw_g_lsb_1 + raw_b_lsb_1
secret_combined_lsb_0 = secret_r_lsb_0 + secret_g_lsb_0 + secret_b_lsb_0
secret_combined_lsb_1 = secret_r_lsb_1 + secret_g_lsb_1 + secret_b_lsb_1


# Calculate chi-square statistic for combined channels
raw_combined_chi = calculate_chi_square(raw_combined_lsb_0, raw_combined_lsb_1)
secret_combined_chi = calculate_chi_square(secret_combined_lsb_0, secret_combined_lsb_1)

# Critical value for chi-square test
critical_value = chi2.ppf(0.95, df=1)

# Print LSB counts
print("\nLSB Counts:")
print(f"R Channel - raw LSB 0: {raw_r_lsb_0}, raw LSB 1: {raw_r_lsb_1}, secret LSB 0: {secret_r_lsb_0}, secret LSB 1: {secret_r_lsb_1}")
print(f"G Channel - raw LSB 0: {raw_g_lsb_0}, raw LSB 1: {raw_g_lsb_1}, secret LSB 0: {secret_g_lsb_0}, secret LSB 1: {secret_g_lsb_1}")
print(f"B Channel - raw LSB 0: {raw_b_lsb_0}, raw LSB 1: {raw_b_lsb_1}, secret LSB 0: {secret_b_lsb_0}, secret LSB 1: {secret_b_lsb_1}")
print(f"Combined - raw LSB 0: {raw_combined_lsb_0}, raw LSB 1: {raw_combined_lsb_1}, secret LSB 0: {secret_combined_lsb_0}, secret LSB 1: {secret_combined_lsb_1}")

# Output results
print("Raw Data Chi-Square Statistics:")
print(f"R Channel: {raw_r_chi}, G Channel: {raw_g_chi}, B Channel: {raw_b_chi}")
print(f"Combined Channels: {raw_combined_chi}")
print("Secret Data Chi-Square Statistics:")
print(f"R Channel: {secret_r_chi}, G Channel: {secret_g_chi}, B Channel: {secret_b_chi}")
print(f"Combined Channels: {secret_combined_chi}")
print("\nCritical Value (significance level = 0.05):", critical_value)

# Interpret results for secret data
def interpret_results(channel_name, chi_square_stat):
    if chi_square_stat > critical_value:
        print(f"Possible steganography detected in {channel_name} channel!")
    else:
        print(f"No steganography detected in {channel_name} channel.")

interpret_results("R", raw_r_chi)
interpret_results("G", raw_g_chi)
interpret_results("B", raw_b_chi)
interpret_results("Combined", raw_combined_chi)
interpret_results("R", secret_r_chi)
interpret_results("G", secret_g_chi)
interpret_results("B", secret_b_chi)
interpret_results("Combined", secret_combined_chi)