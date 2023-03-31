# specify data augmentation
# 1
# 
import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import tensorflow_datasets as tfds

from google.colab import drive
drive.mount('/content/drive')

from pathlib import PosixPath as px
data_dir = px("/content/drive/My Drive/CelebA/Img/preprocessed")

image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)

batch_size = 24
img_height = 150
img_width = 150
# Use mixed precision
tf.keras.mixed_precision.set_global_policy('mixed_float16')

# Use tf.data for input pipelines
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

train_ds = train_ds.shuffle(buffer_size=1000).cache().prefetch(buffer_size=tf.data.AUTOTUNE)
val_ds = val_ds.shuffle(buffer_size=1000).cache().prefetch(buffer_size=tf.data.AUTOTUNE)

# Use early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)

num_classes = 40

# Use a smaller model
model = tf.keras.Sequential([
  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.Conv2D(8, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(8, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(32, activation='relu'),
  tf.keras.layers.Dense(num_classes)
])

# Compile the model with mixed precision and the Adam optimizer
opt = tf.keras.optimizers.Adam()
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
acc = tf.keras.metrics.SparseCategoricalAccuracy()
model.compile(optimizer=opt, loss=loss, metrics=[acc])

# Normalize the images using map() method
normalization_layer = tf.keras.layers.Rescaling(1./255)
normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y), num_parallel_calls=tf.data.AUTOTUNE)

class PrintMetricsCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print("Epoch:", epoch+1, "- Train Loss:", logs['loss'], "- Train Accuracy:", logs['sparse_categorical_accuracy'], "- Val Loss:", logs['val_loss'], "- Val Accuracy:", logs['val_sparse_categorical_accuracy'])

# Train the model with mixed precision, early stopping, and the print metrics callback
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=10,
  callbacks=[early_stopping, PrintMetricsCallback()],
  verbose=2
)

history.save('/content/drive/My Drive/CelebA/model/saved_model')
