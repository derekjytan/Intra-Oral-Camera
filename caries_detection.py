# Import necessary libraries
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from PIL import Image
from sklearn.metrics import roc_curve, auc
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.regularizers import l2
import warnings
from sklearn.exceptions import UndefinedMetricWarning

# Set paths
train_dir = '/Users/derbear/Documents/Work/IOC/teeth_dataset/Trianing'
test_dir = '/Users/derbear/Documents/Work/IOC/teeth_dataset/test'

# Count the number of images in each class
train_caries_count = len(os.listdir(os.path.join(train_dir, 'caries')))
train_no_caries_count = len(os.listdir(os.path.join(train_dir, 'without_caries')))
test_caries_count = len(os.listdir(os.path.join(test_dir, 'caries')))
test_no_caries_count = len(os.listdir(os.path.join(test_dir, 'no-caries')))

# Define the target image size
target_size = (224, 224)


# Loading training sets


# Load caries images as a NumPy array
caries_image_paths = [os.path.join(train_dir, 'caries', filename) for filename in os.listdir(os.path.join(train_dir, 'caries'))]
caries_images = []
for img_path in caries_image_paths:
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    caries_images.append(img_array)
caries_images = np.array(caries_images)

# Load no caries images as a NumPy array
no_caries_image_paths = [os.path.join(train_dir, 'without_caries', filename) for filename in os.listdir(os.path.join(train_dir, 'without_caries'))]
no_caries_images = []
for img_path in no_caries_image_paths:
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    no_caries_images.append(img_array)
no_caries_images = np.array(no_caries_images)

# Plot histograms of pixel values
# pixel value represents the intensity or color of a single pixel in an image
# 50 bins to be more accurate holding pixel values 0-255
plt.figure(figsize=(10, 6))
plt.hist(caries_images.flatten(), bins=50, color='blue', alpha=0.5, label='Caries')
plt.hist(no_caries_images.flatten(), bins=50, color='orange', alpha=0.5, label='No Caries')

def display_samples(class_name, directory):
    plt.figure(figsize=(12, 6))
    #display 4 sample images in subplots
    for i in range(4):
        image_path = os.path.join(directory, class_name, os.listdir(os.path.join(directory, class_name))[i])
        img = Image.open(image_path)
        plt.subplot(1, 4, i + 1)
        plt.imshow(img)
        plt.title(class_name)
        plt.axis('off')
    plt.show()

display_samples('caries', train_dir)
display_samples('without_caries', train_dir)

# augment image data
#applying random image movements to allow for larger data sets

train_datagen = ImageDataGenerator(
    
    rescale=1.0/255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_datagen.flow_from_directory(
    train_dir,          # directory
    target_size=(224, 224), #size image
    batch_size=32, # number images
    class_mode='binary' #carries vs no carries (1 vs 0)
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)


def display_augmented_images(class_name, directory, generator):
    plt.figure(figsize=(12, 6))
    for i in range(4):
        original_image_path = os.path.join(directory, class_name, os.listdir(os.path.join(directory, class_name))[i])
        original_img = Image.open(original_image_path)
        
        # Convert PIL Image to NumPy array
        original_array = np.array(original_img)
        
        # Apply random transformation to the NumPy original array
        augmented_array = generator.random_transform(original_array)
        
        augmented_img = Image.fromarray(augmented_array)
        
        plt.subplot(2, 4, i + 1)
        plt.imshow(original_img)
        plt.title(f'Original {class_name}')
        plt.axis('off')
        
        plt.subplot(2, 4, i + 5)
        plt.imshow(augmented_img)
        plt.title(f'Augmented {class_name}')
        plt.axis('off')
    
    plt.show()

# Display augmented images for 'caries' class
display_augmented_images('caries', train_dir, train_datagen)

# Display augmented images for 'no_caries' class
display_augmented_images('without_caries', train_dir, train_datagen)

# Model with regularization: convolutional neural network
# CNN has convolutional intemediate layers its not just a start and end layer like typical NN
# filters on layers detect data patterns 
# filters are matricies with random numbers
# 3x3 filter goes over every 3x3 pixels in the entire image = convolving
# to calculate: dot product of 3x3 pixels in the input image and the 3x3 filter = resultant colvolved image in pixel 1
# if there are spots on the initial image that are the same colour, their dot product will be the same because their pixels will be the same, meaning they create the same convolved image
# This becomes the next layers input
# video: https://www.youtube.com/watch?v=YRhxdVk_sIs


model = Sequential() # one task after another
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
# 32 = filters
# 3,3 = filter matrix size
# Rectified Linear Unit creates non-linearity
# shape of input images 224 x 224 pixels 3 rgb colour


model.add(MaxPooling2D((2, 2)))
# pooling reduces layers by performing operations like max, average, etc..
# example: 2x2 means you take the max value out of those 4

model.add(Flatten())
# make 2d to 1d for dense layers

model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01)))  # L2 regularization
#128 neurons

model.add(Dropout(0.5))  # Dropout
# prevent overfitting
model.add(Dense(1, activation='sigmoid'))
# outputs 0-1 carrie or no carrie

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    # how many batches of samples per model iteration
    epochs=10,
    #train 10 times
    validation_data=test_generator,
    validation_steps=len(test_generator)
)

# Model evaluation
test_loss, test_acc = model.evaluate(test_generator, steps=len(test_generator))
print(f"Test accuracy: {test_acc:.2f}")

# Generate predictions
predictions = model.predict(test_generator)
y_pred = np.round(predictions)

# Suppress UndefinedMetricWarning warnings
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

# Confusion matrix and classification report to evaluate model
conf_matrix = confusion_matrix(test_generator.classes, y_pred)
class_names = list(test_generator.class_indices.keys())

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print(classification_report(test_generator.classes, y_pred, target_names=class_names))

# Remove the filter after using
warnings.filterwarnings("default", category=UndefinedMetricWarning)

# Load a few test images and predict their labels
num_images_to_predict = 16  # Change this to the number of images you want to predict

# Get a few test images and their true labels
test_images, true_labels = next(test_generator)

# Predict labels for the test images
predicted_labels = model.predict(test_images)

# Convert predicted labels to binary (0 or 1)
predicted_labels = np.round(predicted_labels)

# Define class names
class_names = ['caries', 'no_caries']

# Define the number of rows and columns for subplots
num_rows = 4
num_cols = (num_images_to_predict + num_rows - 1) // num_rows

# Display the test images along with their predicted labels
plt.figure(figsize=(15, 10))
for i in range(num_images_to_predict):
    plt.subplot(num_rows, num_cols, i + 1)
    plt.imshow(test_images[i])
    plt.title(f"True: {class_names[int(true_labels[i])]}, Predicted: {class_names[int(predicted_labels[i])]}")
    plt.axis('off')

plt.subplots_adjust(wspace=0.5, hspace=0.5)  # Adjust the spacing between subplots
plt.show()
