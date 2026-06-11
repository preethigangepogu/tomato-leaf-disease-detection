<<<<<<< HEAD
import os
import cv2
import numpy as np

# Dataset path
dataset_path = "C:/Users/gakil/Desktop/Tomato Dataset"

# Image size
IMG_SIZE = 256

# Disease classes
classes = [
    "Bacterial Spot",
    "Early Blight",
    "Healthy",
    "Late Blight",
    "Septoria Leaf Spot",
    "Yellow Leaf Curl Virus"
]

# Lists for images and labels
data = []
labels = []

# Preprocessing dataset
for class_name in classes:
    class_path = os.path.join(dataset_path, class_name)
    class_index = classes.index(class_name)

    for img_name in os.listdir(class_path):
        try:
            img_path = os.path.join(class_path, img_name)

            # Read image
            img = cv2.imread(img_path)

            # Resize image
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

            # Normalize image
            img = img / 255.0

            # Store image and label
            data.append(img)
            labels.append(class_index)

        except Exception as e:
            print(f"Error processing image: {img_name}")

# Convert to numpy arrays
data = np.array(data)
labels = np.array(labels)

print("Preprocessing Completed")
=======
import os
import cv2
import numpy as np

# Dataset path
dataset_path = "C:/Users/gakil/Desktop/Tomato Dataset"

# Image size
IMG_SIZE = 256

# Disease classes
classes = [
    "Bacterial Spot",
    "Early Blight",
    "Healthy",
    "Late Blight",
    "Septoria Leaf Spot",
    "Yellow Leaf Curl Virus"
]

# Lists for images and labels
data = []
labels = []

# Preprocessing dataset
for class_name in classes:
    class_path = os.path.join(dataset_path, class_name)
    class_index = classes.index(class_name)

    for img_name in os.listdir(class_path):
        try:
            img_path = os.path.join(class_path, img_name)

            # Read image
            img = cv2.imread(img_path)

            # Resize image
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

            # Normalize image
            img = img / 255.0

            # Store image and label
            data.append(img)
            labels.append(class_index)

        except Exception as e:
            print(f"Error processing image: {img_name}")

# Convert to numpy arrays
data = np.array(data)
labels = np.array(labels)

print("Preprocessing Completed")
>>>>>>> 55f015d0840e17926785313512fef6048d0d9875
print("Total Images:", len(data))