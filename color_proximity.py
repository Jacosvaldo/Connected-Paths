# -*- coding: utf-8 -*-
"""Color Proximity

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iQlEFj8Vw7uqUOZscTPXh1KdJObF2Z9p

#How to use
<font size=4>To use it, just run the code blocks one by one, reading and following the notes.
This first block of code will probably return "Requirement already satisfied", it was here just for precaution</font>
"""

pip install pillow numpy pandas

"""#Upload your archive

<font size=4>Run the code block below and a button to upload your archives will appear below it
Upload the texture archives, not the zip or the folder, you can get a zip with all the block textures (version 1.21) [here](https://drive.google.com/file/d/1rHnYbSPcGSj5UmAsKTScUTLzUAMUovru/view?usp=sharing) and a spreadsheet comparing all the texturess [here](https://docs.google.com/spreadsheets/d/1qa-kvz-ej8CGpITm65_nWaHIFwjSY2cM/edit?usp=sharing&ouid=105034559760310195424&rtpof=true&sd=true)
</font>
"""

import os
import shutil
from google.colab import files

# Create the 'input' folder if it does not exist
if not os.path.exists('input'):
    os.makedirs('input')

# Clear the 'input' folder if there are any files in it
for filename in os.listdir('input'):
    file_path = os.path.join('input', filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Allow file upload
uploaded_files = files.upload()

# Move the uploaded files to the 'input' folder
for filename in uploaded_files.keys():
    shutil.move(filename, 'input/')

print("Files uploaded and moved to the 'input' folder:")
print(os.listdir('input'))

"""# Download

<font size=4>Just run the code block below and a spreadsheet will be downloaded</font>
"""

from PIL import Image
import numpy as np
import pandas as pd

# Function to calculate the average color of an image
def calculate_average_color(image_path):
    image = Image.open(image_path).convert('RGB')  # Convert to RGB
    image = image.resize((16, 16))  # Ensure the image is 16x16
    pixels = np.array(image)
    average_color = pixels.mean(axis=(0, 1))
    return average_color

# Function to calculate color difference (using Euclidean distance)
def calculate_difference(color1, color2):
    return np.linalg.norm(color1 - color2)

# Load all images from the 'input' folder
input_folder = 'input'
images = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Calculate the average color of each image
average_colors = {}
for image in images:
    image_path = os.path.join(input_folder, image)
    average_colors[image] = calculate_average_color(image_path)

# Compare the average colors and store differences less than 30
results = {image: [] for image in images}
for img1, color1 in average_colors.items():
    for img2, color2 in average_colors.items():
        if img1 != img2:
            difference = calculate_difference(color1, color2)
            if difference < 30:
                results[img1].append((img2, difference))

# Find the maximum length of the lists
max_len = max(len(lst) for lst in results.values())

# Standardize the length of the lists by filling with empty values
for image in images:
    while len(results[image]) < max_len:
        results[image].append(("", ""))

# Create the spreadsheet with the results
df = pd.DataFrame({image: [f"{img2}: {dif:.2f}" if img2 else "" for img2, dif in results[image]] for image in images})

# Save the spreadsheet
df.to_excel('color_comparison_results.xlsx', index=False)

print("Spreadsheet generated successfully!")

# Provide a download link
from google.colab import files
files.download('color_comparison_results.xlsx')