import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from src.utils import DATA_DIR

def check_indices():
    datagen = ImageDataGenerator(rescale=1./255)
    generator = datagen.flow_from_directory(
        DATA_DIR,
        class_mode='categorical',
        batch_size=32,
        shuffle=False
    )
    print("Class Indices:", generator.class_indices)
    print("Classes found:", generator.classes)
    print("Filenames (first 5):", generator.filenames[:5])

if __name__ == "__main__":
    check_indices()
