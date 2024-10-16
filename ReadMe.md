# Image Comparer v2
## Setup
1. Install Python and Dependencies
First, ensure that you have Python installed on your system. To install the required dependencies, follow these steps:

Optional (Recommended): Create a Virtual Environment
It’s a good idea to create a virtual environment to keep dependencies isolated. Run the following command to create a virtual environment:

```
python -m venv .venv
```

Activate the Environment:
Windows:

```
source .venv/Scripts/activate
```

macOS/Linux:

```
source .venv/bin/activate
```

2. Install Dependencies
With the environment activated (if using), install the required dependencies by running:

```
pip install -r requirements.txt
```

in your terminal.

## Running the Application
1. Navigate to the Root Folder
Open your terminal and navigate to the folder where imageComparer-v2.py is located.

2. Run the Application
Execute the following command to start the application:

```
python imageComparer-v2.py
```

## How to Use the Application
1. Prepare the Image Folders
Make sure you have two folders, each containing images with the same file names and types in both folders (e.g., image1.jpg in both Folder A and Folder B).

2. Select the Folders for Comparison
First, select the first folder to compare.
Next, select the second folder to compare.
3. Select the Output Folder
Choose an output folder. This is where the differences between the images, as well as any generated text files, will be saved.

You're now ready to compare images! The application will output the differences in the chosen folder.