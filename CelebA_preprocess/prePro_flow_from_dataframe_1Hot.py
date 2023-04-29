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
labelsList = np.zeros((6500, 22), dtype=object)

# Set number of images to process
training_size = 100

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

  # define label_counter
  label_counter = 0
  
  # Loop over class flags, skipping the positions not in this list: [1, 3, 5, 8, 9, 11, 15, 17, 18, 19, 21, 22, 23, 29, 31, 32, 33, 34, 35, 36, 37]
  for j in range(0, 39):
    # switch statement to check if j is any value in used_classes
    if j in used_classes:
      # increment label_counter
      label_counter += 1
      # check if the current class flag is true
      if annotations_file.iloc[i, j+1] == 1:
        # add a flag to labelsList
        labelsList[i, label_counter] = 1
        # increment class placement counter
        class_placement[i] += 1
        print(f"Going to {class_names[label_counter]}")
      else: 
       # do nothing
        continue
    else:
      continue

  # Print progress message
  print(f"Image {fileName} placed into {class_placement[i]} classes")

# create and define 'labels.csv' using pd
labels = pd.DataFrame(data=labelsList)
# set column names to 'filenames' and 'labels'
labels.columns = ['filenames', 'Arched_Eyebrows', 'Bags_Under_Eyes', 'Bangs', 'Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Eyeglasses', 'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones', 'Mouth_Slightly_Open', 'Mustache', 'Narrow_Eyes', 'Rosy_Cheeks', 'Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Earrings', 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace']
# save labels.csv to drive
labels.to_csv('/content/drive/My Drive/CelebA/Anno/labels.csv', index=False)

