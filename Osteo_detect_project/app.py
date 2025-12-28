import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import cv2
import os
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from src.utils import IMG_SIZE, CLASSES, MODEL_DIR, OUTPUT_DIR
from src.grad_cam import make_gradcam_heatmap, overlay_heatmap

# Page Config
st.set_page_config(
    page_title="Dr.Bones : Osteoporosis Detector",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utils
@st.cache_resource
def load_model_cached(model_name):
    path = os.path.join(MODEL_DIR, f"best_{model_name}.h5")
    if not os.path.exists(path):
        return None
    model = tf.keras.models.load_model(path)
    return model

def preprocess_image(image):
    image = image.resize(IMG_SIZE)
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def get_risk_level(severity, class_name):
    if class_name == 'normal':
        return "Low", "green"
    elif class_name == 'osteophenia':
        return "Medium", "orange"
    else: # osteoporosis
        return "High", "red"

def get_stage_description(class_name):
    if class_name == 'normal':
        return "Healthy Bone Structure"
    elif class_name == 'osteophenia':
        return "Early Stage Bone Loss (Osteopenia)"
    else:
        return "Severe Bone Loss (Osteoporosis)"

def get_suggestions(class_name):
    if class_name == 'normal':
        return [
            "Maintain a calcium-rich diet.",
            "Regular weight-bearing exercise.",
            "Vitamin D supplementation if needed."
        ]
    elif class_name == 'osteophenia':
        return [
            "Consult a doctor for bone density monitoring.",
            "Increase Calcium and Vitamin D intake.",
            "Lifestyle changes to prevent further loss."
        ]
    else:
        return [
            "**Urgent Medical Consultation Required.**",
            "Fall prevention strategies are critical.",
            "Prescription medication may be needed.",
            "Avoid high-impact activities that may cause fractures."
        ]

# Header
st.title("🦴 Dr.Bones : Osteoporosis Detection & Analysis")
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    .risk-high { color: red; font-weight: bold; }
    .risk-medium { color: orange; font-weight: bold; }
    .risk-low { color: green; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.warning("⚠️ DISCLAIMER: This tool is for research and assistance only and does not replace professional medical diagnosis.")

# Tabs
tab1, tab2, tab3 = st.tabs(["🕵️ Prediction & Analysis", "📊 Model Comparison", "📥 Downloads"])

# --- TAB 1: Prediction ---
with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload Spine X-Ray")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

        model_options = ["mobilenetv2", "resnet50", "efficientnetb0"]
        selected_model_name = st.selectbox("Select Model for Analysis", model_options, index=0)

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        
        with col1:
            st.image(image, caption='Uploaded X-Ray', use_container_width=True)

        # Process
        img_array = preprocess_image(image)
        model = load_model_cached(selected_model_name)

        if model is None:
            st.error(f"Model {selected_model_name} not found. Please train models first.")
        else:
            with st.spinner(f"Analyzing with {selected_model_name}..."):
                preds = model.predict(img_array)
                pred_class_idx = np.argmax(preds)
                pred_class = CLASSES[pred_class_idx]
                confidence = np.max(preds) * 100
                
                # Severity Estimation (Pseudo-metric based on class and confidence)
                # In a real regression model, this would be direct.
                # Here we simulate: Normal=0-30%, Osteopenia=30-70%, Osteoporosis=70-100%
                base_severity = {'normal': 10, 'osteophenia': 50, 'osteoporosis': 85}
                severity = base_severity[pred_class] + (np.random.randint(-5, 5)) 
                severity = np.clip(severity, 0, 100)

                risk_level, risk_color = get_risk_level(severity, pred_class)

            # Results Column
            with col2:
                st.subheader("Analysis Results")
                
                # Metrics
                st.markdown(f"**Predicted Stage:** {get_stage_description(pred_class)}")
                st.markdown(f"**Confidence:** {confidence:.2f}%")
                st.markdown(f"**Estimated Severity:** {severity}%")
                
                st.markdown(f"**Risk Level:** <span class='risk-{risk_color}'>{risk_level}</span>", unsafe_allow_html=True)
                st.progress(int(severity))

                st.subheader("Preventive Suggestions")
                for s in get_suggestions(pred_class):
                    st.markdown(f"- {s}")

                # Grad-CAM
                st.subheader("Explainable AI (Grad-CAM)")
                try:
                    # Determine last conv layer based on model
                    # This is model-specific and might need inspection.
                    # Commonly:
                    if 'mobilenet' in selected_model_name:
                        last_conv_layer = 'out_relu'
                    elif 'resnet' in selected_model_name:
                        last_conv_layer = 'conv5_block3_out'
                    elif 'efficientnet' in selected_model_name:
                        last_conv_layer = 'top_activation'
                    
                    # For safety, lets try to find the last 4D layer if possible or use known ones
                    # Or simpler: we will just catch error if layer name is wrong
                    heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer)
                    
                    # Overlay
                    orig_img_cv = np.array(image.convert('RGB'))
                    orig_img_cv = cv2.resize(orig_img_cv, IMG_SIZE)
                    superimposed_img = overlay_heatmap(orig_img_cv, heatmap)

                    st.image(superimposed_img, caption="Model Attention Map (Grad-CAM)", use_container_width=True)
                    st.info("Highlights indicate regions most influential to the model's prediction.")

                except Exception as e:
                    st.warning(f"Could not generate Grad-CAM: {e}. (Verify layer names for {selected_model_name})")


# --- TAB 2: Comparison ---
with tab2:
    st.subheader("Model Performance Comparison")
    results_path = os.path.join(OUTPUT_DIR, 'model_comparison.csv')
    
    if os.path.exists(results_path):
        df = pd.read_csv(results_path)
        st.dataframe(df.style.highlight_max(axis=0, color='lightgreen'))
        
        # Plots
        metric = st.selectbox("Select Metric to Visualize", ['Accuracy', 'Precision', 'Recall', 'F1-Score'])
        
        fig, ax = plt.subplots()
        sns.barplot(x='Model', y=metric, data=df, ax=ax, palette='viridis')
        plt.ylim(0, 1.1)
        st.pyplot(fig)
        
        best_model_row = df.loc[df['F1-Score'].idxmax()]
        st.success(f"🏆 Best Performing Model: **{best_model_row['Model']}** with F1-Score: **{best_model_row['F1-Score']:.4f}**")
        
    else:
        st.info("No comparison results found. Please run training first.")

# --- TAB 3: Downloads ---
with tab3:
    st.subheader("Download Reports")
    if os.path.exists(results_path):
        with open(results_path, "rb") as f:
            st.download_button(
                label="Download Model Comparison CSV",
                data=f,
                file_name="osteoporosis_model_comparison.csv",
                mime="text/csv"
            )
    else:
        st.info("Reports unavailable.")
