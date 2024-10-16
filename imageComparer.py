import cv2
import os
import numpy as np
from PIL import Image
import re
import tkinter as tk
from tkinter import filedialog

# Function to read images using Pillow to handle Unicode paths
def load_image(image_path):
    try:
        pil_image = Image.open(image_path)
        return np.array(pil_image)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

# Function to compare two images
def compare_images(image1_path, image2_path):
    img1 = load_image(image1_path)
    img2 = load_image(image2_path)

    if img1 is None or img2 is None:
        return None

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray1, gray2)
    _, diff_thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    return diff_thresh

# function that saves the image using Pillow
def save_image(image_data, save_path):
    try:
        if image_data.dtype != np.uint8:
            image_data = image_data.astype(np.uint8)

        if len(image_data.shape) == 2:  # Single-channel (grayscale)
            pil_image = Image.fromarray(image_data, mode='L')
        else:  # Multi-channel (e.g., RGB)
            pil_image = Image.fromarray(image_data)

        pil_image.save(save_path)
        print(f"Image saved to {save_path}")
    except Exception as e:
        print(f"Error saving image {save_path}: {e}")

# Function to sanitize filenames to ASCII
def sanitize_filename(filename):
    sanitized = re.sub(r'[^\x00-\x7F]', '_', filename)  # Replace non-ASCII characters with underscores
    return sanitized

# Folder selection using tkinter
def select_folder(prompt):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title=prompt)
    if not folder_selected:
        print("No folder selected.")
        exit()
    return folder_selected

# Folder paths
folder1 = select_folder("Select the first folder:")
folder2 = select_folder("Select the second folder:")
diff_folder = select_folder("Select the output folder:")

if not os.path.exists(diff_folder):
    os.makedirs(diff_folder)

non_black_images = []

# Iterate through images in testFolder1
for filename in os.listdir(folder1):
    if filename in os.listdir(folder2):
        img1_path = os.path.join(folder1, filename)
        img2_path = os.path.join(folder2, filename)

        # Compare images and get the difference
        diff_image = compare_images(img1_path, img2_path)

        if diff_image is None:
            print(f"Skipping {filename} due to loading error.")
            continue

        # Check if the diff image is not entirely black
        if not np.all(diff_image == 0):
            non_black_images.append(filename)

        # Sanitize the filename for saving
        sanitized_filename = sanitize_filename(filename)
        diff_output_path = os.path.join(diff_folder, f"diff_{filename}")

        # Save the difference image using Pillow
        save_image(diff_image, diff_output_path)

# Write non-black images to a text file with UTF-8 encoding
if non_black_images:
    output_file = "different_images.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for img in non_black_images:
            f.write(img + "\n")
    print(f"List of non-black images saved to {output_file}")
else:
    print("No differences found in any images.")
