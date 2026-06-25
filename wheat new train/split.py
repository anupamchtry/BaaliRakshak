import splitfolders
import os

input_folder = 'C:/Users/anupa/Downloads/CROP DISEASE DETECTION/NEW TRAINED/wheat new train/main'
output_folder = 'C:/Users/anupa/Downloads/CROP DISEASE DETECTION/NEW TRAINED/wheat new train/main2'

# Check the structure of the input folder
print("Input folder contents:", os.listdir(input_folder))

# Check contents of each subfolder
for subfolder in os.listdir(input_folder):
    subfolder_path = os.path.join(input_folder, subfolder)
    if os.path.isdir(subfolder_path):
        print(f"Contents of {subfolder}: {os.listdir(subfolder_path)}")

print("Starting the folder split...")

# Split the folders into train, val, and test
splitfolders.ratio(input_folder, output=output_folder, 
                   seed=42, ratio=(.7, .2, .1), 
                   group_prefix=None)

print(f"Splitting completed. Check the {output_folder} directory.")
