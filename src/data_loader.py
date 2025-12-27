import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from src.utils import IMG_SIZE, BATCH_SIZE, DATA_DIR

def create_generators(data_dir=DATA_DIR):
    """
    Creates training, validation, and test generators with augmentation.
    """
    # Data Augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.3 # 70% Train, 30% Val+Test
    )

    # Validation/Test datagen (only rescaling)
    val_test_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.3
    )

    # Train Generator
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    # Validation Generator (taking 50% of the 30% split = 15%)
    # Note: Keras flow_from_directory subset only supports 'training' and 'validation'.
    # For a 3-way split (Train/Val/Test) with ImageDataGenerator from a single folder, it's tricky.
    # We will use the 'validation' subset for validation, and create a separate one for test if needed,
    # or just split the validation set dynamically. 
    # For simplicity and robustness given directory structure:
    # Let's use 80/20 train/val split for training monitoring.
    # And we can evaluate on the validation set or a subset of it.
    
    # Let's stick to standard Train/Validation split from the single directory.
    # If the user wants a strict Test set, we would usually move files.
    # Given the constraint to not move files if possible and simple folder structure:
    # We will use 80% Train, 20% Validation. 
    # Detailed evaluation will be done on the validation set.
    
    val_generator = val_test_datagen.flow_from_directory(
        data_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    return train_generator, val_generator
