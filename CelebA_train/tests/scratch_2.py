history_frame = pd.DataFrame(history.history)
history_frame.loc[:, [ 
                  'val_Arched_Eyebrows_accuracy',
                  'val_Bags_Under_Eyes_accuracy',
                  'val_Bangs_accuracy',
                  'val_Black_Hair_accuracy',
                  'val_Blond_Hair_accuracy',
                     ]].plot()
plt.xlabel('Epochs')
plt.ylabel('Validation Accuracy')
history_frame.loc[:, [
                  'val_Brown_Hair_accuracy',
                  'val_Eyeglasses_accuracy',
                  'val_Gray_Hair_accuracy',
                  'val_Heavy_Makeup_accuracy',
                  'val_High_Cheekbones_accuracy',
                     ]].plot()
plt.xlabel('Epochs')
plt.ylabel('Validation Accuracy')
history_frame.loc[:, [
                  'val_Mouth_Slightly_Open_accuracy',
                  'val_Mustache_accuracy',
                  'val_Narrow_Eyes_accuracy',
                  'val_Rosy_Cheeks_accuracy',
                  'val_Smiling_accuracy',
                     ]].plot()
plt.xlabel('Epochs')
plt.ylabel('Validation Accuracy')
history_frame.loc[:, [
                  'val_Straight_Hair_accuracy',
                  'val_Wavy_Hair_accuracy',
                  'val_Wearing_Earrings_accuracy',
                  'val_Wearing_Hat_accuracy',
                  'val_Wearing_Lipstick_accuracy',
                  'val_Wearing_Necklace_accuracy',
                  ]].plot()
plt.xlabel('Epochs')
plt.ylabel('Validation Accuracy')

history_frame.loc[:, [ 
                  'Arched_Eyebrows_loss',
                  'Bags_Under_Eyes_loss',
                  'Bangs_loss',
                  'Black_Hair_loss',
                  'Blond_Hair_loss',
                  ]].plot()
plt.xlabel('Epochs')
plt.ylabel('Training Loss')
history_frame.loc[:, [
                  'Brown_Hair_loss',
                  'Eyeglasses_loss',
                  'Gray_Hair_loss',
                  'Heavy_Makeup_loss',
                  'High_Cheekbones_loss',
                  ]].plot()
plt.xlabel('Epochs')
plt.ylabel('Training Loss')
history_frame.loc[:, [
                  'Mouth_Slightly_Open_loss',
                  'Mustache_loss',
                  'Narrow_Eyes_loss',
                  'Rosy_Cheeks_loss',
                  'Smiling_loss',
                  ]].plot()
plt.xlabel('Epochs')
plt.ylabel('Training Loss')
history_frame.loc[:, [
                  'Straight_Hair_loss',
                  'Wavy_Hair_loss',
                  'Wearing_Earrings_loss',
                  'Wearing_Hat_loss',
                  'Wearing_Lipstick_loss',
                  'Wearing_Necklace_loss',
                  ]].plot()
plt.xlabel('Epochs')
plt.ylabel('Training Loss')


imagePreds = []

print(predictions[20][14][0])
for i in range(21):
  classPreds = []
  for j in range(15):
    classPreds.append(predictions[i][j][0])
  imagePreds.append(classPreds)

for i in range(15):
   # create a new list with the name 'image{i}'
   exec(f'image{i} = []')
   for j in range(21):
      exec(f'image{i}.append(imagePreds[j][i])')
   