import os
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Set up directories and paths
data_dir = '/content/drive/My Drive/CelebA'
img_dir = os.path.join(data_dir, 'Img', 'img_align_celeba_6500')
labels_file = os.path.join(data_dir, 'Anno', 'labels.csv')

# Load the labels into a DataFrame
df = pd.read_csv(labels_file, index_col=0)

# Sort the list of filenames in img_dir alphabetically
filenames = sorted(os.listdir(img_dir))

# Create an ImageDataGenerator for data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

# Create the train and validation generators
train_generator = datagen.flow_from_dataframe(
    df,
    directory=filenames,
    x_col='index',
    y_col=df.columns.tolist(),
    target_size=(128, 128),
    batch_size=32,
    class_mode='raw',
    shuffle=True,
    subset='training'
)

val_generator = datagen.flow_from_dataframe(
    df,
    directory=filenames,
    x_col='index',
    y_col=df.columns.tolist(),
    target_size=(128, 128),
    batch_size=32,
    class_mode='raw',
    shuffle=True,
    subset='validation'
)
