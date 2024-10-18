import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define image size and input shape
img_width, img_height = 128, 128
input_shape = (img_width, img_height, 3)

# CNN Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    MaxPooling2D(pool_size=(2, 2)),
    BatchNormalization(),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    BatchNormalization(),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    BatchNormalization(),

    Flatten(),

    Dense(128, activation='relu'),
    Dropout(0.5),

    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'deepfake_database/deepfake_database/train_test',
    target_size=(img_width, img_height),
    batch_size=32,  # Adjust the batch size as needed
    class_mode='binary',
    shuffle=True)

validation_generator = validation_datagen.flow_from_directory(
    'deepfake_database/deepfake_database/validation',
    target_size=(img_width, img_height),
    batch_size=32,  # Adjust the batch size as needed
    class_mode='binary',
    shuffle=False)

model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator)

# Save the model
model.save('deepfake_cnn_model.h5')
