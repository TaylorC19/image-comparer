import os
import numpy as np
from PIL import Image
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to read images using Pillow to handle Unicode paths
def load_image(image_path):
    try:
        pil_image = Image.open(image_path)
        return np.array(pil_image)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

# Function to save images using Pillow
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

# Function to compare two color images
def compare_images_color(image1_path, image2_path):
    img1 = load_image(image1_path)
    img2 = load_image(image2_path)

    if img1 is None or img2 is None:
        return None, None
    
    # Check if the two images have the same shape (same dimensions and channels)
    if img1.shape != img2.shape:
        print(f"Skipping comparison: Images {image1_path} and {image2_path} do not have the same size.")
        
        return None, None

    # Compute the absolute difference between the images
    diff = cv2.absdiff(img1, img2)

    # Convert the difference to grayscale for visualization purposes
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Normalize the difference image for better visibility
    _, diff_thresh = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)

    return diff_thresh, None  # No similarity index

# Function to select a folder and display the selected path in the entry box
def select_folder(entry_widget):
    folder_selected = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)  # Clear the existing text in the entry box
    entry_widget.insert(0, folder_selected)  # Insert the selected folder path

# Function to run the comparison after the user selects the folders
def run_comparison():
    folder1 = folder1_entry.get()
    folder2 = folder2_entry.get()
    diff_folder = diff_folder_entry.get()

    if not folder1 or not folder2 or not diff_folder:
        messagebox.showerror("Error", "Please select all folders!")
        return

    if not os.path.exists(diff_folder):
        os.makedirs(diff_folder)

    non_black_images = []
    missing_images = []
    different_sizes = [] # add warning message if images are different sizes

    # Iterate through images in testFolder1
    for filename in os.listdir(folder1):
        if filename in os.listdir(folder2):
            img1_path = os.path.join(folder1, filename)
            img2_path = os.path.join(folder2, filename)

            # Compare images and get the difference
            diff_image, _ = compare_images_color(img1_path, img2_path)

            # Check if the diff image is not entirely black
            if diff_image is not None and not np.all(diff_image == 0):
                non_black_images.append(filename)
            if diff_image is None:
                different_sizes.append(filename)

            # Save the difference image using Pillow
            diff_output_path = os.path.join(diff_folder, f"diff_{filename}")
            save_image(diff_image, diff_output_path)
        else: # List files in folder 1 that are not in folder 2
            missing_images.append(f"{os.path.basename(folder1)}/{filename} is missing in {os.path.basename(folder2)}")

    # List files in folder 2 that are not in folder 1
    for filename in os.listdir(folder2):
        if filename not in os.listdir(folder1):
            missing_images.append(f"{os.path.basename(folder2)}/{filename} is missing in {os.path.basename(folder1)}")

    # create output message
    outputMessage = ''

    if non_black_images:
        output_file = os.path.join(diff_folder, "different_images.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            for img in non_black_images:
                f.write(img + "\n")
        outputMessage += f"List of different images saved to {os.path.basename(diff_folder)}/{os.path.basename(output_file)}\n"
    if missing_images:
        output_file = os.path.join(diff_folder, "missing_images.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            for img in missing_images:
                f.write(img + "\n")
        outputMessage += f"List of missing images saved to {os.path.basename(diff_folder)}/{os.path.basename(output_file)}\n"
    if different_sizes:
        output_file = os.path.join(diff_folder, "different_sizes.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            for img in different_sizes:
                f.write(img + "\n")
        outputMessage += f"List of different size image(s) saved to {os.path.basename(diff_folder)}/{os.path.basename(output_file)}"

    if outputMessage:
        messagebox.showinfo("Comparison Complete", outputMessage)
    else:
        messagebox.showinfo("No Differences", "No differences found in any images.")

    # Write non-black images to a text file with UTF-8 encoding
    # if non_black_images and missing_images:
    #     output_file = os.path.join(diff_folder, "different_images.txt")
    #     with open(output_file, "w", encoding="utf-8") as f:
    #         for img in non_black_images:
    #             f.write(img + "\n")
    #     output_file2 = os.path.join(diff_folder, "missing_images.txt")
    #     with open(output_file2, "w", encoding="utf-8") as f:
    #         for img in missing_images:
    #             f.write(img + "\n")
    #     messagebox.showinfo("Comparison Complete", f"List of different images saved to {os.path.basename(diff_folder)}/{os.path.basename(output_file)} \nand missing images saved to {os.path.basename(diff_folder)}/{os.path.basename(output_file2)}")
    # elif non_black_images:
    #     output_file = os.path.join(diff_folder, "different_images.txt")
    #     with open(output_file, "w", encoding="utf-8") as f:
    #         for img in non_black_images:
    #             f.write(img + "\n")
    #     messagebox.showinfo("Comparison Complete", f"List of different images saved to {os.path.basename(diff_folder)}/{os.path.basename(output_file)}")
    # elif missing_images:
    #     output_file1 = os.path.join(diff_folder, "missing_images.txt")
    #     with open(output_file1, "w", encoding="utf-8") as f:
    #         for img in missing_images:
    #             f.write(img + "\n")
    #     messagebox.showinfo("Comparison Complete", f"List of missing images saved to {os.path.basename(diff_folder)}/{os.path.basename(output_file)}")
    # else:
    #     messagebox.showinfo("No Differences", "No differences found in any images.")

# Create the main application window
root = tk.Tk()
root.title("Image Folder Comparison")

# Create a language selection dropdown
# language_var = tk.StringVar(value="English") #default English
# language_label = tk.Label(root, text="Select Language:")


# Create labels and entry widgets for folder paths
folder1_label = tk.Label(root, text="Select Folder 1:")
folder1_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
folder1_entry = tk.Entry(root, width=50)
folder1_entry.grid(row=1, column=1, padx=10, pady=5)
folder1_button = tk.Button(root, text="Browse", command=lambda: select_folder(folder1_entry))
folder1_button.grid(row=1, column=2, padx=10, pady=5)

folder2_label = tk.Label(root, text="Select Folder 2:")
folder2_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
folder2_entry = tk.Entry(root, width=50)
folder2_entry.grid(row=2, column=1, padx=10, pady=5)
folder2_button = tk.Button(root, text="Browse", command=lambda: select_folder(folder2_entry))
folder2_button.grid(row=2, column=2, padx=10, pady=5)

diff_folder_label = tk.Label(root, text="Select Output Folder:")
diff_folder_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
diff_folder_entry = tk.Entry(root, width=50)
diff_folder_entry.grid(row=3, column=1, padx=10, pady=5)
diff_folder_button = tk.Button(root, text="Browse", command=lambda: select_folder(diff_folder_entry))
diff_folder_button.grid(row=3, column=2, padx=10, pady=5)

# Create a button to start the comparison
run_button = tk.Button(root, text="Run Comparison", command=run_comparison)
run_button.grid(row=4, column=1, pady=20)

# Start the GUI event loop
root.mainloop()
