import os
import numpy as np
from PIL import Image
import cv2
from skimage.metrics import structural_similarity as ssim

# Function to read images using Pillow to handle Unicode paths
def load_image(image_path):
    try:
        pil_image = Image.open(image_path)
        return np.array(pil_image)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

# Function to save images using Pillow, ensuring proper conversion
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

# Function to compare two images using SSIM
def compare_images_ssim(image1_path, image2_path):
    img1 = load_image(image1_path)
    img2 = load_image(image2_path)

    if img1 is None or img2 is None:
        return None, None

    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    similarity_index, diff = ssim(gray1, gray2, full=True)
    
    # Normalize the difference image for better visibility
    diff = (diff * 255).astype("uint8")

    return diff, similarity_index

# Folder paths
folder1 = "original"
folder2 = "new"
diff_folder = "diffFolder"

if not os.path.exists(diff_folder):
    os.makedirs(diff_folder)

non_black_images = []

# Iterate through images in testFolder1
for filename in os.listdir(folder1):
    if filename in os.listdir(folder2):
        img1_path = os.path.join(folder1, filename)
        img2_path = os.path.join(folder2, filename)

        # Compare images and get the difference and similarity index
        diff_image, similarity_index = compare_images_ssim(img1_path, img2_path)

        # Check if the similarity index indicates significant differences
        if similarity_index is not None and similarity_index < 0.95:  # Adjust threshold as needed
            non_black_images.append(filename)

        # Save the difference image using Pillow
        diff_output_path = os.path.join(diff_folder, f"diff_{filename}")
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
