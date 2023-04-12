# specifiy data augmentation

import pandas as pd
import numpy as np
import os
import shutil

# Load annotations file
annotations_file = pd.read_csv('/content/drive/My Drive/CelebA/Anno/list_attr_celeba.txt', delim_whitespace=True, skiprows=1)

# Set variable to image directory
img_dir = '/content/drive/My Drive/CelebA/Img/img_align_celeba_6500'

# Define list of class names (subset of the classes listed in `list_attr_celeba.txt`)
class_names = ['Arched_Eyebrows', 'Bags_Under_Eyes', 'Bangs', 'Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Eyeglasses', 'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones', 'Mouth_Slightly_Open', 'Mustache', 'Narrow_Eyes', 'Rosy_Cheeks', 'Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Earrings', 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace']
# define the positions of the classes to be used
used_classes = [1, 3, 5, 8, 9, 11, 15, 17, 18, 19, 21, 22, 23, 29, 31, 32, 33, 34, 35, 36, 37]
used_classes_set = set(used_classes)

print(class_names)
print(f"Expected 41 columns in annotations file, found {len(class_names)}")

# set number of images to process
training_size = 100

# define a dictionary 'class_directories_counters'
class_directories_counters = np.zeros(len(class_names), dtype=int)

# loop over the annotations file and find labels
for i in range(training_size):
  # get filename
  fileName = annotations_file.iloc[i, 0]
  print(">>-----------------------------------<<")
  print(f"Current file: {fileName}")

  # Check if filename exists in image directory
  if not os.path.exists(os.path.join(img_dir, fileName)):
    print(f"{fileName} does not exist in image directory, skipping")
    continue

  # define a vector of type string and size 21
  class_placement_counters = np.zeros(len(class_names), dtype=int)
 
  # define label_counter and vector_counter
  label_counter = -1
  vector_counter = -1
  
  # Loop over class flags, skipping the positions not in this list: [1, 3, 5, 8, 9, 11, 15, 17, 18, 19, 21, 22, 23, 29, 31, 32, 33, 34, 35, 36, 37]
  for j in range(0, 39):
    # switch statement to check if j is any value in used_classes_set
    if j in used_classes_set:
      # increment label_counter
      label_counter += 1
      # check if the current class flag is true
      if annotations_file.iloc[i, j+1] == 1:
        # increment vector_counter
        vector_counter += 1
        # add a class index to class_placement_counters
        class_placement_counters[vector_counter] = label_counter
      else: 
       # do nothing
        continue
    else:
      continue
  # remove empty trailing entries from class_placement_counters
  class_placement_counters = class_placement_counters[0:vector_counter+1]

  # find the least element of class_directories_counters within the indices in class_placement_counters:
  for k in range(len(class_placement_counters)):
    # find the applicable class directory with the fewest items and assign it to placedClass
    if class_directories_counters[class_placement_counters[k]] == class_directories_counters[class_placement_counters].min():
      placedClass = class_placement_counters[k]
      class_directories_counters[placedClass] += 1
      break 

  # if the directory name at placedClass in class_names doesn't exist, create it
  if not os.path.exists(os.path.join('/content/drive/My Drive/CelebA/Img/train', class_names[placedClass])):
    os.makedirs(os.path.join('/content/drive/My Drive/CelebA/Img/train', class_names[placedClass]))
    
  # copy file fileName to the directory name at placedCLass in class_names
  shutil.copy(os.path.join(img_dir, fileName), os.path.join('/content/drive/My Drive/CelebA/Img/train', class_names[placedClass]))
  # alternatively, move file fileName to the directory name at placedClass in class_names
 # shutil.move(os.path.join(img_dir, fileName), os.path.join('/content/drive/My Drive/CelebA/Img/train', class_names[placedClass]))

 
  # Print progress message
  print(f"File {fileName} placed in {class_names[placedClass]}.")
  print(f"File {i+1} of {training_size} processed")
  print(f"Directories counters: {class_directories_counters}")


