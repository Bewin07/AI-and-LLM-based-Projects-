import os

# Constants
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15 # Can be increased for better results
LEARNING_RATE = 1e-4
CLASSES = ['normal', 'osteophenia', 'osteoporosis']
NUM_CLASSES = len(CLASSES)
DATA_DIR = os.path.join(os.getcwd(), 'resources')
MODEL_DIR = os.path.join(os.getcwd(), 'models')
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')

# Create directories if they don't exist
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_class_name(class_index):
    return CLASSES[class_index]
