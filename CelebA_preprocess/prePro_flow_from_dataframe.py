# specifiy data augmentation

import pandas as pd
import numpy as np
import os

# Load annotations file
annotations_file = pd.read_csv('/content/drive/My Drive/CelebA/Anno/list_attr_celeba.txt', delim_whitespace=True, skiprows=1)

# Set variable to image directory
img_dir = '/content/drive/My Drive/CelebA/Img/img_align_celeba_6500'

# Define list of class names (subset of the classes listed in `list_attr_celeba.txt`)
class_names = ['Arched_Eyebrows', 'Bags_Under_Eyes', 'Bangs', 'Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Eyeglasses', 'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones', 'Mouth_Slightly_Open', 'Mustache', 'Narrow_Eyes', 'Rosy_Cheeks', 'Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Earrings', 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace']
# define the positions of the classes to be used
used_classes = [1, 3, 5, 8, 9, 11, 15, 17, 18, 19, 21, 22, 23, 29, 31, 32, 33, 34, 35, 36, 37]
# define a list of class placement counters, one for each image
class_placement = np.zeros(6500)
print(class_names)
print(f"Expected 41 columns in annotations file, found {len(class_names)}")

# create a define a list of 2 dimensions, type = string,  rows = 6500, columns = 41
labelsList = np.zeros((6500, 2), dtype=object)

# Set number of images to process
training_size = 6500

# Loop over the annotations file and find labels
for i in range(training_size):
  # Get filename
  fileName = annotations_file.iloc[i, 0]
  print(">>-----------------------------------<<")
  print(f"Current file: {fileName}")

  # Check if filename exists in image directory
  if not os.path.exists(os.path.join(img_dir, fileName)):
    print(f"{fileName} does not exist in image directory, skipping")
    continue

  # add fileName to first column of labelsList
  labelsList[i, 0] = fileName

  # define a vector of type string and size 21
  #label_vector = np.zeros(len(class_names), dtype='U20')
  # define a list 'label_vector' of length 21 and type string
  label_vector = [''] * 21

  # define label_counter and vector_counter
  label_counter = -1
  vector_counter = -1
  
  # Loop over class flags, skipping the positions not in this list: [1, 3, 5, 8, 9, 11, 15, 17, 18, 19, 21, 22, 23, 29, 31, 32, 33, 34, 35, 36, 37]
  for j in range(0, 39):
    # switch statement to check if j is any value in used_classes
    if j in used_classes:
      # increment label_counter
      label_counter += 1
      # check if the current class flag is true
      if annotations_file.iloc[i, j+1] == 1:
        # increment vector_counter
        vector_counter += 1
        # add a class name to label_vector
        label_vector[vector_counter] = class_names[label_counter]
        # increment class placement counter
        class_placement[i] += 1
        # print(f"Going to {class_names[label_counter]}")
      else: 
       # do nothing
        continue
    else:
      continue
  # remove empty trailing entries from label_vector
  label_vector = label_vector[0:vector_counter+1]
  # remove single quotes around each entry in label_vector except the last entry
  label_vector = '[%s]' % ', '.join(map(str, label_vector))
  # Add label_vector to labelsList in the second column
  labelsList[i, 1] = label_vector

  # Print progress message
  print(f"{fileName} added to {int(class_placement[i].sum())} classes")
  # print the current row and all columns of labelsList
  print(label_vector)
  print(type(label_vector))

# create and define 'labels.csv' using pd
labels = pd.DataFrame(data=labelsList)
# set column names to 'filenames' and 'labels'
labels.columns = ['filenames', 'labels']
# save labels.csv to drive
labels.to_csv('/content/drive/My Drive/CelebA/Anno/labels.csv', index=False)

