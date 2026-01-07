import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from pathlib import Path
import numpy as np

# ================= CONFIG =================
IMG_SIZE = 224
CLASS_NAMES = ['aothun', 'bottle', 'hoodie', 'lego', 'other']

BASE_DIR = Path(__file__).resolve().parent
WEIGHTS_PATH = BASE_DIR / "mobilenet_weights.weights.h5"

print("🔄 Building MobileNetV2 architecture...")

# Backbone
base_model = MobileNetV2(
    weights=None,               # ⚠️ QUAN TRỌNG
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

# Full model
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(len(CLASS_NAMES), activation="softmax")
])

print("🔄 Loading weights...")
model.load_weights(WEIGHTS_PATH)

print("✅ Model loaded successfully (weights-only)")

# ===== PREDICT FUNCTION =====
def predict_image(img_path):

    # Load & preprocess ảnh
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_arr = image.img_to_array(img)
    img_arr = np.expand_dims(img_arr, axis=0)
    img_arr = preprocess_input(img_arr)

    # Dự đoán
    preds = model.predict(img_arr, verbose=0)
    pred_idx = np.argmax(preds)
    confidence = float(np.max(preds))
    label = CLASS_NAMES[pred_idx]

    return label, confidence