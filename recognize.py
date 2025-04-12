import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime

# Paths
MODEL_PATH = os.path.join("trained_model", "face_model.yml")
LABEL_MAP_PATH = "label_map.csv"
PATIENT_DATA_PATH = "patient_data.csv"
VISIT_LOGS_PATH = "visit_logs.csv"
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Load model and cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

# Load mappings
label_df = pd.read_csv(LABEL_MAP_PATH)
label_map = dict(zip(label_df["Label"], label_df["PatientID"]))

# Load patient data
patient_df = pd.read_csv(PATIENT_DATA_PATH)
patient_info = patient_df.set_index("PatientID").T.to_dict()

# Ensure visit log exists
if not os.path.exists(VISIT_LOGS_PATH):
    with open(VISIT_LOGS_PATH, 'w') as f:
        f.write("Timestamp,PatientID,Name\n")

def log_visit(patient_id, name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(VISIT_LOGS_PATH, 'a') as f:
        f.write(f"{timestamp},{patient_id},{name}\n")

# Start webcam
cap = cv2.VideoCapture(0)
recognized_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        label, confidence = recognizer.predict(face_img)

        if confidence < 60:
            patient_id = label_map.get(label, "Unknown")
            data = patient_info.get(patient_id, {})
            name = data.get("Name", "Unknown")

            # Log only once per session
            if patient_id != "Unknown" and patient_id not in recognized_ids:
                log_visit(patient_id, name)
                recognized_ids.add(patient_id)

            # Info to display
            age = data.get("Age", "N/A")
            disease = data.get("Disease", "N/A")
            medicines = data.get("Medicines", "N/A")

            lines = [
                f"Name: {name}",
                f"ID: {patient_id}",
                f"Age: {age}",
                f"Disease: {disease}",
                f"Medicines: {medicines}"
            ]
        else:
            lines = ["Unknown"]

        # Draw box and text
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        for i, line in enumerate(lines):
            cv2.putText(frame, line, (x, y - 10 - i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Patient Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
