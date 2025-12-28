import os
import pandas as pd
import tensorflow as tf
from src.utils import MODEL_DIR, OUTPUT_DIR, EPOCHS, BATCH_SIZE
from src.data_loader import create_generators
from src.model_factory import build_model
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score, accuracy_score
import numpy as np

def train_and_evaluate():
    models_to_train = ['mobilenetv2', 'resnet50', 'efficientnetb0']
    results = []

    train_gen, val_gen = create_generators()

    for model_name in models_to_train:
        print(f"Training {model_name}...")
        model = build_model(model_name)
        
        # Callbacks
        checkpoint_path = os.path.join(MODEL_DIR, f"best_{model_name}.h5")
        callbacks = [
            tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_best_only=True, monitor='val_accuracy', mode='max'),
            tf.keras.callbacks.EarlyStopping(patience=5, monitor='val_loss', restore_best_weights=True)
        ]

        history = model.fit(
            train_gen,
            epochs=EPOCHS,
            validation_data=val_gen,
            callbacks=callbacks
        )

        # Fine-tuning Phase
        print(f"Fine-tuning {model_name}...")
        from src.model_factory import unfreeze_model
        model = unfreeze_model(model, num_layers=30)
        
        # Fine-tuning callbacks (save best of fine-tuning)
        ft_callbacks = [
            tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_best_only=True, monitor='val_accuracy', mode='max'),
            tf.keras.callbacks.EarlyStopping(patience=5, monitor='val_loss', restore_best_weights=True)
        ]
        
        history_ft = model.fit(
            train_gen,
            epochs=10, # Additional epochs for fine-tuning
            validation_data=val_gen,
            callbacks=ft_callbacks
        )

        # Evaluation (Load best weights from either phase)
        model.load_weights(checkpoint_path)
        print(f"Evaluating {model_name}...")
        # Reset validation generator
        val_gen.reset()
        predictions = model.predict(val_gen)
        y_pred = np.argmax(predictions, axis=1)
        y_true = val_gen.classes

        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

        results.append({
            'Model': model_name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-Score': f1
        })
        
        print(f"{model_name} Results: Accuracy={acc:.4f}, F1={f1:.4f}")

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(OUTPUT_DIR, 'model_comparison.csv'), index=False)
    print("Training complete. Results saved.")
    
    return results_df

if __name__ == '__main__':
    train_and_evaluate()
