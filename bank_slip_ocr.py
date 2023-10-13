import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Data Setup
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=15,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   shear_range=0.1,
                                   zoom_range=0.1,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'data/train/',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary')

test_generator = test_datagen.flow_from_directory(
    'data/test/',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary')

# Model Definition
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
model.add(MaxPooling2D(2, 2))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(2, 2))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the Model
history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=20,
    validation_data=test_generator,
    validation_steps=len(test_generator))

# Save the model
model.save("bank_slip_classifier.h5")

# Prediction Function
def predict_bank_slip(img_path, model):
    img = load_img(img_path, target_size=(128, 128))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.
    result = model.predict(x)
    if result[0][0] > 0.5:
        return "This is a bank slip."
    else:
        return "This is not a bank slip."

# Example Prediction (comment out if not required immediately)
loaded_model = tf.keras.models.load_model("bank_slip_classifier.h5")
image_path = "C:\\Users\\Ipin0\\trainslip\\data\\train\\slip\\IMG_2805.JPG"
print(predict_bank_slip(image_path, loaded_model))
