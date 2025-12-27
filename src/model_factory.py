import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2, ResNet50, EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from src.utils import IMG_SIZE, NUM_CLASSES, LEARNING_RATE

def build_model(model_name):
    """
    Builds and compiles a transfer learning model.
    """
    input_shape = IMG_SIZE + (3,)
    
    if model_name == 'mobilenetv2':
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
    elif model_name == 'resnet50':
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    elif model_name == 'efficientnetb0':
        base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=input_shape)
    else:
        raise ValueError(f"Unknown model name: {model_name}")

    # Freeze base model layers
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(NUM_CLASSES, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
                  loss='categorical_crossentropy',
                  metrics=['accuracy', tf.keras.metrics.Precision(name='precision'), tf.keras.metrics.Recall(name='recall')])
    
    return model

def unfreeze_model(model, num_layers=20):
    """
    Unfreezes the top N layers of the base model for fine-tuning.
    """
    # Finding the base model layer (usually indices 1 or similar in functional API if wrapped, 
    # but here we constructed with Model(inputs=base.input, ...))
    # In this construction, model.layers includes the base model's layers flattened if we used base_model.output directly? 
    # Actually, Keras Applications when used like `x = base_model.output` adds all layers to `model`.
    
    # We want to unfreeze the last N layers.
    for layer in model.layers[-num_layers:]:
        if not isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = True

    # Recompile with lower learning rate
    model.compile(optimizer=Adam(learning_rate=1e-5),
                  loss='categorical_crossentropy',
                  metrics=['accuracy', tf.keras.metrics.Precision(name='precision'), tf.keras.metrics.Recall(name='recall')])
    return model
