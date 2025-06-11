import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, 
    precision_score, recall_score, f1_score, cohen_kappa_score, 
    matthews_corrcoef, roc_auc_score
)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# Load dataset
df = pd.read_csv("final_clean_dataset_flow_0.3_to_30.csv")

# --- DATA CLEANING ---
df = df.drop(columns=["timestamp"])
df["anomaly_type"] = df["anomaly_type"].fillna("None").astype(str)
df = pd.get_dummies(df, columns=["sensor_id", "pump_status"])

# Label encode target
label_encoder = LabelEncoder()
df["anomaly_type"] = label_encoder.fit_transform(df["anomaly_type"])

# Split features and target
X = df.drop(columns=["anomaly_type"])
y = df["anomaly_type"]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# One-hot encode labels
y_categorical = to_categorical(y)

# --- CREATE SEQUENCES FOR LSTM ---
def create_sequences(X, y, time_steps=5):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:i + time_steps])
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

X_seq, y_seq = create_sequences(X_scaled, y_categorical)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

# Load and preprocess data
df = pd.read_csv("final_clean_dataset_flow_0.3_to_30.csv")

# Drop unused columns
df = df.drop(columns=["timestamp", "anomaly_type"])

# One-hot encode categorical variables
df = pd.get_dummies(df, columns=["sensor_id", "pump_status"])

# Save feature column names for GUI use
with open("feature_columns.txt", "w") as f:
    for col in df.columns:
        f.write(col + "\n")

print("✅ Saved feature_columns.txt with", len(df.columns), "features.")

# --- LSTM MODEL ---
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X_seq.shape[1], X_seq.shape[2])),
    Dropout(0.3),
    LSTM(64),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(y_categorical.shape[1], activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2, verbose=1)

# --- PREDICTIONS ---
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)

# --- METRICS CALCULATION ---
class_names = [str(cls) for cls in label_encoder.classes_]

print("\n--- Classification Report ---")
print(classification_report(y_true_classes, y_pred_classes, target_names=class_names, zero_division=1))

print("\n--- Accuracy ---")
print("Accuracy:", accuracy_score(y_true_classes, y_pred_classes))

print("\n--- Precision, Recall, F1 (Macro) ---")
print("Precision (macro):", precision_score(y_true_classes, y_pred_classes, average='macro', zero_division=1))
print("Recall (macro):", recall_score(y_true_classes, y_pred_classes, average='macro', zero_division=1))
print("F1 Score (macro):", f1_score(y_true_classes, y_pred_classes, average='macro', zero_division=1))

print("\n--- Cohen’s Kappa ---")
print("Cohen Kappa:", cohen_kappa_score(y_true_classes, y_pred_classes))

print("\n--- Matthews Correlation Coefficient ---")
print("MCC:", matthews_corrcoef(y_true_classes, y_pred_classes))

# ROC-AUC (multi-class, one-vs-rest)
try:
    roc_auc = roc_auc_score(y_test, y_pred, multi_class='ovr')
    print("\n--- ROC AUC Score (OVR) ---")
    print("ROC AUC (OVR):", roc_auc)
except ValueError as e:
    print("\nROC AUC could not be computed:", str(e))

print("\n--- Confusion Matrix ---")
print(confusion_matrix(y_true_classes, y_pred_classes))

# --- PLOT TRAINING CURVES ---
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label="Train Accuracy")
plt.plot(history.history['val_accuracy'], label="Val Accuracy")
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label="Train Loss")
plt.plot(history.history['val_loss'], label="Val Loss")
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.tight_layout()
plt.show()

import joblib
from tensorflow.keras.models import save_model

# Save the model
model.save("model.h5")

# Save scaler and label encoder
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
