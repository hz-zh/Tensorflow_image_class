# specifiy data augmentation

import pandas as pd
import numpy as np
import os
import shutil
from PIL import Image

# Load annotations file
annotations_file = pd.read_csv('/content/drive/My Drive/CelebA/Anno/list_attr_celeba.txt', delim_whitespace=True, skiprows=1)

# Load bbox file
bbox_file = pd.read_csv('/content/drive/My Drive/CelebA/Anno/list_bbox_celeba.txt', delim_whitespace=True, skiprows=1)
print(bbox_file)
# Set variables to paths
img_dir = '/content/drive/My Drive/CelebA/Img/img_align_celeba'
output_dir = '/content/drive/My Drive/CelebA/Img/preprocessed'
if not os.path.exists(output_dir):
  os.makedirs(output_dir)

# Define list of class names
class_names = annotations_file.columns.tolist()
classPlacement = np.zeros(6500)
print(class_names)
print(f"Expected 41 columns in annotations file, found {len(class_names)}")

# Set image number
training_size = 5

# Loop over the annotations file and preprocess images
for i in range(training_size):
  # Get filename
  fileName = annotations_file.iloc[i, 0]
  print(">>-----------------------------------<<")
  print(f"Current file: {fileName}")

  # Check if filename exists in image directory
  if not os.path.exists(os.path.join(img_dir, fileName)):
    print(f"{fileName} does not exist in image directory, skipping")
    continue
  
   # open image and crop it to the size of the bbox for the current class, if it exists
   # _________________________________________________________________________________
   # Opens a image in RGB mode
  print(f"Opening from {img_dir}/{fileName}")
  im = Image.open(f"{img_dir}/{fileName}")
 
   # Setting the points for cropped image
  left = bbox_file.iloc[i, 1]
  top = bbox_file.iloc[i, 2]
  right = bbox_file.iloc[i, 3]
  bottom = bbox_file.iloc[i, 4]

  print(left, top, right, bottom)
      
   # Cropped image of above dimension
   # (It will not change original image)
  cropped = im.crop((left, top, right, bottom))
  cropped = cropped.convert('jpg')

  # create output directory if it doesn't exist
  output_dir_cropped = '/content/drive/My Drive/CelebA/Img/cropped'
  if not os.path.exists(output_dir_cropped):
      os.makedirs(output_dir_cropped)

  # save cropped image to file
  output_path = os.path.join(output_dir_cropped, fileName)
  cropped.save(output_path)

  cropped.show()

  # save `cropped` to a directory at `f"/content/drive/My Drive/CelebA/Img/cropped/{fileName}"`
  # if the directory doesn't exist, create it 
  # ________________________________________________

  # Loop over class flags
  for j in range(1, len(class_names)):
    if annotations_file.iloc[i, j] == 1:
      # Get class name
      class_name = class_names[j]
      # Get output path
      outputPath = os.path.join(output_dir, class_name)

      print(f"Image {fileName} is going to... {class_name}")

      # If output path does not exist, create it
      if not os.path.exists(outputPath):
        os.makedirs(outputPath)
        print(f"Creating new directory at  {outputPath}…")

      # Copy image to output path
      src_path = os.path.join(img_dir, fileName)
      dst_path = os.path.join(outputPath, fileName)
      shutil.copyfile(src_path, dst_path)

      # Increment class placement counter
      classPlacement[i] += 1

    else:
      continue

  # Print progress message
  print(f"{fileName} added to {int(classPlacement[i].sum())} classes")
  print("<<----------------------------------->>")

