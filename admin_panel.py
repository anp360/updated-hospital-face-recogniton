import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

PATIENT_DATA_PATH = "patient_data.csv"
VISIT_LOGS_PATH = "visit_logs.csv"

def open_admin_panel():
    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("450x500")

    title_label = tk.Label(root, text="Welcome to the Admin Panel", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=20)

    def view_all_patients():
        if not os.path.exists(PATIENT_DATA_PATH):
            messagebox.showerror("Error", "Patient data file not found.")
            return

        df = pd.read_csv(PATIENT_DATA_PATH)

        view_win = tk.Toplevel(root)
        view_win.title("All Patients")
        text = tk.Text(view_win, wrap="none", width=100)
        text.pack()

        text.insert(tk.END, df.to_string(index=False))

    def edit_patient_details():
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Patient Details")
        edit_window.geometry("400x400")

        tk.Label(edit_window, text="Enter Patient ID to Edit", font=("Helvetica", 12)).pack(pady=10)
        id_entry = tk.Entry(edit_window, font=("Helvetica", 12))
        id_entry.pack(pady=5)

        def load_details():
            patient_id = id_entry.get().strip()
            if not os.path.exists(PATIENT_DATA_PATH):
                messagebox.showerror("Error", "Patient data file not found.")
                return
            df = pd.read_csv(PATIENT_DATA_PATH)

            if patient_id not in df['PatientID'].astype(str).values:
                messagebox.showerror("Error", "Patient ID not found.")
                return

            patient = df[df['PatientID'].astype(str) == patient_id].iloc[0]

            name_var.set(patient['Name'])
            age_var.set(patient['Age'])
            disease_var.set(patient['Disease'])
            medicine_var.set(patient['Medicines'])

        name_var = tk.StringVar()
        age_var = tk.StringVar()
        disease_var = tk.StringVar()
        medicine_var = tk.StringVar()

        tk.Button(edit_window, text="Load Details", command=load_details).pack(pady=5)

        tk.Label(edit_window, text="Name").pack()
        name_entry = tk.Entry(edit_window, textvariable=name_var)
        name_entry.pack()

        tk.Label(edit_window, text="Age").pack()
        age_entry = tk.Entry(edit_window, textvariable=age_var)
        age_entry.pack()

        tk.Label(edit_window, text="Disease").pack()
        disease_entry = tk.Entry(edit_window, textvariable=disease_var)
        disease_entry.pack()

        tk.Label(edit_window, text="Medicines").pack()
        medicine_entry = tk.Entry(edit_window, textvariable=medicine_var)
        medicine_entry.pack()

        def save_changes():
            patient_id = id_entry.get().strip()
            df = pd.read_csv(PATIENT_DATA_PATH)
            index = df[df['PatientID'].astype(str) == patient_id].index[0]

            df.at[index, 'Name'] = name_var.get()
            df.at[index, 'Age'] = age_var.get()
            df.at[index, 'Disease'] = disease_var.get()
            df.at[index, 'Medicines'] = medicine_var.get()

            df.to_csv(PATIENT_DATA_PATH, index=False)
            messagebox.showinfo("Success", "Patient details updated successfully.")
            edit_window.destroy()

        tk.Button(edit_window, text="Save Changes", command=save_changes, bg="lightgreen").pack(pady=15)

    def delete_patient():
        del_window = tk.Toplevel(root)
        del_window.title("Delete Patient")

        tk.Label(del_window, text="Enter Patient ID to Delete", font=("Helvetica", 12)).pack(pady=10)
        id_entry = tk.Entry(del_window, font=("Helvetica", 12))
        id_entry.pack(pady=5)

        def confirm_delete():
            patient_id = id_entry.get().strip()
            if not os.path.exists(PATIENT_DATA_PATH):
                messagebox.showerror("Error", "Patient data file not found.")
                return

            df = pd.read_csv(PATIENT_DATA_PATH)

            if patient_id not in df['PatientID'].astype(str).values:
                messagebox.showerror("Error", "Patient ID not found.")
                return

            df = df[df['PatientID'].astype(str) != patient_id]
            df.to_csv(PATIENT_DATA_PATH, index=False)
            messagebox.showinfo("Success", f"Patient ID {patient_id} deleted successfully.")
            del_window.destroy()

        tk.Button(del_window, text="Delete", command=confirm_delete, bg="red", fg="white").pack(pady=10)

    def view_visit_logs():
        if not os.path.exists(VISIT_LOGS_PATH):
            messagebox.showerror("Error", "Visit log file not found.")
            return

        df = pd.read_csv(VISIT_LOGS_PATH)

        log_win = tk.Toplevel(root)
        log_win.title("Visit Logs")
        text = tk.Text(log_win, wrap="none", width=100)
        text.pack()

        text.insert(tk.END, df.to_string(index=False))

    def logout():
        root.destroy()

    tk.Button(root, text="📄 View All Patients", width=30, command=view_all_patients).pack(pady=5)
    tk.Button(root, text="✏️ Edit Patient Details", width=30, command=edit_patient_details).pack(pady=5)
    tk.Button(root, text="🗑️ Delete Patient", width=30, command=delete_patient).pack(pady=5)
    tk.Button(root, text="📘 View Visit Logs", width=30, command=view_visit_logs).pack(pady=5)
    tk.Button(root, text="🔒 Logout / Exit", width=30, command=logout).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    open_admin_panel()
