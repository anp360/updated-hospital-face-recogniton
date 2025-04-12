import cv2
import os
import csv
import pandas as pd

# Paths
DATASET_DIR = os.path.join(os.getcwd(), "dataset")
PATIENT_DATA_PATH = os.path.join(os.getcwd(), "patient_data.csv")
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Create dataset folder if not exists
os.makedirs(DATASET_DIR, exist_ok=True)

def capture_patient_faces(patient_id, name):
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    cap = cv2.VideoCapture(0)

    count = 0
    patient_dir = os.path.join(DATASET_DIR, str(patient_id))
    os.makedirs(patient_dir, exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            face_path = os.path.join(patient_dir, f"{count}.jpg")
            cv2.imwrite(face_path, face_img)
            count += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Capturing {count}/50", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Capture Faces", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 50:
            break

    cap.release()
    cv2.destroyAllWindows()

def save_patient_info(patient_id, name, age, disease, medicines):
    file_exists = os.path.isfile(PATIENT_DATA_PATH)

    with open(PATIENT_DATA_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["PatientID", "Name", "Age", "Disease", "Medicines"])
        writer.writerow([patient_id, name, age, disease, medicines])

# ===== Main =====
print("=== Add New Patient ===")
name = input("Enter patient name: ")
patient_id = input("Enter patient ID (must be unique): ")
age = input("Enter patient age: ")
disease = input("Enter disease: ")
medicines = input("Enter medicines (comma separated): ")

# Check for duplicate patient ID
if os.path.exists(PATIENT_DATA_PATH):
    df = pd.read_csv(PATIENT_DATA_PATH)
    if patient_id in df["PatientID"].astype(str).values:
        print("❌ Error: Patient ID already exists. Choose a unique ID.")
        exit()

save_patient_info(patient_id, name, age, disease, medicines)
capture_patient_faces(patient_id, name)
print("✅ Patient added successfully!")
